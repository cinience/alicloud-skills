import argparse
import json
import time
from collections import Counter

from alibabacloud_arms20190808 import models

from _common import create_client, default_region


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="ARMS get trace detail")
    parser.add_argument("--trace-id", required=True)
    parser.add_argument("--region", default=default_region())
    parser.add_argument("--start", type=int, default=None, help="start time in epoch ms")
    parser.add_argument("--end", type=int, default=None, help="end time in epoch ms")
    parser.add_argument("--page", type=int, default=None)
    parser.add_argument("--page-size", type=int, default=None)
    parser.add_argument("--tree", action="store_true", help="render span tree with analysis")
    return parser.parse_args()


def parse_span(span) -> dict:
    return {
        "span_id": span.span_id,
        "parent_span_id": span.parent_span_id,
        "operation_name": span.operation_name,
        "service_name": span.service_name,
        "service_ip": span.service_ip,
        "duration": span.duration,
        "timestamp": span.timestamp,
        "result_code": span.result_code,
        "have_stack": span.have_stack,
        "rpc_id": span.rpc_id,
        "tag_entry_list": [
            {"key": t.key, "value": t.value}
            for t in (span.tag_entry_list or [])
        ],
        "log_event_list": [
            {
                "timestamp": e.timestamp,
                "tag_entry_list": [
                    {"key": t.key, "value": t.value}
                    for t in (e.tag_entry_list or [])
                ],
            }
            for e in (span.log_event_list or [])
        ],
    }


def tags_dict(span: dict) -> dict[str, str]:
    return {t["key"]: t["value"] for t in span["tag_entry_list"]}


def span_summary(span: dict) -> str:
    """One-line summary with key attributes."""
    t = tags_dict(span)
    op = span["operation_name"]
    parts = []

    if op.startswith("model."):
        if "model.name" in t:
            parts.append(f"model={t['model.name']}")
        if "model.stop_reason" in t:
            parts.append(f"stop={t['model.stop_reason']}")
        if "model.input_tokens" in t:
            parts.append(f"in={t['model.input_tokens']} out={t['model.output_tokens']}")
        if "model.cache_read_tokens" in t:
            cr, cw = t.get("model.cache_read_tokens", "0"), t.get("model.cache_creation_tokens", "0")
            parts.append(f"cache_r={cr} cache_w={cw}")
        if "model.provider" in t:
            parts.append(f"provider={t['model.provider']}")
    elif op == "tool.execute":
        if "tool.name" in t:
            parts.append(f"tool={t['tool.name']}")
        if "tool.input" in t:
            inp = t["tool.input"]
            if len(inp) > 80:
                inp = inp[:77] + "..."
            parts.append(f"cmd={inp}")
        elif "tool.input_size" in t:
            parts.append(f"input={t['tool.input_size']}B")
        if "tool.output_size" in t:
            parts.append(f"output={t['tool.output_size']}B")
        if "tool.status" in t:
            parts.append(f"status={t['tool.status']}")
    elif op == "agent.run":
        if "agent.model" in t:
            parts.append(f"model={t['agent.model']}")
        if "agent.stop_reason" in t:
            parts.append(f"stop={t['agent.stop_reason']}")
        if "agent.input_tokens" in t:
            parts.append(f"in={t['agent.input_tokens']} out={t['agent.output_tokens']}")
        if "agent.stream" in t:
            parts.append(f"stream={t['agent.stream']}")
    elif op == "permission.check":
        if "permission.tool" in t:
            parts.append(f"tool={t['permission.tool']}")
        if "permission.decision" in t:
            parts.append(f"decision={t['permission.decision']}")
    elif op == "subagent.run":
        if "subagent.name" in t:
            parts.append(f"name={t['subagent.name']}")
        if "subagent.type" in t:
            parts.append(f"type={t['subagent.type']}")

    if "session.id" in t and op in ("agent.run",):
        parts.append(f"session={t['session.id'][:8]}...")

    return "  ".join(parts)


def duration_bar(dur_ms: int, max_ms: int, width: int = 20) -> str:
    if max_ms <= 0:
        return ""
    filled = min(width, max(1, int(dur_ms / max_ms * width))) if dur_ms > 0 else 0
    return "█" * filled + "░" * max(0, width - filled)


def slow_marker(dur_ms: int) -> str:
    if dur_ms >= 10000:
        return " ❌ VERY SLOW"
    if dur_ms >= 3000:
        return " ⚠ SLOW"
    return ""


