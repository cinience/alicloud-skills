# ALB Resource Dependencies and Creation Order

## Dependency Diagram

```
VPC + VSwitch (prerequisite, already exists)
│
├── ACL ← Only requires Region, no other dependencies
│
├── Security Policy ← Only requires Region, no other dependencies
│
├── Server Group ← Requires VpcId
│   └── Add Servers ← Requires ServerGroupId + backend instances (ECS/ENI/ECI/IP)
│
└── ALB Instance ← Requires VpcId + ZoneMappings(ZoneId + VSwitchId)
    │
    ├── Access Log (enable) ← Requires LoadBalancerId + SLS Project/LogStore
    │
    └── Listener ← Requires LoadBalancerId + ServerGroupId (default forwarding action)
        │           + CertificateId (required for HTTPS)
        │           + SecurityPolicyId (optional for HTTPS)
        │
        ├── Forwarding Rule ← Requires ListenerId + ServerGroupId (forwarding target)
        │
        ├── Associate Certificate (SNI) ← Requires ListenerId + CertificateId
        │
        └── Associate ACL ← Requires ListenerId + AclId + AclType(White/Black)
```

## Creation Order (Building a Complete ALB from Scratch)

Must strictly follow the order below, otherwise it will fail due to missing dependency IDs:

```
Step 1: Prepare resources with no dependencies (can be parallelized)
  ├── Create Server Group          → Obtain ServerGroupId
  ├── Create ACL (if needed)       → Obtain AclId
  └── Create Security Policy (if needed) → Obtain SecurityPolicyId

Step 2: Add backends to Server Group (can be done at any time)
  └── Add Servers to ServerGroup ← ServerGroupId + backend instance info

Step 3: Create ALB instance
  └── Create LoadBalancer          → Obtain LoadBalancerId
      ⚠️ ALB creation is an async operation, wait until status becomes Active

Step 4: Enable Access Log (optional)
  └── EnableLoadBalancerAccessLog ← LoadBalancerId

Step 5: Create Listener
  └── Create Listener              → Obtain ListenerId
      ← LoadBalancerId + ServerGroupId (default forwarding)
      ← CertificateId (required for HTTPS)
      ← SecurityPolicyId (optional for HTTPS, defaults to tls_cipher_policy_1_0)
      ⚠️ Listener creation is also an async operation

Step 6: Configure Listener associated resources (can be parallelized)
  ├── Create Forwarding Rule     ← ListenerId + ServerGroupId
  ├── Associate SNI Certificate  ← ListenerId + CertificateId
  └── Associate ACL              ← ListenerId + AclId
```

## Deletion Order (Reverse of Creation)

Deletion must start from leaf resources; disassociate first, then delete:

```
Step 1: Delete/disassociate Listener associated resources (can be parallelized)
  ├── Delete Forwarding Rules
  ├── Disassociate SNI Certificates (DissociateAdditionalCertificatesFromListener)
  └── Disassociate ACLs (DissociateAclsFromListener)

Step 2: Delete Listener
  └── Delete Listener

Step 3: Delete ALB instance
  ├── Disable Deletion Protection (DisableDeletionProtection) (if enabled)
  └── Delete LoadBalancer

Step 4: Delete resources with no dependencies (can be parallelized)
  ├── Remove backends → Delete Server Group
  ├── Delete ACL
  └── Delete Security Policy
```

## Async Operation Notes

The following operations are asynchronous. They return a `JobId` upon invocation, and you need to poll until completion:

| Operation | Wait Condition |
|---|---|
| CreateLoadBalancer | `GetLoadBalancerAttribute` → `LoadBalancerStatus == Active` |
| DeleteLoadBalancer | `GetLoadBalancerAttribute` → 404 (resource does not exist) |
| CreateListener | `GetListenerAttribute` → `ListenerStatus == Running` |
| DeleteListener | `GetListenerAttribute` → 404 |
| CreateRule / CreateRules | `ListRules` to confirm the rule exists |

You can query async task status via `ListAsynJobs`.

## ID Passing Quick Reference

| Current Operation | Required IDs | Where to Obtain |
|---|---|---|
| CreateServerGroup | VpcId | Known or from VPC console |
| AddServersToServerGroup | ServerGroupId | Returned by CreateServerGroup |
| CreateLoadBalancer | VpcId, ZoneId, VSwitchId | Known or from VPC/ECS console |
| CreateListener | LoadBalancerId, ServerGroupId | Returned by previous steps |
| CreateListener (HTTPS) | CertificateId | SSL Certificate Management console |
| CreateRule | ListenerId, ServerGroupId | Returned by previous steps |
| AssociateAclsWithListener | ListenerId, AclId | Returned by previous steps |
| EnableLoadBalancerAccessLog | LoadBalancerId, LogProject, LogStore | SLS console |

## Common Topology Patterns

### Pattern 1: HTTP → HTTPS Redirect

```
ServerGroup-A (with backends attached)

ALB
├── Listener HTTP:80
│   └── DefaultAction: Redirect → HTTPS:443
└── Listener HTTPS:443
    ├── DefaultAction: Forward → ServerGroup-A
    └── Certificate: cert-xxx
```

Creation order: ServerGroup-A → ALB → Listener HTTPS:443 (bindServerGroup-A) → Listener HTTP:80 (DefaultAction=Redirect)

### Pattern 2: Multi-Domain Routing

```
ServerGroup-API (API backend)
ServerGroup-Web (frontend static)
ServerGroup-Default (fallback)

ALB
└── Listener HTTPS:443
    ├── Rule: Host(api.example.com) → ServerGroup-API
    ├── Rule: Host(www.example.com) → ServerGroup-Web
    └── DefaultAction → ServerGroup-Default
```

Creation order: 3 ServerGroups → ALB → Listener (bind ServerGroup-Default) → 2 Rules

### Pattern 3: Blue-Green Deployment

```
ServerGroup-Blue (current version, weight 100)
ServerGroup-Green (new version, weight 0)

ALB
└── Listener HTTPS:443
    └── DefaultAction: ForwardGroup
        ├── ServerGroup-Blue  weight=100
        └── ServerGroup-Green weight=0
```

Adjust weights via `UpdateRuleAttribute` to switch traffic.
