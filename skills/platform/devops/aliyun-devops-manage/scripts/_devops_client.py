#!/usr/bin/env python3
"""Shared DevOps client helpers for local scripts."""

from __future__ import annotations

import os


def _get_env(*names: str) -> str | None:
    for name in names:
        value = os.getenv(name)
        if value:
            return value
    return None


def create_client(region_id: str):
    """Return (devops_client, devops_models_module)."""
    try:
        from alibabacloud_devops20210625.client import Client as DevopsClient
        from alibabacloud_devops20210625 import models as devops_models
        from alibabacloud_tea_openapi import models as open_api_models
    except ImportError as exc:  # pragma: no cover - compile-safe fallback
        raise RuntimeError(
            "Missing SDK dependencies. Install with: "
            "python -m pip install -U alibabacloud_devops20210625 alibabacloud_tea_openapi"
        ) from exc

    ak = _get_env("ALICLOUD_ACCESS_KEY_ID", "ALIBABA_CLOUD_ACCESS_KEY_ID")
    sk = _get_env("ALICLOUD_ACCESS_KEY_SECRET", "ALIBABA_CLOUD_ACCESS_KEY_SECRET")
    token = _get_env("ALICLOUD_SECURITY_TOKEN", "ALIBABA_CLOUD_SECURITY_TOKEN")

    if not ak or not sk:
        raise RuntimeError(
            "Missing credentials: set ALICLOUD_ACCESS_KEY_ID and "
            "ALICLOUD_ACCESS_KEY_SECRET (or ALIBABA_CLOUD_* equivalents)."
        )

    config = open_api_models.Config(region_id=region_id)
    config.access_key_id = ak
    config.access_key_secret = sk
    if token:
        config.security_token = token

    return DevopsClient(config), devops_models
