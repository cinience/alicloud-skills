# VPC API Overview (2016-04-28)

Product code: `Vpc` | API version: `2016-04-28`

## VPC

| API | Description |
|-----|-------------|
| CreateVpc | Create a VPC. Required: `RegionId`, `CidrBlock`. Returns `VpcId`. |
| DeleteVpc | Delete a VPC. Fails if resources (VSwitches, security groups) still exist. |
| ModifyVpcAttribute | Modify VPC name, description, or CIDR block. |
| DescribeVpcs | List VPCs. Supports filters: `VpcId`, `VpcName`, `IsDefault`, `ResourceGroupId`. Paginated via `PageNumber`+`PageSize`. |
| DescribeVpcAttribute | Get detailed attributes of a single VPC by `VpcId`. |

## VSwitch

| API | Description |
|-----|-------------|
| CreateVSwitch | Create a VSwitch. Required: `RegionId`, `VpcId`, `ZoneId`, `CidrBlock`. VPC must be `Available`. |
| DeleteVSwitch | Delete a VSwitch. Fails if resources (ECS, RDS) still attached. |
| ModifyVSwitchAttribute | Modify VSwitch name or description. |
| DescribeVSwitches | List VSwitches. Supports filters: `VpcId`, `VSwitchId`, `ZoneId`, `VSwitchName`, `IsDefault`. Paginated via `PageNumber`+`PageSize`. |
| DescribeVSwitchAttributes | Get detailed attributes of a single VSwitch. |

## Route Table

| API | Description |
|-----|-------------|
| CreateRouteTable | Create a custom route table in a VPC. |
| DeleteRouteTable | Delete a custom route table. |
| DescribeRouteTables | List route tables. Supports filters: `VpcId`, `RouteTableId`, `RouteTableName`. |
| CreateRouteEntry | Add a route entry to a route table. |
| DeleteRouteEntry | Delete a route entry. |
| DescribeRouteEntryList | List route entries in a route table. |
| AssociateRouteTable | Associate a route table with a VSwitch. |
| UnassociateRouteTable | Disassociate a route table from a VSwitch. |

## NAT Gateway

| API | Description |
|-----|-------------|
| CreateNatGateway | Create a NAT gateway in a VPC. |
| DeleteNatGateway | Delete a NAT gateway. |
| DescribeNatGateways | List NAT gateways. |
| CreateSnatEntry | Create an SNAT entry for outbound internet access. |
| DeleteSnatEntry | Delete an SNAT entry. |
| DescribeSnatTableEntries | List SNAT entries. |

## Elastic IP (EIP)

| API | Description |
|-----|-------------|
| AllocateEipAddress | Allocate an EIP. |
| AssociateEipAddress | Bind EIP to ECS, NAT, SLB, etc. |
| UnassociateEipAddress | Unbind EIP. |
| ReleaseEipAddress | Release an EIP. |
| DescribeEipAddresses | List EIPs. |

## Common Parameters

All APIs require `RegionId`. Authentication via AccessKey (AK/SK) or STS token.

### Pagination

Most list APIs use `PageNumber` (starts at 1) + `PageSize` (max 50). Response includes `TotalCount`.

### CIDR Block Ranges

VPC supports: `10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16` and their subnets.
VSwitch CIDR must be a subset of the VPC CIDR block.
