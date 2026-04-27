#!/usr/bin/env python3
"""Executable smoke test for aliyun-alb-manage skill."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[5]
SKILL_DIR = REPO_ROOT / "skills" / "network" / "slb" / "aliyun-alb-manage"
SCRIPTS_DIR = SKILL_DIR / "scripts"
OUTPUT_DIR = REPO_ROOT / "output" / "aliyun-alb-manage-test"


def run_script(script_name: str, args: list[str], label: str) -> dict:
    """Run a skill script and return structured result."""
    script_path = SCRIPTS_DIR / script_name
    cmd = [sys.executable, str(script_path)] + args
    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=30, cwd=str(REPO_ROOT),
        )
        return {
            "test": label,
            "script": script_name,
            "exit_code": result.returncode,
            "stdout_lines": len(result.stdout.strip().splitlines()) if result.stdout.strip() else 0,
            "stderr_preview": result.stderr.strip()[:200] if result.stderr.strip() else "",
            "passed": result.returncode == 0,
        }
    except subprocess.TimeoutExpired:
        return {
            "test": label,
            "script": script_name,
            "exit_code": -1,
            "error": "timeout (30s)",
            "passed": False,
        }
    except Exception as e:
        return {
            "test": label,
            "script": script_name,
            "exit_code": -1,
            "error": str(e),
            "passed": False,
        }


def test_compile_all() -> list[dict]:
    """Test that all scripts compile without errors."""
    results = []
    scripts = sorted(SCRIPTS_DIR.glob("*.py"))
    for script in scripts:
        try:
            subprocess.run(
                [sys.executable, "-m", "py_compile", str(script)],
                capture_output=True, text=True, check=True,
            )
            results.append({
                "test": f"compile:{script.name}",
                "passed": True,
            })
        except subprocess.CalledProcessError as e:
            results.append({
                "test": f"compile:{script.name}",
                "passed": False,
                "error": e.stderr.strip()[:200],
            })
    return results


def test_sdk_import() -> dict:
    """Test that the ALB SDK is importable."""
    try:
        subprocess.run(
            [sys.executable, "-c",
             "from alibabacloud_alb20200616 import models; "
             "from alibabacloud_tea_openapi import models as m; "
             "print('import_ok')"],
            capture_output=True, text=True, check=True,
        )
        return {"test": "sdk_import", "passed": True}
    except subprocess.CalledProcessError as e:
        return {"test": "sdk_import", "passed": False, "error": e.stderr.strip()[:200]}


def test_list_operations(region: str) -> list[dict]:
    """Test read-only list operations that work even with empty accounts."""
    results = []
    output_file = str(OUTPUT_DIR / "list_instances.json")
    results.append(run_script(
        "list_instances.py",
        ["--region", region, "--json", "--output", output_file],
        "list_instances",
    ))
    results.append(run_script(
        "list_server_groups.py",
        ["--region", region, "--json", "--output", str(OUTPUT_DIR / "list_server_groups.json")],
        "list_server_groups",
    ))
    results.append(run_script(
        "list_acls.py",
        ["--region", region, "--json", "--output", str(OUTPUT_DIR / "list_acls.json")],
        "list_acls",
    ))
    results.append(run_script(
        "list_security_policies.py",
        ["--region", region, "--output", str(OUTPUT_DIR / "list_security_policies.txt")],
        "list_security_policies",
    ))
    return results


def test_instance_operations(region: str, lb_id: str) -> list[dict]:
    """Test instance-specific operations (requires a real ALB)."""
    results = []
    results.append(run_script(
        "get_instance_status.py",
        ["--region", region, "--lb-id", lb_id,
         "--output", str(OUTPUT_DIR / "instance_overview.txt")],
        "get_instance_status_overview",
    ))
    results.append(run_script(
        "get_instance_status.py",
        ["--region", region, "--lb-id", lb_id, "--view", "detail",
         "--output", str(OUTPUT_DIR / "instance_detail.json")],
        "get_instance_status_detail",
    ))
    results.append(run_script(
        "list_listeners.py",
        ["--region", region, "--lb-id", lb_id, "--json",
         "--output", str(OUTPUT_DIR / "list_listeners.json")],
        "list_listeners",
    ))
    results.append(run_script(
        "list_rules.py",
        ["--region", region, "--lb-id", lb_id, "--json",
         "--output", str(OUTPUT_DIR / "list_rules.json")],
        "list_rules",
    ))
    results.append(run_script(
        "check_health_status.py",
        ["--region", region, "--lb-id", lb_id, "--json",
         "--output", str(OUTPUT_DIR / "health_status.json")],
        "check_health_status",
    ))
    return results


def main() -> None:
    parser = argparse.ArgumentParser(description="Smoke test for ALB skill")
    parser.add_argument("--region", help="Region ID for API tests, e.g. cn-hangzhou")
    parser.add_argument("--lb-id", help="ALB instance ID for instance-specific tests")
    parser.add_argument(
        "--compile-only", action="store_true",
        help="Only check script compilation and SDK import (no credentials needed)",
    )
    parser.add_argument(
        "--output",
        default=str(OUTPUT_DIR / "smoke-test-result.json"),
        help="Path to save test result JSON",
    )
    args = parser.parse_args()

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    all_results: list[dict] = []

    # Phase 1: Compile + import checks (always run)
    all_results.extend(test_compile_all())
    all_results.append(test_sdk_import())

    if not args.compile_only:
        if not args.region:
            print("Error: --region is required for API tests (or use --compile-only)")
            sys.exit(1)

        # Phase 2: List operations (work even with empty accounts)
        all_results.extend(test_list_operations(args.region))

        # Phase 3: Instance-specific tests (optional)
        if args.lb_id:
            all_results.extend(test_instance_operations(args.region, args.lb_id))

    passed = sum(1 for r in all_results if r.get("passed"))
    failed = sum(1 for r in all_results if not r.get("passed"))
    overall = "pass" if failed == 0 else "fail"

    summary = {
        "status": overall,
        "total": len(all_results),
        "passed": passed,
        "failed": failed,
        "results": all_results,
    }

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8",
    )

    # Print summary
    print(json.dumps({"status": overall, "passed": passed, "failed": failed}, ensure_ascii=False))

    if failed > 0:
        print("\nFailed tests:")
        for r in all_results:
            if not r.get("passed"):
                err = r.get("error") or r.get("stderr_preview") or ""
                print(f"  - {r['test']}: {err}")

    sys.exit(0 if overall == "pass" else 1)


if __name__ == "__main__":
    main()
