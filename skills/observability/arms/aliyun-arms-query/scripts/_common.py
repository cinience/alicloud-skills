"""Shared utilities for ARMS query scripts."""

import os
import sys

from alibabacloud_arms20190808.client import Client
from alibabacloud_tea_openapi.models import Config

DEFAULT_REGION = "cn-shanghai"

_AK_NAMES = ("ALIBABACLOUD_ACCESS_KEY_ID", "ALIBABA_CLOUD_ACCESS_KEY_ID", "ALICLOUD_ACCESS_KEY_ID", "ALIBABA_AK")
_SK_NAMES = ("ALIBABACLOUD_ACCESS_KEY_SECRET", "ALIBABA_CLOUD_ACCESS_KEY_SECRET", "ALICLOUD_ACCESS_KEY_SECRET", "ALIBABA_SK")


def get_env(*names: str, default: str | None = None) -> str:
    for name in names:
        value = os.getenv(name)
        if value:
            return value
    if default is not None:
        return default
    print(f"Missing env var: {' / '.join(names)}", file=sys.stderr)
    sys.exit(1)


def default_region() -> str:
    return os.getenv("ARMS_REGION_ID", DEFAULT_REGION)


def create_client(region_id: str | None = None) -> Client:
    if region_id is None:
        region_id = default_region()
    config = Config(
        access_key_id=get_env(*_AK_NAMES),
        access_key_secret=get_env(*_SK_NAMES),
        region_id=region_id,
    )
    config.endpoint = f"arms.{region_id}.aliyuncs.com"
    return Client(config)
