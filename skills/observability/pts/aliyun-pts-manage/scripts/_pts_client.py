#!/usr/bin/env python3
"""Shared PTS client helpers for local scripts."""

from __future__ import annotations

import os
from typing import Tuple


def _get_env(*names: str) -> str | None:
    for name in names:
        value = os.getenv(name)
        if value:
            return value
    return None


def create_client(region_id: str):
    """Return (pts_client, pts_models_module).

    Imports PTS SDK lazily so scripts can provide a clear install hint.
    """
    try:
        from alibabacloud_pts20201020.client import Client as PtsClient
        from alibabacloud_pts20201020 import models as pts_models
        from alibabacloud_tea_openapi import models as open_api_models
    except ImportError as exc:  # pragma: no cover - compile-safe fallback
        raise RuntimeError(
            "Missing SDK dependencies. Install with: "
            "python -m pip install -U alibabacloud_pts20201020 alibabacloud_tea_openapi"
        ) from exc

    ak = _get_env("ALICLOUD_ACCESS_KEY_ID", "ALIBABA_CLOUD_ACCESS_KEY_ID")
    sk = _get_env("ALICLOUD_ACCESS_KEY_SECRET", "ALIBABA_CLOUD_ACCESS_KEY_SECRET")
    token = _get_env("ALICLOUD_SECURITY_TOKEN", "ALIBABA_CLOUD_SECURITY_TOKEN")

    if not ak or not sk:
        raise RuntimeError(
            "Missing credentials: set ALICLOUD_ACCESS_KEY_ID and "
            "ALICLOUD_ACCESS_KEY_SECRET (or ALIBABA_CLOUD_* equivalents)."
        )

    config = open_api_models.Config(
        region_id=region_id,
        endpoint=f"pts.{region_id}.aliyuncs.com",
    )
    config.access_key_id = ak
    config.access_key_secret = sk
    if token:
        config.security_token = token

    return PtsClient(config), pts_models
