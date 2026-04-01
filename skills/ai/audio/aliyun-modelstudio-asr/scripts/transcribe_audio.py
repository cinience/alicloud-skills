#!/usr/bin/env python3
"""Transcribe audio with DashScope Qwen ASR (non-realtime).

Examples:
  python scripts/transcribe_audio.py --audio https://example.com/a.wav --model qwen3-asr-flash --print-response
  python scripts/transcribe_audio.py --audio ./local.wav --model qwen3-asr-flash-filetrans --async --wait
"""

from __future__ import annotations

import argparse
import base64
import configparser
import json
import mimetypes
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any


ASR_SYNC_ENDPOINT = "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions"
ASR_FILETRANS_ENDPOINT = "https://dashscope.aliyuncs.com/api/v1/services/audio/asr/transcription"
TASK_ENDPOINT_PREFIX = "https://dashscope.aliyuncs.com/api/v1/tasks/"


def _find_repo_root(start: Path) -> Path | None:
    for parent in [start] + list(start.parents):
        if (parent / ".git").exists():
            return parent
    return None


def _load_dotenv(path: Path) -> None:
    if not path.exists():
        return
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


def _load_env() -> None:
    _load_dotenv(Path.cwd() / ".env")
    repo_root = _find_repo_root(Path(__file__).resolve())
    if repo_root:
        _load_dotenv(repo_root / ".env")


def _load_dashscope_api_key_from_credentials() -> None:
    if os.environ.get("DASHSCOPE_API_KEY"):
        return
    credentials_path = Path(os.path.expanduser("~/.alibabacloud/credentials"))
    if not credentials_path.exists():
        return
    config = configparser.ConfigParser()
    try:
        config.read(credentials_path)
    except configparser.Error:
        return
    profile = os.getenv("ALIBABA_CLOUD_PROFILE") or os.getenv("ALICLOUD_PROFILE") or "default"
    if not config.has_section(profile):
        return
    key = config.get(profile, "dashscope_api_key", fallback="").strip()
    if not key:
        key = config.get(profile, "DASHSCOPE_API_KEY", fallback="").strip()
    if key:
        os.environ["DASHSCOPE_API_KEY"] = key


def _http_json(
    method: str,
    url: str,
    api_key: str,
    payload: dict[str, Any] | None = None,
    async_enable: bool = False,
) -> dict[str, Any]:
    body = None if payload is None else json.dumps(payload, ensure_ascii=True).encode("utf-8")
    req = urllib.request.Request(url=url, data=body, method=method)
    req.add_header("Authorization", f"Bearer {api_key}")
    req.add_header("Content-Type", "application/json")
    if async_enable:
        req.add_header("X-DashScope-Async", "enable")

    try:
        with urllib.request.urlopen(req, timeout=180) as resp:
            raw = resp.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="ignore")
        raise RuntimeError(f"HTTP {exc.code}: {detail}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Request failed: {exc}") from exc

    try:
        return json.loads(raw)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Invalid JSON response: {raw[:500]}") from exc


def _is_url(value: str) -> bool:
    parsed = urllib.parse.urlparse(value)
    return parsed.scheme in {"http", "https"}


def _make_data_uri(path: Path) -> str:
    mime = mimetypes.guess_type(path.name)[0] or "audio/wav"
    b64 = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{b64}"


def _build_sync_payload(args: argparse.Namespace) -> dict[str, Any]:
    if _is_url(args.audio):
        audio_data = args.audio
    else:
        path = Path(args.audio)
        if not path.exists():
            raise ValueError(f"audio file not found: {args.audio}")
        audio_data = _make_data_uri(path)

    payload: dict[str, Any] = {
        "model": args.model,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_audio",
                        "input_audio": {"data": audio_data},
                    }
                ],
            }
        ],
        "stream": False,
    }

    asr_options: dict[str, Any] = {}
    if args.language_hints:
        asr_options["language_hints"] = [s.strip() for s in args.language_hints.split(",") if s.strip()]
    if args.sample_rate:
        asr_options["sample_rate"] = args.sample_rate
    if args.vocabulary_id:
        asr_options["vocabulary_id"] = args.vocabulary_id
    if args.disfluency_removal_enabled:
        asr_options["disfluency_removal_enabled"] = True
    if args.timestamp_granularities:
        asr_options["timestamp_granularities"] = [
            s.strip() for s in args.timestamp_granularities.split(",") if s.strip()
        ]
    if asr_options:
        payload["asr_options"] = asr_options

    return payload


def _build_filetrans_payload(args: argparse.Namespace) -> dict[str, Any]:
    if _is_url(args.audio):
        return {"model": args.model, "input": {"file_url": args.audio}}

    path = Path(args.audio)
    if not path.exists():
        raise ValueError(f"audio file not found: {args.audio}")

    # Prefer data URI fallback when no public URL is available.
    return {"model": args.model, "input_audio": {"data": _make_data_uri(path)}}


def _extract_text(obj: Any) -> str:
    if isinstance(obj, dict):
        choices = obj.get("choices")
        if isinstance(choices, list) and choices:
            first = choices[0]
            if isinstance(first, dict):
                msg = first.get("message")
                if isinstance(msg, dict):
                    content = msg.get("content")
                    if isinstance(content, str) and content.strip():
                        return content

        output = obj.get("output")
        if isinstance(output, dict):
            transcription = output.get("transcription")
            if isinstance(transcription, dict) and isinstance(transcription.get("text"), str):
                return transcription["text"]
            results = output.get("results")
            if isinstance(results, list):
                texts = []
                for item in results:
                    if isinstance(item, dict):
                        t = item.get("transcription")
                        if isinstance(t, dict) and isinstance(t.get("text"), str):
                            texts.append(t["text"])
                if texts:
                    return "\n".join(texts)

        texts: list[str] = []
        for v in obj.values():
            t = _extract_text(v)
            if t:
                texts.append(t)
        return "\n".join(texts)

    if isinstance(obj, list):
        texts = [_extract_text(v) for v in obj]
        texts = [t for t in texts if t]
        return "\n".join(texts)

    return obj if isinstance(obj, str) else ""


