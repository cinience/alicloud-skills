#!/usr/bin/env python3
"""Plan and provision one Alibaba Cloud ECS spot instance via aliyun CLI."""

from __future__ import annotations

import argparse
import ipaddress
import json
from pathlib import Path
import re
import subprocess
import sys
import time
from typing import Any


class ProvisionError(RuntimeError):
    pass


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("plan", "apply"))
    parser.add_argument("--name", required=True, help="Stable name used for resources and evidence")
    parser.add_argument("--region", required=True)
    parser.add_argument("--zone")
    parser.add_argument("--cpu", type=int, required=True)
    parser.add_argument("--memory-gib", type=int, required=True)
    parser.add_argument("--instance-type")
    parser.add_argument("--image-id")
    parser.add_argument("--system-disk-size", type=int, default=40)
    parser.add_argument("--system-disk-category")
    parser.add_argument("--internet-bandwidth-out", type=int, default=0)
    parser.add_argument("--ssh-cidr")
    parser.add_argument("--spot-duration", type=int, choices=(0, 1), default=1)
    parser.add_argument("--spot-price-limit", type=float)
    parser.add_argument("--auto-release-time", help="UTC ISO 8601 time accepted by RunInstances")
    parser.add_argument("--vpc-id")
    parser.add_argument("--vswitch-id")
    parser.add_argument("--security-group-id")
    parser.add_argument("--key-pair-name")
    parser.add_argument("--vpc-cidr", default="10.88.0.0/16")
    parser.add_argument("--vswitch-cidr", default="10.88.1.0/24")
    parser.add_argument("--output-root", type=Path, default=Path("output/aliyun-ecs-spot-provision"))
    parser.add_argument("--confirm-create", action="store_true")
    args = parser.parse_args()
    validate_args(args)
    return args


def validate_args(args: argparse.Namespace) -> None:
    if not re.fullmatch(r"[a-zA-Z0-9][a-zA-Z0-9._-]{1,63}", args.name):
        raise ProvisionError("--name must be 2-64 safe ASCII characters")
    if args.cpu < 1 or args.memory_gib < 1:
        raise ProvisionError("CPU and memory must be positive")
    if args.spot_price_limit is not None and args.spot_price_limit <= 0:
        raise ProvisionError("--spot-price-limit must be positive")
    if not 20 <= args.system_disk_size <= 2048:
        raise ProvisionError("system disk size must be between 20 and 2048 GiB")
    if not 0 <= args.internet_bandwidth_out <= 100:
        raise ProvisionError("public bandwidth must be between 0 and 100 Mbit/s")
    if args.ssh_cidr:
        network = ipaddress.ip_network(args.ssh_cidr, strict=False)
        if network.version != 4:
            raise ProvisionError("--ssh-cidr must be an IPv4 network")
        if network.prefixlen == 0:
            raise ProvisionError("refusing an unrestricted SSH CIDR")
    if args.auto_release_time and not re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", args.auto_release_time):
        raise ProvisionError("--auto-release-time must use UTC format YYYY-MM-DDTHH:MM:SSZ")
    if args.internet_bandwidth_out > 0 and not (args.ssh_cidr or args.security_group_id):
        raise ProvisionError("public instances require --ssh-cidr or an existing --security-group-id")
    if args.vswitch_id and not args.vpc_id:
        raise ProvisionError("--vswitch-id requires --vpc-id")
    if args.mode == "apply" and not args.confirm_create:
        raise ProvisionError("apply requires --confirm-create")


class Aliyun:
    def __init__(self, evidence_dir: Path):
        self.evidence_dir = evidence_dir
        self.evidence_dir.mkdir(parents=True, exist_ok=True)

    def call(
        self,
        service: str,
        action: str,
        params: list[tuple[str, Any]],
        evidence: str,
        *,
        check: bool = True,
    ) -> tuple[int, dict[str, Any] | None, str]:
        command = ["aliyun", service, action]
        recorded_params: dict[str, Any] = {}
        for key, value in params:
            if value is None:
                continue
            recorded_params[key] = "<redacted>" if key == "PublicKeyBody" else value
            command.extend((f"--{key}", str(value).lower() if isinstance(value, bool) else str(value)))
        (self.evidence_dir / f"{evidence}.request.json").write_text(
            json.dumps(
                {"service": service, "action": action, "parameters": recorded_params},
                indent=2,
                ensure_ascii=False,
            ) + "\n",
            encoding="utf-8",
        )
        result = subprocess.run(command, text=True, capture_output=True, check=False)
        (self.evidence_dir / f"{evidence}.stdout.json").write_text(result.stdout, encoding="utf-8")
        (self.evidence_dir / f"{evidence}.stderr.txt").write_text(result.stderr, encoding="utf-8")
        payload = None
        if result.stdout.strip():
            try:
                payload = json.loads(result.stdout)
            except json.JSONDecodeError as exc:
                raise ProvisionError(f"{action} returned invalid JSON; see {evidence}.stdout.json") from exc
        if check and result.returncode != 0:
            raise ProvisionError(f"{action} failed; see {evidence}.stderr.txt: {result.stderr.strip()}")
        return result.returncode, payload, result.stderr