def render_tree(spans: list[dict]) -> None:
    if not spans:
        print("No spans found.")
        return

    by_id: dict[str, dict] = {s["span_id"]: s for s in spans}
    children: dict[str, list[str]] = {}
    for s in spans:
        children.setdefault(s["parent_span_id"], []).append(s["span_id"])

    # Find roots (parent not in span set)
    all_ids = set(by_id.keys())
    root_parents = set(s["parent_span_id"] for s in spans) - all_ids
    roots = []
    for rp in root_parents:
        for sid in children.get(rp, []):
            roots.append(sid)
    roots.sort(key=lambda sid: by_id[sid]["timestamp"])

    # Use second-longest span for bar scale to avoid container spans (cli.session)
    # compressing all bars to 1 pixel.
    durations = sorted((s["duration"] for s in spans), reverse=True)
    max_dur = durations[1] if len(durations) > 1 else durations[0] if durations else 1
    base_ts = min((s["timestamp"] for s in spans), default=0)

    # Collect all spans for agent.run to show iteration timeline
    agent_start = None
    for s in spans:
        if s["operation_name"] == "agent.run":
            agent_start = s["timestamp"]
            break
    if agent_start is None:
        agent_start = base_ts

    print(f"\n{'='*100}")
    print(f"Trace: {spans[0].get('trace_id', 'N/A') if spans else 'N/A'}")

    # Span type counts
    ops = Counter(s["operation_name"] for s in spans)
    print(f"Spans: {len(spans)} total  ({', '.join(f'{op}:{cnt}' for op, cnt in ops.most_common())})")

    if root_parents:
        print(f"Missing parent spans: {root_parents} (still running or not exported)")
    print(f"{'='*100}\n")

    # Header
    print(f"{'Offset':>8s}  {'Dur':>7s}  {'Bar':<20s}  {'Operation':<28s}  Details")
    print("-" * 110)

    def print_node(sid: str, depth: int = 0) -> None:
        s = by_id[sid]
        op = s["operation_name"]
        dur = s["duration"]
        offset = s["timestamp"] - agent_start
        indent = "  " * depth
        bar = duration_bar(dur, max_dur)
        summary = span_summary(s)
        marker = slow_marker(dur)

        print(f"{offset:>7d}ms {dur:>6d}ms  {bar:<20s}  {indent}{op:<{28 - len(indent)}s}  {summary}{marker}")

        # Show span events
        for evt in s.get("log_event_list", []):
            evt_tags = {t["key"]: t["value"] for t in evt.get("tag_entry_list", [])}
            evt_offset = (evt["timestamp"] or 0) - agent_start if evt.get("timestamp") else 0
            evt_name = evt_tags.get("event", "event")
            evt_details = ", ".join(f"{k}={v}" for k, v in evt_tags.items() if k != "event")
            print(f"{evt_offset:>7d}ms          {'':20s}  {indent}  └─ {evt_name}: {evt_details}")

        # Recurse children sorted by timestamp
        child_ids = children.get(sid, [])
        child_ids.sort(key=lambda cid: by_id[cid]["timestamp"])
        for cid in child_ids:
            print_node(cid, depth + 1)

    for rid in roots:
        print_node(rid)

    # Bottleneck analysis
    print(f"\n{'='*100}")
    print("Bottleneck Analysis")
    print(f"{'='*100}")

    slow = sorted(spans, key=lambda s: s["duration"], reverse=True)[:5]
    for i, s in enumerate(slow, 1):
        t = tags_dict(s)
        op = s["operation_name"]
        dur = s["duration"]
        extra = ""
        if op == "tool.execute":
            extra = f"  tool={t.get('tool.name', '?')}"
            if "tool.input" in t:
                inp = t["tool.input"][:60]
                extra += f"  cmd={inp}"
        elif op.startswith("model."):
            extra = f"  model={t.get('model.name', '?')}"
        elif op == "agent.run":
            extra = f"  model={t.get('agent.model', '?')}"
        bar = duration_bar(dur, max_dur, 30)
        print(f"  #{i}  {dur:>6d}ms  {bar}  {op}{extra}")

    # Token summary
    total_input = 0
    total_output = 0
    total_cache_r = 0
    total_cache_w = 0
    model_calls = 0
    for s in spans:
        if s["operation_name"] == "model.generate":
            t = tags_dict(s)
            model_calls += 1
            total_input += int(t.get("model.input_tokens", 0))
            total_output += int(t.get("model.output_tokens", 0))
            total_cache_r += int(t.get("model.cache_read_tokens", 0))
            total_cache_w += int(t.get("model.cache_creation_tokens", 0))

    if model_calls:
        print(f"\n  Model calls: {model_calls}")
        print(f"  Total tokens: input={total_input}  output={total_output}  cache_read={total_cache_r}  cache_write={total_cache_w}")

    # Tool summary
    tool_spans = [s for s in spans if s["operation_name"] == "tool.execute"]
    if tool_spans:
        print(f"\n  Tool calls: {len(tool_spans)}")
        for s in sorted(tool_spans, key=lambda x: x["duration"], reverse=True):
            t = tags_dict(s)
            name = t.get("tool.name", "?")
            dur = s["duration"]
            inp = t.get("tool.input", "")
            if len(inp) > 60:
                inp = inp[:57] + "..."
            status = t.get("tool.status", "?")
            bar = duration_bar(dur, max_dur, 15)
            print(f"    {name:15s}  {dur:6d}ms  {bar}  status={status}  {inp}")

    print()


def main() -> None:
    args = parse_args()
    client = create_client(args.region)

    end_ms = args.end or int(time.time() * 1000)
    start_ms = args.start or (end_ms - 24 * 60 * 60 * 1000)

    request = models.GetTraceRequest(
        trace_id=args.trace_id,
        region_id=args.region,
        start_time=start_ms,
        end_time=end_ms,
        page_number=args.page,
        page_size=args.page_size,
    )
    response = client.get_trace(request)

    spans = [parse_span(s) for s in (response.body.spans or [])]

    if args.tree:
        render_tree(spans)
    else:
        result = {
            "trace_id": args.trace_id,
            "span_count": len(spans),
            "spans": spans,
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
