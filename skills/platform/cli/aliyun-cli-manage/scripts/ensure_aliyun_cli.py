#!/usr/bin/env python3
import argparse
import json
import os
import re
import shutil
import stat
import subprocess
import tarfile
import tempfile
import time
import urllib.request
from pathlib import Path


DOWNLOAD_URL = "https://aliyuncli.alicdn.com/aliyun-cli-linux-latest-amd64.tgz"


def parse_bool(v: str | None, default: bool = False) -> bool:
    if v is None:
        return default
    return v.strip().lower() in {"1", "true", "yes", "y", "on"}


def parse_version(text: str) -> tuple[int, ...]:
    m = re.search(r"(\d+\.\d+\.\d+)", text)
    if not m:
        return tuple()
    return tuple(int(x) for x in m.group(1).split("."))


def version_string(v: tuple[int, ...]) -> str:
    if not v:
        return "unknown"
    return ".".join(str(x) for x in v)


def run_version(binary: Path) -> tuple[tuple[int, ...], str]:
    try:
        out = subprocess.check_output([str(binary), "version"], text=True, stderr=subprocess.STDOUT)
    except Exception:
        return tuple(), ""
    return parse_version(out), out.strip()


def load_state(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def save_state(path: Path, state: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


def install_latest(target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="aliyun-cli-update-") as td:
        td_path = Path(td)
        tgz_path = td_path / "aliyun-cli.tgz"
        with urllib.request.urlopen(DOWNLOAD_URL, timeout=30) as resp:  # nosec B310
            tgz_path.write_bytes(resp.read())
        with tarfile.open(tgz_path, "r:gz") as tf:
            member = None
            for m in tf.getmembers():
                if Path(m.name).name == "aliyun":
                    member = m
                    break
            if member is None:
                raise RuntimeError("aliyun binary not found in archive")
            tf.extract(member, path=td_path)
            extracted = td_path / member.name
            if not extracted.exists():
                raise RuntimeError("extracted aliyun binary missing")
            shutil.copy2(extracted, target)
    mode = target.stat().st_mode
    target.chmod(mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Ensure aliyun CLI is installed and periodically updated")
    p.add_argument("--interval-hours", type=float, default=None, help="check interval in hours (default from env or 24)")
    p.add_argument("--min-version", default=None, help="minimum acceptable version, e.g. 3.2.9")
    p.add_argument("--install-dir", default=None, help="install directory (default: ~/.local/bin)")
    p.add_argument("--binary-path", default=None, help="explicit aliyun binary path")
    p.add_argument("--state-file", default=None, help="state file path")
    p.add_argument("--force", action="store_true", help="force update now")
    return p


def main() -> int:
    args = build_parser().parse_args()
    interval_hours = args.interval_hours
    if interval_hours is None:
        interval_hours = float(os.getenv("ALIYUN_CLI_CHECK_INTERVAL_HOURS", "24"))
    force = args.force or parse_bool(os.getenv("ALIYUN_CLI_FORCE_UPDATE"))
    min_version_str = args.min_version or os.getenv("ALIYUN_CLI_MIN_VERSION", "").strip()
    min_version = parse_version(min_version_str) if min_version_str else tuple()

    install_dir = Path(args.install_dir or os.getenv("ALIYUN_CLI_INSTALL_DIR", str(Path.home() / ".local/bin"))).expanduser()
    default_state = Path.home() / ".cache/aliyun-cli-manage/state.json"
    state_file = Path(args.state_file).expanduser() if args.state_file else default_state

    if args.binary_path:
        target = Path(args.binary_path).expanduser()
    else:
        in_path = shutil.which("aliyun")
        if in_path and os.access(in_path, os.W_OK):
            target = Path(in_path)
        else:
            target = install_dir / "aliyun"

    state = load_state(state_file)
    now = int(time.time())
    last_check = int(state.get("last_check_epoch", 0) or 0)
    due_by_interval = last_check <= 0 or (now - last_check) >= int(interval_hours * 3600)
    exists = target.exists()
    current_version, raw_version = run_version(target) if exists else (tuple(), "")
    below_min = bool(min_version and (not current_version or current_version < min_version))
    should_update = force or (not exists) or due_by_interval or below_min

    print(f"[aliyun-cli] target={target}")
    print(f"[aliyun-cli] current_version={version_string(current_version)}")
    if min_version:
        print(f"[aliyun-cli] min_version={version_string(min_version)}")
    print(f"[aliyun-cli] last_check_epoch={last_check} interval_hours={interval_hours}")

    updated = False
    if should_update:
        print("[aliyun-cli] updating from official latest package...")
        install_latest(target)
        updated = True
        current_version, raw_version = run_version(target)
        print(f"[aliyun-cli] updated_version={version_string(current_version)}")
    else:
        print("[aliyun-cli] skip update (within interval and version acceptable)")

    state.update(
        {
            "last_check_epoch": now,
            "binary_path": str(target),
            "version": version_string(current_version),
            "updated": updated,
            "raw_version": raw_version,
        }
    )
    save_state(state_file, state)
    print(f"[aliyun-cli] state_file={state_file}")
    if min_version and current_version and current_version < min_version:
        print("[aliyun-cli] error: installed version is lower than required minimum")
        return 2
    if not current_version:
        print("[aliyun-cli] error: unable to detect aliyun version after ensure")
        return 3
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