def get_path(data: dict[str, Any], *path: str, default: Any = None) -> Any:
    current: Any = data
    for key in path:
        if not isinstance(current, dict) or key not in current:
            return default
        current = current[key]
    return current


def available_offers(payload: dict[str, Any]) -> list[dict[str, str]]:
    offers: list[dict[str, str]] = []
    zones = get_path(payload, "AvailableZones", "AvailableZone", default=[]) or []
    for zone in zones:
        for resource in get_path(zone, "AvailableResources", "AvailableResource", default=[]) or []:
            supported = get_path(resource, "SupportedResources", "SupportedResource", default=[]) or []
            for item in supported:
                if item.get("Status") == "Available":
                    offers.append({"zone": zone["ZoneId"], "instance_type": item["Value"]})
    return offers


def available_supported_resources(payload: dict[str, Any]) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    zones = get_path(payload, "AvailableZones", "AvailableZone", default=[]) or []
    for zone in zones:
        for resource in get_path(zone, "AvailableResources", "AvailableResource", default=[]) or []:
            supported = get_path(resource, "SupportedResources", "SupportedResource", default=[]) or []
            items.extend(item for item in supported if item.get("Status") == "Available")
    return items


def offer_rank(offer: dict[str, str]) -> tuple[int, str, str]:
    preferred = ("ecs.c9i.", "ecs.c9a.", "ecs.c8i.", "ecs.c8a.", "ecs.c8y.", "ecs.u2")
    instance_type = offer["instance_type"]
    rank = next((index for index, prefix in enumerate(preferred) if instance_type.startswith(prefix)), len(preferred))
    return rank, instance_type, offer["zone"]


def client_token(name: str, action: str) -> str:
    return f"{name[:40]}-{action}"[:64]


