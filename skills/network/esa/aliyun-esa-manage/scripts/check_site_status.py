#!/usr/bin/env python3
"""Check ESA site status and configuration overview.

Displays site info and configuration settings (IPv6, dev mode, tiered cache, etc.).
"""

from __future__ import annotations

import argparse
import os

from alibabacloud_esa20240910.client import Client as Esa20240910Client
from alibabacloud_esa20240910 import models as esa_models
from alibabacloud_tea_openapi import models as open_api_models


def create_client() -> Esa20240910Client:
    config = open_api_models.Config(
        region_id="cn-hangzhou",
        endpoint="esa.cn-hangzhou.aliyuncs.com",
    )
    ak = os.getenv("ALICLOUD_ACCESS_KEY_ID") or os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID")
    sk = os.getenv("ALICLOUD_ACCESS_KEY_SECRET") or os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET")
    token = os.getenv("ALICLOUD_SECURITY_TOKEN") or os.getenv("ALIBABA_CLOUD_SECURITY_TOKEN")
    if ak and sk:
        config.access_key_id = ak
        config.access_key_secret = sk
        if token:
            config.security_token = token
    return Esa20240910Client(config)


def main() -> int:
    parser = argparse.ArgumentParser(description="Check ESA site status and configuration")
    parser.add_argument("--site-id", type=int, required=True, help="ESA site ID")
    args = parser.parse_args()

    client = create_client()
    site_id = args.site_id

    # 1. Site info
    site_resp = client.get_site(esa_models.GetSiteRequest(site_id=site_id))
    site = site_resp.body.site_model  # GetSite returns nested site_model object
    print("=== Site Info ===")
    print(f"  Site Name:   {getattr(site, 'site_name', 'N/A')}")
    print(f"  Site ID:     {site_id}")
    print(f"  Status:      {getattr(site, 'status', 'N/A')}")
    print(f"  Access Type: {getattr(site, 'access_type', 'N/A')}")
    print(f"  Plan:        {getattr(site, 'plan_name', 'N/A')}")
    print(f"  Coverage:    {getattr(site, 'coverage', 'N/A')}")
    print(f"  CNAME Zone:  {getattr(site, 'cname_zone', 'N/A')}")
    print()

    # 2. Tiered cache config
    try:
        cache_resp = client.get_tiered_cache(esa_models.GetTieredCacheRequest(site_id=site_id))
        print("=== Tiered Cache ===")
        print(f"  Architecture: {getattr(cache_resp.body, 'cache_architecture_mode', 'N/A')}")
    except Exception as e:
        print(f"=== Tiered Cache ===\n  Error: {e}")
    print()

    # 3. IPv6 config
    try:
        ipv6_resp = client.get_ipv6(esa_models.GetIPv6Request(site_id=site_id))
        print("=== IPv6 ===")
        print(f"  Enabled: {getattr(ipv6_resp.body, 'enable', 'N/A')}")
    except Exception as e:
        print(f"=== IPv6 ===\n  Error: {e}")
    print()

    # 4. Development mode
    try:
        dev_resp = client.get_development_mode(esa_models.GetDevelopmentModeRequest(site_id=site_id))
        print("=== Development Mode ===")
        print(f"  Enabled: {getattr(dev_resp.body, 'enable', 'N/A')}")
    except Exception as e:
        print(f"=== Development Mode ===\n  Error: {e}")
    print()

    # 5. SEO bypass
    try:
        seo_resp = client.get_seo_bypass(esa_models.GetSeoBypassRequest(site_id=site_id))
        print("=== SEO Bypass ===")
        print(f"  Enabled: {getattr(seo_resp.body, 'enable', 'N/A')}")
    except Exception as e:
        print(f"=== SEO Bypass ===\n  Error: {e}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
