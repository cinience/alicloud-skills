#!/usr/bin/env python3
"""List ALB custom and system security policies (TLS versions & cipher suites)."""

from __future__ import annotations

import argparse
import json
import os

from alibabacloud_alb20200616.client import Client as Alb20200616Client
from alibabacloud_alb20200616 import models as alb_models
from alibabacloud_tea_openapi import models as open_api_models


def create_client(region_id: str) -> Alb20200616Client:
    config = open_api_models.Config(
        region_id=region_id,
        endpoint=f"alb.{region_id}.aliyuncs.com",
    )
    ak = os.getenv("ALICLOUD_ACCESS_KEY_ID") or os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID")
    sk = os.getenv("ALICLOUD_ACCESS_KEY_SECRET") or os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET")
    token = os.getenv("ALICLOUD_SECURITY_TOKEN") or os.getenv("ALIBABA_CLOUD_SECURITY_TOKEN")
    if not ak or not sk:
        raise RuntimeError("ALICLOUD_ACCESS_KEY_ID and ALICLOUD_ACCESS_KEY_SECRET must be set")
    config.access_key_id = ak
    config.access_key_secret = sk
    if token:
        config.security_token = token
    return Alb20200616Client(config)


def iter_custom_policies(client: Alb20200616Client):
    """Yield all custom security policies."""
    next_token: str | None = None
    while True:
        req = alb_models.ListSecurityPoliciesRequest(
            max_results=100,
            next_token=next_token,
        )
        resp = client.list_security_policies(req)
        for sp in resp.body.security_policies or []:
            yield sp
        next_token = resp.body.next_token
        if not next_token:
            break


def main() -> int:
    parser = argparse.ArgumentParser(description="List ALB security policies")
    parser.add_argument("--region", required=True, help="Region ID")
    parser.add_argument("--system", action="store_true",
                        help="Also list system predefined policies")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--output", help="Write output to file")
    args = parser.parse_args()

    client = create_client(args.region)

    # Custom policies
    custom = list(iter_custom_policies(client))

    # System policies (optional)
    system = []
    if args.system:
        resp = client.list_system_security_policies()
        system = resp.body.security_policies or []

    if args.json:
        data = {
            "custom_policies": [p.to_map() for p in custom],
        }
        if args.system:
            data["system_policies"] = [p.to_map() for p in system]
        output = json.dumps(data, indent=2, ensure_ascii=False, default=str)
    else:
        lines: list[str] = []

        # Custom policies
        lines.append("=== Custom Security Policies ===")
        if not custom:
            lines.append("(none)")
        else:
            header = (
                f"{'SecurityPolicyId':<40} {'Name':<30} "
                f"{'TLSVersions':<30} {'Ciphers (count)'}"
            )
            lines.append(header)
            lines.append("-" * len(header))
            for p in custom:
                tls = ",".join(p.tlsversions or []) if p.tlsversions else "-"
                cipher_count = len(p.ciphers) if p.ciphers else 0
                lines.append(
                    f"{p.security_policy_id or '-':<40} "
                    f"{(p.security_policy_name or '-'):<30} "
                    f"{tls:<30} "
                    f"{cipher_count}"
                )
        lines.append(f"Total: {len(custom)} custom policy(ies)")

        # System policies
        if args.system:
            lines.append("")
            lines.append("=== System Security Policies ===")
            if not system:
                lines.append("(none)")
            else:
                header = (
                    f"{'SecurityPolicyId':<40} "
                    f"{'TLSVersions':<30} {'Ciphers (count)'}"
                )
                lines.append(header)
                lines.append("-" * len(header))
                for p in system:
                    tls = ",".join(p.tlsversions or []) if p.tlsversions else "-"
                    cipher_count = len(p.ciphers) if p.ciphers else 0
                    lines.append(
                        f"{p.security_policy_id or '-':<40} "
                        f"{tls:<30} "
                        f"{cipher_count}"
                    )
            lines.append(f"Total: {len(system)} system policy(ies)")

        output = "\n".join(lines)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output + "\n")
        print(f"Output written to {args.output}")
    else:
        print(output)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