def resolve_plan(args: argparse.Namespace, cli: Aliyun) -> dict[str, Any]:
    _, capacity, _ = cli.call(
        "ecs",
        "DescribeAvailableResource",
        [("RegionId", args.region), ("ZoneId", args.zone), ("DestinationResource", "InstanceType"),
         ("ResourceType", "instance"), ("InstanceChargeType", "PostPaid"),
         ("SpotStrategy", "SpotWithPriceLimit" if args.spot_price_limit is not None else "SpotAsPriceGo"),
         ("Cores", args.cpu), ("Memory", args.memory_gib)],
        "capacity",
    )
    offers = available_offers(capacity or {})
    if args.zone:
        offers = [offer for offer in offers if offer["zone"] == args.zone]
    if args.instance_type:
        offers = [offer for offer in offers if offer["instance_type"] == args.instance_type]
    if not offers:
        raise ProvisionError("no matching spot capacity is currently available")
    selected = None
    disk_category = None
    for offer in sorted(offers, key=offer_rank):
        safe_type = offer["instance_type"].replace(".", "-")
        _, disks_payload, _ = cli.call(
            "ecs", "DescribeAvailableResource",
            [("RegionId", args.region), ("ZoneId", offer["zone"]),
             ("DestinationResource", "SystemDisk"), ("ResourceType", "instance"),
             ("InstanceChargeType", "PostPaid"),
             ("SpotStrategy", "SpotWithPriceLimit" if args.spot_price_limit is not None else "SpotAsPriceGo"),
             ("InstanceType", offer["instance_type"])],
            f"disk-capacity-{offer['zone']}-{safe_type}",
        )
        disk_items = available_supported_resources(disks_payload or {})
        requested = args.system_disk_category
        categories = (requested,) if requested else ("cloud_essd", "cloud_auto", "cloud_efficiency")
        match = next(
            (
                item for category in categories for item in disk_items
                if item.get("Value") == category
                and int(item.get("Min", 0)) <= args.system_disk_size <= int(item.get("Max", 2**31))
            ),
            None,
        )
        if match:
            selected = offer
            disk_category = match["Value"]
            break
    if not selected or not disk_category:
        raise ProvisionError("no offer has a compatible system disk at the requested size")
    zone = selected["zone"]
    instance_type = selected["instance_type"]

    image_id = args.image_id
    if not image_id:
        _, images_payload, _ = cli.call(
            "ecs", "DescribeImages",
            [("RegionId", args.region), ("ImageOwnerAlias", "system"), ("OSType", "linux"),
             ("Architecture", "x86_64"), ("PageSize", 100)],
            "images",
        )
        images = get_path(images_payload or {}, "Images", "Image", default=[]) or []
        candidates = [image for image in images if "ubuntu_24_04_x64" in image.get("ImageId", "")
                      and "gpu" not in image.get("ImageId", "").lower() and image.get("Status") == "Available"]
        if not candidates:
            raise ProvisionError("no Ubuntu 24.04 x86_64 system image found; pass --image-id")
        image_id = sorted(candidates, key=lambda image: image.get("CreationTime", ""), reverse=True)[0]["ImageId"]

    spot_strategy = "SpotWithPriceLimit" if args.spot_price_limit is not None else "SpotAsPriceGo"
    price_params: list[tuple[str, Any]] = [
        ("RegionId", args.region), ("ZoneId", zone), ("ResourceType", "instance"),
        ("InstanceType", instance_type), ("PriceUnit", "Hour"), ("Period", 1),
        ("SpotStrategy", spot_strategy), ("SpotDuration", args.spot_duration),
        ("SystemDisk.Category", disk_category), ("SystemDisk.Size", args.system_disk_size),
        ("InternetChargeType", "PayByTraffic"),
        ("InternetMaxBandwidthOut", args.internet_bandwidth_out),
    ]
    _, price, _ = cli.call("ecs", "DescribePrice", price_params, "price")
    price_info = get_path(price or {}, "PriceInfo", "Price", default={}) or {}
    details = get_path(price_info, "DetailInfos", "DetailInfo", default=[]) or []
    return {
        "name": args.name,
        "region": args.region,
        "zone": zone,
        "cpu": args.cpu,
        "memory_gib": args.memory_gib,
        "instance_type": instance_type,
        "image_id": image_id,
        "system_disk_category": disk_category,
        "system_disk_size_gib": args.system_disk_size,
        "spot_strategy": spot_strategy,
        "spot_duration_hours": args.spot_duration,
        "spot_price_limit": args.spot_price_limit,
        "internet_charge_type": "PayByTraffic",
        "internet_bandwidth_out_mbit": args.internet_bandwidth_out,
        "ssh_cidr": args.ssh_cidr,
        "auto_release_time": args.auto_release_time,
        "available_offers": sorted(offers, key=offer_rank),
        "quote": {
            "currency": price_info.get("Currency"),
            "trade_price_per_hour": price_info.get("TradePrice"),
            "spot_compute_price_per_hour": price_info.get("SpotInstanceTypePrice"),
            "original_price_per_hour": price_info.get("OriginalPrice"),
            "components": [
                {"resource": item.get("Resource"), "trade_price_per_hour": item.get("TradePrice")}
                for item in details
            ],
        },
    }


