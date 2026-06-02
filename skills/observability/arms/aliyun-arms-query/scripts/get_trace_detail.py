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
    parser.add_argument("--summary", action="store_true", help="compact view without span events")
    parser.add_argument("--expand-progress", action="store_true", help="show all progress events (default: collapsed)")
    return parser.parse_args()


def parse_span(span) -> dict:
    return {
        "trace_id": span.trace_id,
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
        if "model.iteration" in t:
            parts.append(f"iter={t['model.iteration']}")
        if "model.stop_reason" in t:
            parts.append(f"stop={t['model.stop_reason']}")
        if "model.input_tokens" in t:
            parts.append(f"in={t['model.input_tokens']} out={t['model.output_tokens']}")
        if "model.cache_read_tokens" in t:
            cr, cw = t.get("model.cache_read_tokens", "0"), t.get("model.cache_creation_tokens", "0")
            parts.append(f"cache_r={cr} cache_w={cw}")
        if "model.ttft_ms" in t:
            parts.append(f"ttft={t['model.ttft_ms']}ms")
        if "model.retries" in t:
            parts.append(f"retries={t['model.retries']}")
        if "model.error_reason" in t:
            parts.append(f"err={t['model.error_reason']}")
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
        if "agent.model_stop_reason" in t:
            parts.append(f"model_stop={t['agent.model_stop_reason']}")
        if "agent.iterations" in t:
            parts.append(f"iters={t['agent.iterations']}")
        if "agent.input_tokens" in t:
            parts.append(f"in={t['agent.input_tokens']} out={t['agent.output_tokens']}")
        if "agent.stream" in t:
            parts.append(f"stream={t['agent.stream']}")
        if "agent.passthrough_tools" in t:
            parts.append(f"passthrough=[{t['agent.passthrough_tools']}]")
    elif op == "agent.passthrough":
        if "agent.passthrough_tools" in t:
            parts.append(f"tools=[{t['agent.passthrough_tools']}]")
        if "agent.iteration" in t:
            parts.append(f"iter={t['agent.iteration']}")
    elif op == "permission.check":
        if "permission.tool" in t:
            parts.append(f"tool={t['permission.tool']}")
        if "permission.decision" in t:
            parts.append(f"decision={t['permission.decision']}")
    elif op in ("subagent.run", "subagent.dispatch"):
        if "subagent.target" in t:
            parts.append(f"target={t['subagent.target']}")
        if "subagent.name" in t:
            parts.append(f"name={t['subagent.name']}")
        if "subagent.type" in t:
            parts.append(f"type={t['subagent.type']}")
        if "subagent.entry_point" in t:
            parts.append(f"entry={t['subagent.entry_point']}")
        if "subagent.output_len" in t:
            parts.append(f"out_len={t['subagent.output_len']}")

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


def _render_events(s: dict, depth: int, agent_start: int, expand_progress: bool) -> None:
    """Render span events, collapsing progress events by default."""
    events = s.get("log_event_list", [])
    if not events:
        return

    indent = "  " * depth

    if expand_progress:
        for evt in events:
            evt_tags = {t["key"]: t["value"] for t in evt.get("tag_entry_list", [])}
            evt_offset = (evt["timestamp"] or 0) - agent_start if evt.get("timestamp") else 0
            evt_name = evt_tags.get("event", "event")
            evt_details = ", ".join(f"{k}={v}" for k, v in evt_tags.items() if k != "event")
            print(f"{evt_offset:>7d}ms          {'':20s}  {indent}  └─ {evt_name}: {evt_details}")
        return

    progress_events: list[dict] = []
    non_progress_buffer: list[tuple] = []

    def flush_progress() -> None:
        if not progress_events:
            return
        pcts = []
        first_ts = None
        last_ts = None
        last_msg = ""
        for pe in progress_events:
            tags = {t["key"]: t["value"] for t in pe.get("tag_entry_list", [])}
            pct_str = tags.get("progress.pct", "")
            if pct_str:
                try:
                    pcts.append(int(pct_str))
                except ValueError:
                    pass
            ts = pe.get("timestamp") or 0
            if first_ts is None:
                first_ts = ts
            last_ts = ts
            last_msg = tags.get("progress.msg", last_msg)
            last_phase = tags.get("progress.phase", "")

        min_pct = min(pcts) if pcts else "?"
        max_pct = max(pcts) if pcts else "?"
        duration_s = ((last_ts or 0) - (first_ts or 0)) / 1000 if first_ts and last_ts else 0
        offset = (first_ts or 0) - agent_start

        detail = f"{min_pct}% → {max_pct}% ({len(progress_events)} events, {duration_s:.0f}s"
        if last_msg:
            detail += f", {last_msg}"
        detail += ")"
        print(f"{offset:>7d}ms          {'':20s}  {indent}  └─ progress: {detail}")
        progress_events.clear()

    for evt in events:
        evt_tags = {t["key"]: t["value"] for t in evt.get("tag_entry_list", [])}
        evt_name = evt_tags.get("event", "event")

        if "progress.pct" in evt_tags:
            progress_events.append(evt)
        else:
            flush_progress()
            evt_offset = (evt["timestamp"] or 0) - agent_start if evt.get("timestamp") else 0
            evt_details = ", ".join(f"{k}={v}" for k, v in evt_tags.items() if k != "event")
            print(f"{evt_offset:>7d}ms          {'':20s}  {indent}  └─ {evt_name}: {evt_details}")

    flush_progress()


def render_tree(spans: list[dict], *, summary: bool = False, expand_progress: bool = False) -> None:
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
    # Filter out legitimate root markers
    missing_parents = root_parents - {"", "0000000000000000"}
    roots = []
    for rp in root_parents:
        for sid in children.get(rp, []):
            roots.append(sid)
    roots.sort(key=lambda sid: by_id[sid]["timestamp"])

    # Use second-longest span for bar scale to avoid container spans (cli.session)
    durations = sorted((s["duration"] for s in spans), reverse=True)
    max_dur = durations[1] if len(durations) > 1 else durations[0] if durations else 1
    base_ts = min((s["timestamp"] for s in spans), default=0)

    agent_start = None
    for s in spans:
        if s["operation_name"] == "agent.run":
            agent_start = s["timestamp"]
            break
    if agent_start is None:
        agent_start = base_ts

    print(f"\n{'='*100}")
    print(f"Trace: {spans[0].get('trace_id', 'N/A') if spans else 'N/A'}")

    ops = Counter(s["operation_name"] for s in spans)
    print(f"Spans: {len(spans)} total  ({', '.join(f'{op}:{cnt}' for op, cnt in ops.most_common())})")

    if missing_parents:
        print(f"Missing parent spans: {missing_parents} (still running or not exported)")
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
        smry = span_summary(s)
        marker = slow_marker(dur)

        print(f"{offset:>7d}ms {dur:>6d}ms  {bar:<20s}  {indent}{op:<{28 - len(indent)}s}  {smry}{marker}")

        if not summary:
            _render_events(s, depth, agent_start, expand_progress)

        child_ids = children.get(sid, [])
        child_ids.sort(key=lambda cid: by_id[cid]["timestamp"])
        for cid in child_ids:
            print_node(cid, depth + 1)

    for rid in roots:
        print_node(rid)

    # === Bottleneck Analysis ===
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
            if "model.iteration" in t:
                extra += f"  iter={t['model.iteration']}"
            if "model.retries" in t:
                extra += f"  retries={t['model.retries']}"
        elif op == "agent.run":
            extra = f"  model={t.get('agent.model', '?')}"
            if "agent.iterations" in t:
                extra += f"  iters={t['agent.iterations']}"
            if "agent.stop_reason" in t:
                extra += f"  stop={t['agent.stop_reason']}"
        bar = duration_bar(dur, max_dur, 30)
        print(f"  #{i}  {dur:>6d}ms  {bar}  {op}{extra}")

    # === Idle/Gap Analysis ===
    gaps: list[tuple[str, str, int]] = []
    for sid, child_ids in children.items():
        if sid not in by_id:
            continue
        sorted_children = sorted(child_ids, key=lambda cid: by_id[cid]["timestamp"])
        for j in range(len(sorted_children) - 1):
            prev = by_id[sorted_children[j]]
            nxt = by_id[sorted_children[j + 1]]
            prev_end = prev["timestamp"] + prev["duration"]
            gap_ms = nxt["timestamp"] - prev_end
            if gap_ms > 10:
                prev_label = prev["operation_name"]
                prev_tags = tags_dict(prev)
                if "model.iteration" in prev_tags:
                    prev_label += f"[iter={prev_tags['model.iteration']}]"
                elif "tool.name" in prev_tags:
                    prev_label += f"[{prev_tags['tool.name']}]"
                nxt_label = nxt["operation_name"]
                nxt_tags = tags_dict(nxt)
                if "model.iteration" in nxt_tags:
                    nxt_label += f"[iter={nxt_tags['model.iteration']}]"
                elif "tool.name" in nxt_tags:
                    nxt_label += f"[{nxt_tags['tool.name']}]"
                gaps.append((prev_label, nxt_label, gap_ms))

    if gaps:
        print(f"\n{'='*100}")
        print("Idle/Gap Analysis (gaps > 10ms)")
        print(f"{'='*100}")
        for prev_label, nxt_label, gap_ms in sorted(gaps, key=lambda x: x[2], reverse=True):
            print(f"  {prev_label} → {nxt_label}: {gap_ms}ms")

    # === Token Summary ===
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
        if total_cache_r + total_cache_w > 0:
            hit_ratio = total_cache_r / (total_cache_r + total_cache_w) * 100
            print(f"  Cache hit ratio: {hit_ratio:.0f}%")

        # Cost estimation (¥ per 1M tokens)
        cost_table = {
            "qwen3.7-max": {"input": 2.0, "output": 8.0, "cache_read": 0.5, "cache_write": 2.0},
            "qwen-plus": {"input": 0.8, "output": 2.0, "cache_read": 0.2, "cache_write": 0.8},
            "qwen-max": {"input": 2.0, "output": 8.0, "cache_read": 0.5, "cache_write": 2.0},
            "qwen-turbo": {"input": 0.3, "output": 0.6, "cache_read": 0.075, "cache_write": 0.3},
        }
        model_names = set()
        for s in spans:
            if s["operation_name"] == "model.generate":
                t = tags_dict(s)
                if "model.name" in t:
                    model_names.add(t["model.name"])
        for mn in model_names:
            if mn in cost_table:
                c = cost_table[mn]
                cost_in = total_input / 1_000_000 * c["input"]
                cost_out = total_output / 1_000_000 * c["output"]
                cost_cr = total_cache_r / 1_000_000 * c["cache_read"]
                cost_cw = total_cache_w / 1_000_000 * c["cache_write"]
                total_cost = cost_in + cost_out + cost_cr + cost_cw
                print(f"  Estimated cost ({mn}): ¥{total_cost:.4f} (input=¥{cost_in:.4f}, output=¥{cost_out:.4f}, cache_r=¥{cost_cr:.4f}, cache_w=¥{cost_cw:.4f})")

    # === Agent Summary ===
    agent_spans = [s for s in spans if s["operation_name"] == "agent.run"]
    if agent_spans:
        print(f"\n  Agent runs: {len(agent_spans)}")
        for s in agent_spans:
            t = tags_dict(s)
            iters = t.get("agent.iterations", "?")
            stop = t.get("agent.stop_reason", "?")
            model_stop = t.get("agent.model_stop_reason", "")
            pt = t.get("agent.passthrough_tools", "")
            line = f"    {s['duration']:>6d}ms  iters={iters}  stop={stop}"
            if model_stop:
                line += f"  model_stop={model_stop}"
            if pt:
                line += f"  passthrough=[{pt}]"
            print(line)

    # === Agent Runs Comparison (multi-run) ===
    if len(agent_spans) > 1:
        print(f"\n{'='*100}")
        print("Agent Runs Comparison")
        print(f"{'='*100}")
        hdr = f"  {'#':>3s}  {'Duration':>10s}  {'Iters':>5s}  {'Stop':<18s}  {'Model':<20s}  {'Tokens(in/out)':>16s}"
        print(hdr)
        for idx, s in enumerate(agent_spans, 1):
            t = tags_dict(s)
            iters = t.get("agent.iterations", "?")
            stop = t.get("agent.stop_reason", "?")
            mdl = t.get("agent.model", "?")
            tok_in = t.get("agent.input_tokens", "0")
            tok_out = t.get("agent.output_tokens", "0")
            print(f"  {idx:>3d}  {s['duration']:>8d}ms  {iters:>5s}  {stop:<18s}  {mdl:<20s}  {tok_in:>7s}/{tok_out:<7s}")

    # === Retry/Fallback Events ===
    retry_events = []
    for s in spans:
        if not s["operation_name"].startswith("model."):
            continue
        for evt in s.get("log_event_list", []):
            evt_tags = {t["key"]: t["value"] for t in evt.get("tag_entry_list", [])}
            name = evt_tags.get("event", "")
            if name.startswith("model.") and name != "model.generate":
                retry_events.append((name, evt_tags))
    if retry_events:
        print(f"\n  Model events: {len(retry_events)}")
        for name, tags in retry_events:
            detail = ", ".join(f"{k}={v}" for k, v in tags.items() if k != "event")
            print(f"    {name}: {detail}")

    # === Tool Summary ===
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

    if args.tree or args.summary:
        render_tree(spans, summary=args.summary, expand_progress=args.expand_progress)
    else:
        result = {
            "trace_id": args.trace_id,
            "span_count": len(spans),
            "spans": spans,
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
