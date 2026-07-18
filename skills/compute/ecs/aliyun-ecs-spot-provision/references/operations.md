# Spot ECS provisioning operations

## Resource sequence

Create resources in this order and persist every returned ID before continuing:

1. VPC, then poll `DescribeVpcAttribute` for `Available`.
2. vSwitch in the selected zone.
3. VPC security group and only the requested ingress rule.
4. Local key material, followed by `ImportKeyPair`.
5. `RunInstances` with `DryRun=true`.
6. `RunInstances` without `DryRun` using the same resolved plan.
7. `DescribeInstances` until `Running`.

Alibaba Cloud control-plane creation is asynchronous. An immediate dependent call can return `IncorrectVpcStatus`; wait and reuse the same VPC instead of creating another one.

## Price interpretation

Use `DescribePrice` with the exact zone, instance type, spot strategy, system-disk category/size, and bandwidth mode.

- `TradePrice`: current combined hourly price returned for the request.
- `DetailInfos.DetailInfo`: compute, image, disk, and fixed-bandwidth components.
- `SpotInstanceTypePrice`: current spot compute component.
- `SpotAsPriceGo`: automatic market bid with the normal pay-as-you-go compute price as the upper bound.
- `PayByTraffic`: no fixed hourly bandwidth charge; outbound traffic is billed separately per GB.

Quotes are snapshots. Re-query immediately before creation and state the currency.

## Release semantics

- `SpotDuration=1`: protect the instance from reclamation for the first hour. It does not schedule release at one hour.
- Empty `AutoReleaseTime`: no scheduled release. Billing continues while the instance survives and runs.
- `AutoReleaseTime`: explicit UTC scheduled release time accepted by `RunInstances`.
- Spot reclaim: after the protection period, inventory changes or price conditions can reclaim the instance.
- System disk: assume it is deleted with the instance unless the API response and disk attributes prove otherwise.

## Partial failure recovery

Inspect `state.json` and individual API response files in the evidence directory. Re-run with the same `--name` and arguments. The script reuses persisted VPC, vSwitch, security-group, key-pair, and instance IDs.

Do not perform automatic rollback. Deleting a partially created key, security group, vSwitch, or VPC can remove resources that became useful during manual recovery.

## Guest verification

Control-plane `Running` proves the instance launched, not that SSH is reachable or that the guest filesystem spans the requested disk.

- Verify SSH only from a source covered by the security-group CIDR.
- If the execution environment blocks outbound TCP/22, use Cloud Assistant `RunCommand` to inspect the guest.
- Check `lsblk`, `findmnt`, and `df -hT /` for large system disks.
- If an existing ext4 system disk was expanded online, identify the root partition, use `growpart`, then `resize2fs`. Use `xfs_growfs /` for XFS.