def load_state(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def save_state(path: Path, state: dict[str, Any]) -> None:
    path.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def wait_for_vpc(cli: Aliyun, region: str, vpc_id: str) -> None:
    for attempt in range(30):
        _, payload, _ = cli.call(
            "vpc", "DescribeVpcAttribute", [("RegionId", region), ("VpcId", vpc_id)],
            f"vpc-status-{attempt + 1}",
        )
        if (payload or {}).get("Status") == "Available":
            return
        time.sleep(2)
    raise ProvisionError(f"VPC {vpc_id} did not become Available")


def ensure_infrastructure(args: argparse.Namespace, plan: dict[str, Any], cli: Aliyun,
                          state_path: Path, state: dict[str, Any]) -> dict[str, Any]:
    prefix = args.name[:64]
    vpc_id = state.get("vpc_id") or args.vpc_id
    if not vpc_id:
        _, payload, _ = cli.call(
            "vpc", "CreateVpc",
            [("RegionId", args.region), ("VpcName", f"{prefix}-vpc"), ("CidrBlock", args.vpc_cidr),
             ("Description", "VPC for one spot ECS instance"),
             ("ClientToken", client_token(prefix, "create-vpc"))],
            "create-vpc",
        )
        vpc_id = (payload or {}).get("VpcId")
        if not vpc_id:
            raise ProvisionError("CreateVpc returned no VpcId")
        state["vpc_id"] = vpc_id
        save_state(state_path, state)
    wait_for_vpc(cli, args.region, vpc_id)

    vswitch_id = state.get("vswitch_id") or args.vswitch_id
    if not vswitch_id:
        _, payload, _ = cli.call(
            "vpc", "CreateVSwitch",
            [("RegionId", args.region), ("ZoneId", plan["zone"]), ("VpcId", vpc_id),
             ("VSwitchName", f"{prefix}-vsw"), ("CidrBlock", args.vswitch_cidr),
             ("Description", "vSwitch for one spot ECS instance"),
             ("ClientToken", client_token(prefix, "create-vswitch"))],
            "create-vswitch",
        )
        vswitch_id = (payload or {}).get("VSwitchId")
        if not vswitch_id:
            raise ProvisionError("CreateVSwitch returned no VSwitchId")
        state["vswitch_id"] = vswitch_id
        save_state(state_path, state)

    security_group_id = state.get("security_group_id") or args.security_group_id
    if not security_group_id:
        _, payload, _ = cli.call(
            "ecs", "CreateSecurityGroup",
            [("RegionId", args.region), ("VpcId", vpc_id), ("SecurityGroupName", f"{prefix}-sg"),
             ("SecurityGroupType", "normal"), ("Description", "Restricted security group for spot ECS"),
             ("ClientToken", client_token(prefix, "create-sg"))],
            "create-security-group",
        )
        security_group_id = (payload or {}).get("SecurityGroupId")
        if not security_group_id:
            raise ProvisionError("CreateSecurityGroup returned no SecurityGroupId")
        state["security_group_id"] = security_group_id
        save_state(state_path, state)
        if args.ssh_cidr:
            cli.call(
                "ecs", "AuthorizeSecurityGroup",
                [("RegionId", args.region), ("SecurityGroupId", security_group_id),
                 ("IpProtocol", "tcp"), ("PortRange", "22/22"), ("SourceCidrIp", args.ssh_cidr),
                 ("Policy", "accept"), ("Priority", 1), ("Description", "Restricted SSH"),
                 ("ClientToken", client_token(prefix, "authorize-ssh"))],
                "authorize-ssh",
            )

    key_pair_name = state.get("key_pair_name") or args.key_pair_name
    if not key_pair_name:
        key_pair_name = f"{prefix}-key"[:64]
    if not args.key_pair_name and not state.get("key_pair_imported"):
        key_dir = cli.evidence_dir / "private"
        key_dir.mkdir(mode=0o700, exist_ok=True)
        private_key = key_dir / f"{key_pair_name}.pem"
        if private_key.exists() and state.get("private_key_path") != str(private_key):
            raise ProvisionError(f"refusing to reuse untracked private key {private_key}")
        if not private_key.exists():
            subprocess.run(
                ["ssh-keygen", "-q", "-t", "rsa", "-b", "4096", "-N", "", "-C", prefix,
                 "-f", str(private_key)],
                check=True,
            )
        private_key.chmod(0o600)
        public_key = Path(f"{private_key}.pub").read_text(encoding="utf-8").strip()
        state["key_pair_name"] = key_pair_name
        state["private_key_path"] = str(private_key)
        save_state(state_path, state)
        cli.call(
            "ecs", "ImportKeyPair",
            [("RegionId", args.region), ("KeyPairName", key_pair_name), ("PublicKeyBody", public_key)],
            "import-key-pair",
        )
        state["key_pair_imported"] = True
        save_state(state_path, state)

    state.update({"vpc_id": vpc_id, "vswitch_id": vswitch_id,
                  "security_group_id": security_group_id, "key_pair_name": key_pair_name})
    save_state(state_path, state)
    return state


def instance_params(args: argparse.Namespace, plan: dict[str, Any], state: dict[str, Any],
                    dry_run: bool) -> list[tuple[str, Any]]:
    params: list[tuple[str, Any]] = [
        ("RegionId", args.region), ("ZoneId", plan["zone"]), ("ImageId", plan["image_id"]),
        ("InstanceType", plan["instance_type"]), ("InstanceChargeType", "PostPaid"),
        ("SpotStrategy", plan["spot_strategy"]), ("SpotDuration", args.spot_duration),
        ("Amount", 1), ("MinAmount", 1), ("InstanceName", args.name),
        ("VSwitchId", state["vswitch_id"]), ("SecurityGroupId", state["security_group_id"]),
        ("KeyPairName", state["key_pair_name"]), ("SystemDisk.Category", plan["system_disk_category"]),
        ("SystemDisk.Size", args.system_disk_size), ("InternetChargeType", "PayByTraffic"),
        ("InternetMaxBandwidthOut", args.internet_bandwidth_out),
        ("AutoReleaseTime", args.auto_release_time), ("DryRun", dry_run),
    ]
    if not dry_run:
        params.append(("ClientToken", client_token(args.name, "run-instance")))
    if args.spot_price_limit is not None:
        params.append(("SpotPriceLimit", args.spot_price_limit))
    return params


def create_and_verify(args: argparse.Namespace, plan: dict[str, Any], cli: Aliyun,
                      state_path: Path, state: dict[str, Any]) -> dict[str, Any]:
    instance_id = state.get("instance_id")
    if not instance_id:
        code, _, stderr = cli.call(
            "ecs", "RunInstances", instance_params(args, plan, state, True), "run-instances-dry-run", check=False,
        )
        if code == 0 or "DryRunOperation" not in stderr:
            raise ProvisionError("RunInstances dry run did not return DryRunOperation")
        _, payload, _ = cli.call(
            "ecs", "RunInstances", instance_params(args, plan, state, False), "run-instances",
        )
        ids = get_path(payload or {}, "InstanceIdSets", "InstanceIdSet", default=[]) or []
        if len(ids) != 1:
            raise ProvisionError("RunInstances did not return exactly one instance ID")
        instance_id = ids[0]
        state["instance_id"] = instance_id
        save_state(state_path, state)

    for attempt in range(60):
        _, payload, _ = cli.call(
            "ecs", "DescribeInstances",
            [("RegionId", args.region), ("InstanceIds", json.dumps([instance_id]))],
            f"instance-status-{attempt + 1}",
        )
        instances = get_path(payload or {}, "Instances", "Instance", default=[]) or []
        if instances and instances[0].get("Status") == "Running":
            state["instance"] = instances[0]
            save_state(state_path, state)
            return state
        time.sleep(3)
    raise ProvisionError(f"instance {instance_id} did not reach Running")


def main() -> int:
    try:
        args = parse_args()
        evidence_dir = args.output_root / args.name
        plan_path = evidence_dir / "plan.json"
        if args.mode == "apply":
            if not plan_path.exists():
                raise ProvisionError("apply requires an existing plan.json; run plan first")
            saved_plan = json.loads(plan_path.read_text(encoding="utf-8"))
            expected = {
                "region": args.region,
                "cpu": args.cpu,
                "memory_gib": args.memory_gib,
                "system_disk_size_gib": args.system_disk_size,
                "internet_bandwidth_out_mbit": args.internet_bandwidth_out,
                "ssh_cidr": args.ssh_cidr,
                "spot_duration_hours": args.spot_duration,
                "spot_price_limit": args.spot_price_limit,
                "auto_release_time": args.auto_release_time,
            }
            mismatches = [key for key, value in expected.items() if saved_plan.get(key) != value]
            if mismatches:
                raise ProvisionError(f"apply arguments differ from saved plan: {', '.join(mismatches)}")
            args.zone = args.zone or saved_plan["zone"]
            args.instance_type = args.instance_type or saved_plan["instance_type"]
            args.image_id = args.image_id or saved_plan["image_id"]
            args.system_disk_category = args.system_disk_category or saved_plan["system_disk_category"]
        cli = Aliyun(evidence_dir)
        plan = resolve_plan(args, cli)
        plan_path.write_text(json.dumps(plan, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        if args.mode == "plan":
            print(json.dumps(plan, indent=2, ensure_ascii=False))
            return 0

        state_path = evidence_dir / "state.json"
        state = load_state(state_path)
        if state.get("plan"):
            locked_fields = (
                "region", "zone", "instance_type", "image_id", "system_disk_category",
                "system_disk_size_gib", "internet_bandwidth_out_mbit", "ssh_cidr",
                "spot_strategy", "spot_duration_hours", "spot_price_limit", "auto_release_time",
            )
            changed = [field for field in locked_fields if state["plan"].get(field) != plan.get(field)]
            if changed:
                raise ProvisionError(
                    f"saved infrastructure state belongs to a different plan: {', '.join(changed)}"
                )
        state["plan"] = plan
        save_state(state_path, state)
        state = ensure_infrastructure(args, plan, cli, state_path, state)
        state = create_and_verify(args, plan, cli, state_path, state)
        summary = {
            "instance_id": state["instance_id"],
            "status": state["instance"].get("Status"),
            "public_ip": get_path(state["instance"], "PublicIpAddress", "IpAddress", default=[]),
            "private_ip": get_path(state["instance"], "VpcAttributes", "PrivateIpAddress", "IpAddress", default=[]),
            "private_key_path": state.get("private_key_path"),
            "quote": plan["quote"],
            "state_path": str(state_path),
        }
        (evidence_dir / "summary.json").write_text(
            json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        print(json.dumps(summary, indent=2, ensure_ascii=False))
        return 0
    except (ProvisionError, FileNotFoundError, subprocess.SubprocessError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
