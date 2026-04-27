#!/usr/bin/env python3
"""End-to-end integration test for ALB skill scripts.

Creates real ALB resources, verifies via list/get APIs, then cleans up.

Flow:
  1. Create Server Group
  2. List Server Groups (verify)
  3. Add backend servers (dry-run, no real ECS)
  4. Create ALB instance
  5. List instances (verify)
  6. Get instance status (verify)
  7. Enable deletion protection
  8. Disable deletion protection
  9. Create HTTP listener (ForwardGroup → server group)
  10. List listeners (verify)
  11. Get listener attribute (verify)
  12. Create forwarding rule
  13. List rules (verify)
  14. Update rule
  15. Update listener
  16. Check health status
  17. Stop listener
  18. Start listener
  19. Delete rule
  20. Delete listener
  21. Delete ALB
  22. Delete server group
  23. Final list to confirm cleanup

Usage:
    export ALICLOUD_ACCESS_KEY_ID=xxx
    export ALICLOUD_ACCESS_KEY_SECRET=xxx
    python e2e_test_alb.py --region cn-chengdu --vpc-id vpc-xxx \\
        --zone1 cn-chengdu-a:vsw-aaa --zone2 cn-chengdu-b:vsw-bbb
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[5]
SCRIPTS_DIR = REPO_ROOT / "skills" / "network" / "slb" / "aliyun-alb-manage" / "scripts"
OUTPUT_DIR = REPO_ROOT / "output" / "aliyun-alb-manage-e2e"


class TestContext:
    """Holds resource IDs created during the test for cleanup."""

    def __init__(self, region: str):
        self.region = region
        self.server_group_id: str | None = None
        self.load_balancer_id: str | None = None
        self.listener_id: str | None = None
        self.rule_id: str | None = None

    def cleanup_order(self) -> list[tuple[str, str | None]]:
        """Return (resource_type, id) in correct deletion order."""
        return [
            ("rule", self.rule_id),
            ("listener", self.listener_id),
            ("load_balancer", self.load_balancer_id),
            ("server_group", self.server_group_id),
        ]


def run_script(script_name: str, args: list[str], label: str, timeout: int = 60) -> dict:
    """Run a skill script and return structured result."""
    script_path = SCRIPTS_DIR / script_name
    cmd = [sys.executable, str(script_path)] + args
    print(f"\n{'='*60}")
    print(f"[{label}] {script_name}")
    print(f"  cmd: python {script_name} {' '.join(args)}")

    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=timeout, cwd=str(REPO_ROOT),
        )
        out = result.stdout.strip()
        err = result.stderr.strip()
        passed = result.returncode == 0

        if out:
            # Truncate very long output
            display = out if len(out) < 2000 else out[:2000] + "\n... (truncated)"
            print(f"  stdout: {display}")
        if err:
            print(f"  stderr: {err[:500]}")
        print(f"  exit_code: {result.returncode}  {'PASS' if passed else 'FAIL'}")

        return {
            "test": label,
            "script": script_name,
            "exit_code": result.returncode,
            "stdout": out,
            "stderr": err,
            "passed": passed,
        }
    except subprocess.TimeoutExpired:
        print(f"  TIMEOUT ({timeout}s)")
        return {"test": label, "script": script_name, "exit_code": -1, "error": f"timeout ({timeout}s)", "passed": False}
    except Exception as e:
        print(f"  ERROR: {e}")
        return {"test": label, "script": script_name, "exit_code": -1, "error": str(e), "passed": False}


def extract_json_field(stdout: str, field: str) -> str | None:
    """Try to extract a field from JSON output."""
    try:
        data = json.loads(stdout)
        return data.get(field)
    except (json.JSONDecodeError, TypeError):
        pass
    # Try to find field in non-JSON output like "Server group created: sgp-xxx"
    for line in stdout.splitlines():
        if field.replace("_", " ") in line.lower() or field.replace("_", "") in line.lower():
            # Try to extract ID-like value
            parts = line.split()
            for part in parts:
                part = part.strip(".,;:()")
                if part.startswith(("sgp-", "alb-", "lsn-", "rule-", "job-")):
                    return part
    return None


def poll_status(
    script_name: str, script_args: list[str], label: str,
    check_fn, max_wait: int = 120, interval: int = 5,
) -> bool:
    """Poll a script's output until check_fn(stdout) returns True or timeout.

    Args:
        script_name: Script to run repeatedly.
        script_args: Arguments for the script.
        label: Display label for logging.
        check_fn: Callable(stdout: str) -> bool. Returns True when ready.
        max_wait: Maximum wait time in seconds.
        interval: Poll interval in seconds.
    """
    elapsed = 0
    while elapsed < max_wait:
        try:
            r = subprocess.run(
                [sys.executable, str(SCRIPTS_DIR / script_name)] + script_args,
                capture_output=True, text=True, timeout=30, cwd=str(REPO_ROOT),
            )
            if r.returncode == 0 and check_fn(r.stdout):
                print(f"  [{label}] Ready after {elapsed}s")
                return True
        except Exception:
            pass
        time.sleep(interval)
        elapsed += interval
        print(f"  [{label}] Waiting... ({elapsed}s)")
    print(f"  [{label}] Timeout after {max_wait}s")
    return False


def main() -> int:
    parser = argparse.ArgumentParser(description="E2E integration test for ALB skill")
    parser.add_argument("--region", required=True, help="Region ID, e.g. cn-chengdu")
    parser.add_argument("--vpc-id", required=True, help="Existing VPC ID")
    parser.add_argument("--zone1", required=True, help="zone_id:vswitch_id for zone 1")
    parser.add_argument("--zone2", required=True, help="zone_id:vswitch_id for zone 2")
    parser.add_argument("--output", default=str(OUTPUT_DIR / "e2e-result.json"), help="Output file")
    parser.add_argument("--skip-cleanup", action="store_true", help="Don't delete resources after test")

    args = parser.parse_args()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    ctx = TestContext(args.region)
    all_results: list[dict] = []
    region = args.region

    def step(script: str, script_args: list[str], label: str, timeout: int = 60) -> dict:
        r = run_script(script, script_args, label, timeout)
        all_results.append(r)
        return r

    def wait_job(result: dict, label: str, timeout: int = 120) -> dict:
        """Extract job_id from a step result and wait via wait_for_job.py."""
        job_id = extract_json_field(result.get("stdout", ""), "job_id")
        if not job_id or not result.get("passed"):
            return result
        r = run_script("wait_for_job.py", [
            "--region", region, "--job-id", job_id,
            "--timeout", str(timeout), "--json",
        ], f"wait_job:{label}", timeout=timeout + 10)
        all_results.append(r)
        return r

    # ========== PHASE 1: CREATE RESOURCES ==========
    print("\n" + "=" * 60)
    print("PHASE 1: CREATE RESOURCES")
    print("=" * 60)

    # 1. Create Server Group
    r = step("create_server_group.py", [
        "--region", region, "--name", "e2e-test-sg",
        "--vpc-id", args.vpc_id, "--protocol", "HTTP",
        "--scheduler", "Wrr",
        "--health-check-path", "/health",
        "--connection-drain-timeout", "0",
        "--json",
    ], "create_server_group")

    if r["passed"]:
        ctx.server_group_id = extract_json_field(r["stdout"], "server_group_id")
        print(f"  >>> server_group_id = {ctx.server_group_id}")

    if not ctx.server_group_id:
        print("\nFATAL: Failed to create server group. Cannot continue.")
        _write_results(args.output, all_results)
        return 1

    # 2. List server groups (verify)
    step("list_server_groups.py", [
        "--region", region, "--sg-ids", ctx.server_group_id, "--json",
    ], "list_server_groups_verify")

    # 3. Add servers (dry-run — we don't have real ECS instances)
    step("add_servers.py", [
        "--region", region, "--sg-id", ctx.server_group_id,
        "--server", "ecs:i-fake-test:8080:100:e2e-test",
        "--dry-run",
    ], "add_servers_dryrun")

    # 4. Remove servers (dry-run)
    step("remove_servers.py", [
        "--region", region, "--sg-id", ctx.server_group_id,
        "--server", "ecs:i-fake-test:8080",
        "--dry-run",
    ], "remove_servers_dryrun")

    # 5. List server group servers (should be empty)
    step("list_server_group_servers.py", [
        "--region", region, "--sg-id", ctx.server_group_id,
    ], "list_server_group_servers_empty")

    # 6. Create ALB instance
    r = step("create_load_balancer.py", [
        "--region", region, "--name", "e2e-test-alb",
        "--vpc-id", args.vpc_id, "--address-type", "Intranet",
        "--edition", "Standard",
        "--zone", args.zone1, "--zone", args.zone2,
        "--json",
    ], "create_load_balancer", timeout=120)

    if r["passed"]:
        ctx.load_balancer_id = extract_json_field(r["stdout"], "load_balancer_id")
        print(f"  >>> load_balancer_id = {ctx.load_balancer_id}")

    if not ctx.load_balancer_id:
        print("\nFATAL: Failed to create ALB. Cleaning up...")
        _cleanup(ctx, region, args.skip_cleanup, all_results)
        _write_results(args.output, all_results)
        return 1

    # 7. Wait for ALB to become Active (poll via get_instance_status.py)
    #    CreateLoadBalancer doesn't return a job_id, so we poll the resource status directly.
    print(f"\n  Waiting for ALB {ctx.load_balancer_id} to become Active...")
    alb_ready = poll_status(
        "get_instance_status.py",
        ["--region", region, "--lb-id", ctx.load_balancer_id, "--view", "detail"],
        "ALB Active",
        check_fn=lambda stdout: '"Active"' in stdout,
        max_wait=180, interval=5,
    )
    all_results.append({"test": "wait_alb_active", "passed": alb_ready})

    if not alb_ready:
        print("\nWARNING: ALB not yet Active, continuing anyway...")

    # ========== PHASE 2: VERIFY & INSPECT ==========
    print("\n" + "=" * 60)
    print("PHASE 2: VERIFY & INSPECT")
    print("=" * 60)

    # 8. List instances (verify)
    step("list_instances.py", [
        "--region", region, "--lb-ids", ctx.load_balancer_id, "--json",
    ], "list_instances_verify")

    # 9. Get instance status (tree view)
    step("get_instance_status.py", [
        "--region", region, "--lb-id", ctx.load_balancer_id,
    ], "get_instance_status_tree")

    # 10. Get instance status (detail JSON)
    step("get_instance_status.py", [
        "--region", region, "--lb-id", ctx.load_balancer_id, "--view", "detail",
    ], "get_instance_status_detail")

    # 11. Enable deletion protection
    #     ALB may still be internally provisioning after reaching Active status.
    #     Retry with backoff if it fails due to IncorrectStatus.
    r = step("deletion_protection.py", [
        "--region", region, "--resource-id", ctx.load_balancer_id, "--enable",
    ], "enable_deletion_protection")

    if not r["passed"] and "IncorrectStatus" in r.get("stderr", ""):
        print("  ALB still provisioning, waiting 15s and retrying...")
        time.sleep(15)
        r = step("deletion_protection.py", [
            "--region", region, "--resource-id", ctx.load_balancer_id, "--enable",
        ], "enable_deletion_protection_retry")

    # 12. Disable deletion protection
    step("deletion_protection.py", [
        "--region", region, "--resource-id", ctx.load_balancer_id, "--disable",
    ], "disable_deletion_protection")

    # ========== PHASE 3: LISTENER & RULE ==========
    print("\n" + "=" * 60)
    print("PHASE 3: LISTENER & RULE")
    print("=" * 60)

    # 13. Create HTTP listener
    r = step("create_listener.py", [
        "--region", region, "--lb-id", ctx.load_balancer_id,
        "--protocol", "HTTP", "--port", "80",
        "--action-type", "ForwardGroup",
        "--forward-server-groups", ctx.server_group_id,
        "--description", "e2e-test-listener",
        "--json",
    ], "create_listener")

    if r["passed"]:
        ctx.listener_id = extract_json_field(r["stdout"], "listener_id")
        print(f"  >>> listener_id = {ctx.listener_id}")

    if not ctx.listener_id:
        print("\nFATAL: Failed to create listener. Cleaning up...")
        _cleanup(ctx, region, args.skip_cleanup, all_results)
        _write_results(args.output, all_results)
        return 1

    # 14. Wait for create_listener job to complete
    wait_job(r, "create_listener")

    # 15. List listeners (verify)
    step("list_listeners.py", [
        "--region", region, "--lb-id", ctx.load_balancer_id, "--json",
    ], "list_listeners_verify")

    # 16. Get listener attribute
    step("get_listener_attribute.py", [
        "--region", region, "--listener-id", ctx.listener_id,
    ], "get_listener_attribute")

    # 17. Create forwarding rule (Path condition — straightforward for all editions)
    r = step("create_rule.py", [
        "--region", region, "--listener-id", ctx.listener_id,
        "--name", "e2e-test-rule", "--priority", "10",
        "--condition-path", "/api/*",
        "--action-forward-to", ctx.server_group_id,
        "--json",
    ], "create_rule")

    if r["passed"]:
        ctx.rule_id = extract_json_field(r["stdout"], "rule_id")
        print(f"  >>> rule_id = {ctx.rule_id}")

    if ctx.rule_id:
        wait_job(r, "create_rule")

    # 18. List rules (verify)
    step("list_rules.py", [
        "--region", region, "--listener-id", ctx.listener_id, "--json",
    ], "list_rules_verify")

    # ========== PHASE 4: UPDATE OPERATIONS ==========
    print("\n" + "=" * 60)
    print("PHASE 4: UPDATE OPERATIONS")
    print("=" * 60)

    # 19. Update rule (change name and priority)
    if ctx.rule_id:
        r = step("update_rule.py", [
            "--region", region, "--rule-id", ctx.rule_id,
            "--name", "e2e-test-rule-updated", "--priority", "20",
            "--json",
        ], "update_rule")
        wait_job(r, "update_rule")

    # 20. Update listener
    r = step("update_listener.py", [
        "--region", region, "--listener-id", ctx.listener_id,
        "--description", "e2e-test-listener-updated",
        "--idle-timeout", "30",
        "--request-timeout", "60",
        "--json",
    ], "update_listener")
    wait_job(r, "update_listener")

    # ========== PHASE 5: HEALTH CHECK & LISTENER OPS ==========
    print("\n" + "=" * 60)
    print("PHASE 5: HEALTH CHECK & LISTENER OPS")
    print("=" * 60)

    # 21. Check health status
    step("check_health_status.py", [
        "--region", region, "--lb-id", ctx.load_balancer_id, "--json",
    ], "check_health_status")

    # 22. List security policies
    step("list_security_policies.py", [
        "--region", region, "--system",
    ], "list_security_policies")

    # 23. List ACLs
    step("list_acls.py", [
        "--region", region, "--json",
    ], "list_acls")

    # 24. Stop listener
    r = step("stop_listener.py", [
        "--region", region, "--listener-id", ctx.listener_id, "--json",
    ], "stop_listener")
    wait_job(r, "stop_listener")

    # 25. Start listener
    r = step("start_listener.py", [
        "--region", region, "--listener-id", ctx.listener_id, "--json",
    ], "start_listener")
    wait_job(r, "start_listener")

    # ========== PHASE 6: CLEANUP (reverse order) ==========
    if not args.skip_cleanup:
        print("\n" + "=" * 60)
        print("PHASE 6: CLEANUP (reverse order)")
        print("=" * 60)
        _cleanup(ctx, region, False, all_results)
    else:
        print("\n  --skip-cleanup: Resources left alive for inspection:")
        print(f"    ALB: {ctx.load_balancer_id}")
        print(f"    Listener: {ctx.listener_id}")
        print(f"    Rule: {ctx.rule_id}")
        print(f"    Server Group: {ctx.server_group_id}")

    # ========== SUMMARY ==========
    _write_results(args.output, all_results)

    passed = sum(1 for r in all_results if r.get("passed"))
    failed = sum(1 for r in all_results if not r.get("passed"))
    total = len(all_results)

    print("\n" + "=" * 60)
    print(f"SUMMARY: {passed}/{total} passed, {failed} failed")
    print("=" * 60)

    if failed > 0:
        print("\nFailed tests:")
        for r in all_results:
            if not r.get("passed"):
                err = r.get("error") or r.get("stderr", "")[:200] or "unknown"
                print(f"  - {r['test']}: {err}")

    return 0 if failed == 0 else 1


def _cleanup(ctx: TestContext, region: str, skip: bool, results: list[dict]):
    """Clean up resources in reverse dependency order."""
    if skip:
        return

    def cleanup_step(script: str, script_args: list[str], label: str) -> dict:
        r = run_script(script, script_args, label, timeout=60)
        results.append(r)
        return r

    def cleanup_wait_job(result: dict, label: str, timeout: int = 120):
        """Wait for cleanup job via wait_for_job.py."""
        job_id = extract_json_field(result.get("stdout", ""), "job_id")
        if not job_id or not result.get("passed"):
            return
        r = run_script("wait_for_job.py", [
            "--region", region, "--job-id", job_id,
            "--timeout", str(timeout), "--json",
        ], f"wait_job:{label}", timeout=timeout + 10)
        results.append(r)

    # 1. Delete rule (wait for listener to reach stable state first)
    if ctx.rule_id:
        if ctx.listener_id:
            print("  Waiting for listener to settle before deleting rule...")
            poll_status(
                "get_listener_attribute.py",
                ["--region", region, "--listener-id", ctx.listener_id],
                "Listener Ready",
                check_fn=lambda stdout: "Running" in stdout or "Stopped" in stdout,
                max_wait=60, interval=3,
            )

        r = cleanup_step("delete_rule.py", [
            "--region", region, "--rule-id", ctx.rule_id, "--yes", "--json",
        ], "cleanup_delete_rule")
        cleanup_wait_job(r, "delete_rule")

    # 2. Delete listener
    if ctx.listener_id:
        r = cleanup_step("delete_listener.py", [
            "--region", region, "--listener-id", ctx.listener_id, "--yes", "--json",
        ], "cleanup_delete_listener")
        cleanup_wait_job(r, "delete_listener")

    # 3. Delete ALB (disable deletion protection first just in case)
    if ctx.load_balancer_id:
        run_script("deletion_protection.py", [
            "--region", region, "--resource-id", ctx.load_balancer_id, "--disable",
        ], "cleanup_disable_deletion_protection")

        r = cleanup_step("delete_load_balancer.py", [
            "--region", region, "--lb-id", ctx.load_balancer_id, "--yes", "--json",
        ], "cleanup_delete_load_balancer")
        cleanup_wait_job(r, "delete_load_balancer")

    # 4. Delete server group
    if ctx.server_group_id:
        r = cleanup_step("delete_server_group.py", [
            "--region", region, "--sg-id", ctx.server_group_id, "--yes", "--json",
        ], "cleanup_delete_server_group")
        cleanup_wait_job(r, "delete_server_group")

    # 5. Final verification: list instances to confirm cleanup
    r = run_script("list_instances.py", [
        "--region", region, "--json",
    ], "final_list_instances")
    results.append(r)


def _write_results(output_path: str, results: list[dict]):
    """Write test results to file."""
    passed = sum(1 for r in results if r.get("passed"))
    failed = sum(1 for r in results if not r.get("passed"))

    # Strip stdout from results to keep file manageable
    clean_results = []
    for r in results:
        cr = {k: v for k, v in r.items() if k != "stdout"}
        if "stdout" in r and r["stdout"]:
            cr["stdout_lines"] = len(r["stdout"].splitlines())
        clean_results.append(cr)

    summary = {
        "status": "pass" if failed == 0 else "fail",
        "total": len(results),
        "passed": passed,
        "failed": failed,
        "results": clean_results,
    }

    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nResults written to {output_path}")


if __name__ == "__main__":
    raise SystemExit(main())
