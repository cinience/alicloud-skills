#!/usr/bin/env python3
"""List certificates associated with an ALB listener."""

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


def iter_certificates(client: Alb20200616Client, listener_id: str):
    """Yield all certificates for a listener."""
    next_token: str | None = None
    while True:
        req = alb_models.ListListenerCertificatesRequest(
            listener_id=listener_id,
            max_results=100,
            next_token=next_token,
        )
        resp = client.list_listener_certificates(req)
        for cert in resp.body.certificates or []:
            yield cert
        next_token = resp.body.next_token
        if not next_token:
            break


def main() -> int:
    parser = argparse.ArgumentParser(description="List ALB listener certificates")
    parser.add_argument("--region", required=True, help="Region ID")
    parser.add_argument("--listener-id", required=True, help="Listener ID")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--output", help="Write output to file")
    args = parser.parse_args()

    client = create_client(args.region)
    certs = list(iter_certificates(client, args.listener_id))

    if args.json:
        output = json.dumps(
            [c.to_map() for c in certs], indent=2, ensure_ascii=False, default=str
        )
    else:
        header = f"{'CertificateId':<50} {'CertificateType':<18} {'IsDefault'}"
        sep = "-" * len(header)
        lines = [header, sep]
        for c in certs:
            is_default = "Yes" if c.is_default else "No"
            lines.append(
                f"{c.certificate_id or '-':<50} "
                f"{(c.certificate_type or '-'):<18} "
                f"{is_default}"
            )
        lines.append(sep)
        lines.append(f"Total: {len(certs)} certificate(s) for {args.listener_id}")
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