def _default_async(model: str) -> bool:
    return model == "qwen3-asr-flash-filetrans"


def _fetch_json_url(url: str) -> dict[str, Any]:
    try:
        with urllib.request.urlopen(url, timeout=180) as resp:
            raw = resp.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="ignore")
        raise RuntimeError(f"Transcription URL HTTP {exc.code}: {detail}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Transcription URL request failed: {exc}") from exc

    try:
        return json.loads(raw)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Invalid transcription JSON: {raw[:500]}") from exc


def _normalize_text(resp: dict[str, Any]) -> str:
    choices = resp.get("choices")
    if isinstance(choices, list) and choices:
        first = choices[0]
        if isinstance(first, dict):
            msg = first.get("message")
            if isinstance(msg, dict):
                content = msg.get("content")
                if isinstance(content, str) and content.strip():
                    return content.strip()

    transcription_result = resp.get("transcription_result")
    if isinstance(transcription_result, dict):
        transcripts = transcription_result.get("transcripts")
        if isinstance(transcripts, list):
            texts: list[str] = []
            for item in transcripts:
                if isinstance(item, dict):
                    t = item.get("text")
                    if isinstance(t, str) and t.strip():
                        texts.append(t.strip())
            if texts:
                return "\n".join(texts)

    return _extract_text(resp).strip()


def _poll_task(api_key: str, task_id: str, interval: float, max_waits: int) -> dict[str, Any]:
    for _ in range(max_waits):
        resp = _http_json("GET", TASK_ENDPOINT_PREFIX + task_id, api_key)
        status = ((resp.get("output") or {}).get("task_status") or "").upper()
        if status in {"SUCCEEDED", "FAILED", "CANCELED"}:
            return resp
        time.sleep(interval)
    raise RuntimeError(f"task {task_id} not finished after {max_waits} polls")


def main() -> None:
    parser = argparse.ArgumentParser(description="Transcribe audio with Qwen ASR (non-realtime)")
    parser.add_argument("--audio", required=True, help="Audio URL or local audio file path")
    parser.add_argument("--model", default="qwen3-asr-flash", help="ASR model name")
    parser.add_argument("--language-hints", help="Comma-separated language hints, e.g. zh,en")
    parser.add_argument("--sample-rate", type=int, help="Sample rate")
    parser.add_argument("--vocabulary-id", help="Vocabulary ID")
    parser.add_argument(
        "--disfluency-removal-enabled",
        action="store_true",
        help="Enable disfluency removal",
    )
    parser.add_argument(
        "--timestamp-granularities",
        help="Comma-separated timestamps, e.g. sentence,word",
    )
    parser.add_argument("--async", dest="async_mode", action="store_true", help="Force async mode")
    parser.add_argument("--wait", action="store_true", help="When async, poll until terminal state")
    parser.add_argument("--poll-interval", type=float, default=8.0, help="Polling interval seconds")
    parser.add_argument("--max-waits", type=int, default=45, help="Max polling count")
    parser.add_argument("--output", help="Output JSON file path")
    parser.add_argument("--print-response", action="store_true", help="Print normalized response")
    args = parser.parse_args()

    _load_env()
    _load_dashscope_api_key_from_credentials()

    api_key = os.getenv("DASHSCOPE_API_KEY")
    if not api_key:
        print(
            "Error: DASHSCOPE_API_KEY is not set. Configure it via env/.env or ~/.alibabacloud/credentials.",
            file=sys.stderr,
        )
        sys.exit(1)

    async_mode = args.async_mode or _default_async(args.model)
    if async_mode:
        payload = _build_filetrans_payload(args)
        submit_resp = _http_json(
            "POST",
            ASR_FILETRANS_ENDPOINT,
            api_key,
            payload,
            async_enable=True,
        )
    else:
        payload = _build_sync_payload(args)
        submit_resp = _http_json("POST", ASR_SYNC_ENDPOINT, api_key, payload, async_enable=False)

    final_resp = submit_resp
    status = ((submit_resp.get("output") or {}).get("task_status") or "")
    task_id = ((submit_resp.get("output") or {}).get("task_id") or (submit_resp.get("task_id") or ""))

    if async_mode and args.wait and task_id:
        final_resp = _poll_task(api_key, task_id, args.poll_interval, args.max_waits)
        status = ((final_resp.get("output") or {}).get("task_status") or status)

    if async_mode and status.upper() == "SUCCEEDED":
        transcription_url = (((final_resp.get("output") or {}).get("result") or {}).get("transcription_url") or "")
        if isinstance(transcription_url, str) and transcription_url:
            transcription_json = _fetch_json_url(transcription_url)
            final_resp["transcription_result"] = transcription_json

    normalized = {
        "text": _normalize_text(final_resp),
        "task_id": task_id or None,
        "status": status or "SUCCEEDED",
        "raw": final_resp,
    }

    output_path = Path(
        args.output
        or (
            Path(os.getenv("OUTPUT_DIR", "output"))
            / "ai-audio-asr"
            / "transcripts"
            / "result.json"
        )
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(normalized, ensure_ascii=False, indent=2), encoding="utf-8")

    if args.print_response:
        print(json.dumps(normalized, ensure_ascii=True))


if __name__ == "__main__":
    main()
