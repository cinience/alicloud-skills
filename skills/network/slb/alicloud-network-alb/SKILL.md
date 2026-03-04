---
name: alicloud-network-alb
description: Manage and troubleshoot Alibaba Cloud ALB (Application Load Balancer). List/inspect/create/update instances, listeners, server groups, rules, certificates, ACLs, security policies, and health check status.
---

Category: service

# Application Load Balancer (ALB)

## Validation

```bash
mkdir -p output/alicloud-network-alb
for f in skills/network/slb/alicloud-network-alb/scripts/*.py; do
  python3 -m py_compile "$f"
done
echo "py_compile_ok" > output/alicloud-network-alb/validate.txt
```

Pass criteria: command exits 0 and `output/alicloud-network-alb/validate.txt` is generated.

## Prerequisites

```bash
pip install alibabacloud_alb20200616 alibabacloud_tea_openapi alibabacloud_credentials
```

## AccessKey priority

1) Environment variables: `ALICLOUD_ACCESS_KEY_ID` / `ALICLOUD_ACCESS_KEY_SECRET`
2) Also supported: `ALIBABA_CLOUD_ACCESS_KEY_ID` / `ALIBABA_CLOUD_ACCESS_KEY_SECRET`
3) Optional STS token: `ALICLOUD_SECURITY_TOKEN`
4) Shared config file: `~/.alibabacloud/credentials`

## Scripts

All scripts support `--output <file>` to write results to file.

### Load Balancer Instances

**List instances** — `scripts/list_instances.py`

```bash
python3 scripts/list_instances.py --region cn-hangzhou
python3 scripts/list_instances.py --region cn-hangzhou --vpc-id vpc-xxx
python3 scripts/list_instances.py --region cn-hangzhou --address-type Internet --status Active
python3 scripts/list_instances.py --region cn-hangzhou --lb-ids alb-aaa alb-bbb --json
```

**Instance status (tree overview / full JSON)** — `scripts/get_instance_status.py`

```bash
# Tree overview: zones → listeners → rules
python3 scripts/get_instance_status.py --region cn-hangzhou --lb-id alb-xxx

# Full API response as JSON
python3 scripts/get_instance_status.py --region cn-hangzhou --lb-id alb-xxx --view detail
```

**Create ALB instance** — `scripts/create_load_balancer.py`

```bash
# Internet-facing ALB in two zones
python3 scripts/create_load_balancer.py --region cn-hangzhou --name my-alb \
    --vpc-id vpc-xxx --address-type Internet \
    --zone cn-hangzhou-h:vsw-aaa --zone cn-hangzhou-i:vsw-bbb

# Internal ALB with deletion protection
python3 scripts/create_load_balancer.py --region cn-hangzhou --name my-alb \
    --vpc-id vpc-xxx --address-type Intranet --deletion-protection \
    --zone cn-hangzhou-h:vsw-aaa --zone cn-hangzhou-i:vsw-bbb
```

**Delete ALB instance** — `scripts/delete_load_balancer.py`

```bash
python3 scripts/delete_load_balancer.py --region cn-hangzhou --lb-id alb-xxx
python3 scripts/delete_load_balancer.py --region cn-hangzhou --lb-id alb-xxx --yes  # skip confirm
```

**Deletion protection** — `scripts/deletion_protection.py`

```bash
python3 scripts/deletion_protection.py --region cn-hangzhou --resource-id alb-xxx --enable
python3 scripts/deletion_protection.py --region cn-hangzhou --resource-id alb-xxx --disable
```

### Listeners

**List listeners** — `scripts/list_listeners.py`

```bash
python3 scripts/list_listeners.py --region cn-hangzhou --lb-id alb-xxx
python3 scripts/list_listeners.py --region cn-hangzhou --lb-id alb-xxx --json
```

**Get listener details (certificates, ACL, config)** — `scripts/get_listener_attribute.py`

```bash
python3 scripts/get_listener_attribute.py --region cn-hangzhou --listener-id lsn-xxx
```

**Create listener** — `scripts/create_listener.py`

```bash
# HTTP listener forwarding to server group
python3 scripts/create_listener.py --region cn-hangzhou --lb-id alb-xxx \
    --protocol HTTP --port 80 --action-type ForwardGroup \
    --forward-server-groups sgp-xxx

# HTTPS listener with certificate
python3 scripts/create_listener.py --region cn-hangzhou --lb-id alb-xxx \
    --protocol HTTPS --port 443 --action-type ForwardGroup \
    --forward-server-groups sgp-xxx --certificate-ids cert-xxx

# HTTP to HTTPS redirect
python3 scripts/create_listener.py --region cn-hangzhou --lb-id alb-xxx \
    --protocol HTTP --port 80 --action-type Redirect \
    --redirect-protocol HTTPS --redirect-port 443

# Dry run
python3 scripts/create_listener.py --region cn-hangzhou --lb-id alb-xxx \
    --protocol HTTP --port 80 --action-type ForwardGroup \
    --forward-server-groups sgp-xxx --dry-run
```

**Update listener** — `scripts/update_listener.py`

```bash
# Update description
python3 scripts/update_listener.py --region cn-hangzhou --listener-id lsn-xxx \
    --description "Production HTTP listener"

# Change default forwarding target
python3 scripts/update_listener.py --region cn-hangzhou --listener-id lsn-xxx \
    --forward-server-groups sgp-new

# Update timeouts and security policy
python3 scripts/update_listener.py --region cn-hangzhou --listener-id lsn-xxx \
    --idle-timeout 60 --request-timeout 120 --security-policy-id tls_cipher_policy_1_2

# Enable HTTP/2 and gzip
python3 scripts/update_listener.py --region cn-hangzhou --listener-id lsn-xxx \
    --http2-enabled true --gzip-enabled true
```

**Start / Stop listener** — `scripts/start_listener.py` / `scripts/stop_listener.py`

```bash
python3 scripts/start_listener.py --region cn-hangzhou --listener-id lsn-xxx
python3 scripts/stop_listener.py --region cn-hangzhou --listener-id lsn-xxx
```

**Delete listener** — `scripts/delete_listener.py`

```bash
python3 scripts/delete_listener.py --region cn-hangzhou --listener-id lsn-xxx
python3 scripts/delete_listener.py --region cn-hangzhou --listener-id lsn-xxx --yes  # skip confirm
```

### Server Groups

**List server groups** — `scripts/list_server_groups.py`

```bash
python3 scripts/list_server_groups.py --region cn-hangzhou
python3 scripts/list_server_groups.py --region cn-hangzhou --vpc-id vpc-xxx
python3 scripts/list_server_groups.py --region cn-hangzhou --sg-ids sgp-aaa sgp-bbb
```

**List backend servers in a server group** — `scripts/list_server_group_servers.py`

```bash
python3 scripts/list_server_group_servers.py --region cn-hangzhou --sg-id sgp-xxx
```

**Create server group** — `scripts/create_server_group.py`

```bash
# Basic HTTP server group
python3 scripts/create_server_group.py --region cn-hangzhou --name my-sg \
    --vpc-id vpc-xxx --protocol HTTP

# With health check customization
python3 scripts/create_server_group.py --region cn-hangzhou --name my-sg \
    --vpc-id vpc-xxx --protocol HTTP \
    --health-check-path /health --health-check-interval 10

# With sticky sessions
python3 scripts/create_server_group.py --region cn-hangzhou --name my-sg \
    --vpc-id vpc-xxx --protocol HTTP \
    --sticky-session-enabled --sticky-session-type Server --sticky-session-cookie SERVERID

# Dry run
python3 scripts/create_server_group.py --region cn-hangzhou --name my-sg \
    --vpc-id vpc-xxx --dry-run
```

**Delete server group** — `scripts/delete_server_group.py`

```bash
python3 scripts/delete_server_group.py --region cn-hangzhou --sg-id sgp-xxx
python3 scripts/delete_server_group.py --region cn-hangzhou --sg-id sgp-xxx --yes  # skip confirm
```

**Add backend servers** — `scripts/add_servers.py`

```bash
# Add ECS server (type:id:port[:weight[:description]])
python3 scripts/add_servers.py --region cn-hangzhou --sg-id sgp-xxx \
    --server ecs:i-xxx:8080

# Add multiple servers with weight
python3 scripts/add_servers.py --region cn-hangzhou --sg-id sgp-xxx \
    --server ecs:i-xxx:8080:100:web-1 \
    --server ecs:i-yyy:8080:50:web-2

# Add IP-based server (for Ip-type server group)
python3 scripts/add_servers.py --region cn-hangzhou --sg-id sgp-xxx \
    --server ip:10.0.1.100:8080
```

**Remove backend servers** — `scripts/remove_servers.py`

```bash
# Remove server (type:id:port)
python3 scripts/remove_servers.py --region cn-hangzhou --sg-id sgp-xxx \
    --server ecs:i-xxx:8080

# Remove multiple servers
python3 scripts/remove_servers.py --region cn-hangzhou --sg-id sgp-xxx \
    --server ecs:i-xxx:8080 --server ecs:i-yyy:8080
```

### Forwarding Rules

**List rules** — `scripts/list_rules.py`

```bash
# By load balancer
python3 scripts/list_rules.py --region cn-hangzhou --lb-id alb-xxx

# By listener
python3 scripts/list_rules.py --region cn-hangzhou --listener-id lsn-xxx
```

**Create forwarding rule** — `scripts/create_rule.py`

```bash
# Block DELETE method with 405 response
python3 scripts/create_rule.py --region cn-hangzhou --listener-id lsn-xxx \
    --name "block-delete" --priority 10 \
    --condition-method DELETE \
    --action-fixed-response "405 Method Not Allowed"

# Host-based routing to server group
python3 scripts/create_rule.py --region cn-hangzhou --listener-id lsn-xxx \
    --name "api-route" --priority 20 \
    --condition-host "api.example.com" \
    --action-forward-to sgp-xxx

# Path-based routing
python3 scripts/create_rule.py --region cn-hangzhou --listener-id lsn-xxx \
    --name "api-v1-route" --priority 30 \
    --condition-host "api.example.com" --condition-path "/v1/*" \
    --action-forward-to sgp-xxx

# HTTP to HTTPS redirect
python3 scripts/create_rule.py --region cn-hangzhou --listener-id lsn-xxx \
    --name "force-https" --priority 5 \
    --action-redirect "https 443"
```

**Update forwarding rule** — `scripts/update_rule.py`

```bash
# Update rule name and priority
python3 scripts/update_rule.py --region cn-hangzhou --rule-id rule-xxx \
    --name "new-name" --priority 50

# Change forwarding target
python3 scripts/update_rule.py --region cn-hangzhou --rule-id rule-xxx \
    --action-forward-to sgp-new

# Update conditions and actions together
python3 scripts/update_rule.py --region cn-hangzhou --rule-id rule-xxx \
    --condition-host "new.example.com" \
    --action-forward-to sgp-new
```

**Delete forwarding rule** — `scripts/delete_rule.py`

```bash
python3 scripts/delete_rule.py --region cn-hangzhou --rule-id rule-xxx
python3 scripts/delete_rule.py --region cn-hangzhou --rule-id rule-xxx --yes  # skip confirm
```

### Health Check

**Check health status** — `scripts/check_health_status.py`

```bash
# All listeners
python3 scripts/check_health_status.py --region cn-hangzhou --lb-id alb-xxx

# Specific listener
python3 scripts/check_health_status.py --region cn-hangzhou --lb-id alb-xxx --listener-id lsn-xxx

# JSON output (includes rule-level health status)
python3 scripts/check_health_status.py --region cn-hangzhou --lb-id alb-xxx --json
```

### Certificates

**List listener certificates** — `scripts/list_listener_certificates.py`

```bash
python3 scripts/list_listener_certificates.py --region cn-hangzhou --listener-id lsn-xxx
```

### Security Policies

**List security policies** — `scripts/list_security_policies.py`

```bash
# Custom policies only
python3 scripts/list_security_policies.py --region cn-hangzhou

# Include system predefined policies
python3 scripts/list_security_policies.py --region cn-hangzhou --system
```

### Access Control (ACL)

**List ACLs** — `scripts/list_acls.py`

```bash
python3 scripts/list_acls.py --region cn-hangzhou
python3 scripts/list_acls.py --region cn-hangzhou --acl-ids acl-aaa acl-bbb
```

**List ACL entries** — `scripts/list_acl_entries.py`

```bash
python3 scripts/list_acl_entries.py --region cn-hangzhou --acl-id acl-xxx
```

### Async Job Polling

Most ALB write operations (create/update/delete listener, rule, ALB instance) return a `job_id`. Use `wait_for_job.py` to poll until the job completes.

**Wait for async job** — `scripts/wait_for_job.py`

```bash
# Wait for a job (default 120s timeout)
python3 scripts/wait_for_job.py --region cn-hangzhou --job-id 606f647c-xxxx-xxxx

# Custom timeout and interval
python3 scripts/wait_for_job.py --region cn-hangzhou --job-id xxx --timeout 300 --interval 3

# JSON output
python3 scripts/wait_for_job.py --region cn-hangzhou --job-id xxx --json

# Write result to file
python3 scripts/wait_for_job.py --region cn-hangzhou --job-id xxx --json --output result.json
```

Job statuses: `Processing` → `Succeeded` / `Failed`. Exit code 0 on success, 1 on failure/timeout.

## Write Operations Cookbook

Step-by-step guide to build a complete ALB from scratch. Full dependency graph: `references/resource-dependencies.md`.

> Prerequisites: VPC, VSwitches, backend instances (ECS/ENI/ECI), and SSL certificates (for HTTPS) must already exist.

### Step 1: Create independent resources (parallelizable)

**1a. Create Server Group** → yields `ServerGroupId`

```python
resp = client.create_server_group(alb_models.CreateServerGroupRequest(
    server_group_name="my-sg",
    vpc_id="vpc-xxx",
    protocol="HTTP",
    scheduler="Wrr",
    health_check_config=alb_models.CreateServerGroupRequestHealthCheckConfig(
        health_check_enabled=True,
        health_check_path="/health",
        health_check_codes=["http_2xx", "http_3xx"],
    ),
))
server_group_id = resp.body.server_group_id
```

**1b. Create ACL (if needed)** → yields `AclId`

```python
resp = client.create_acl(alb_models.CreateAclRequest(acl_name="my-acl"))
acl_id = resp.body.acl_id

# Add IP entries
client.add_entries_to_acl(alb_models.AddEntriesToAclRequest(
    acl_id=acl_id,
    acl_entries=[
        alb_models.AddEntriesToAclRequestAclEntries(entry="10.0.0.0/8", description="internal"),
        alb_models.AddEntriesToAclRequestAclEntries(entry="203.0.113.1/32", description="office"),
    ],
))
```

### Step 2: Add backends to Server Group

```python
client.add_servers_to_server_group(alb_models.AddServersToServerGroupRequest(
    server_group_id=server_group_id,  # ← Step 1a
    servers=[alb_models.AddServersToServerGroupRequestServers(
        server_type="Ecs",
        server_id="i-xxx",
        port=8080,
        weight=100,
    )],
))
```

### Step 3: Create ALB instance → yields `LoadBalancerId`

```python
resp = client.create_load_balancer(alb_models.CreateLoadBalancerRequest(
    load_balancer_name="my-alb",
    address_type="Internet",       # Internet | Intranet
    load_balancer_edition="Standard",  # Basic | Standard | StandardWithWaf
    vpc_id="vpc-xxx",
    load_balancer_billing_config=alb_models.CreateLoadBalancerRequestLoadBalancerBillingConfig(
        pay_type="PostPay",
    ),
    zone_mappings=[
        alb_models.CreateLoadBalancerRequestZoneMappings(zone_id="cn-hangzhou-h", v_switch_id="vsw-aaa"),
        alb_models.CreateLoadBalancerRequestZoneMappings(zone_id="cn-hangzhou-i", v_switch_id="vsw-bbb"),
    ],
))
load_balancer_id = resp.body.load_balancer_id
# ⚠️ Async operation — poll GetLoadBalancerAttribute until LoadBalancerStatus == "Active"
```

### Step 4: Enable Access Log (optional)

```python
client.enable_load_balancer_access_log(alb_models.EnableLoadBalancerAccessLogRequest(
    load_balancer_id=load_balancer_id,  # ← Step 3
    log_project="my-sls-project",
    log_store="alb-access-log",
))
```

### Step 5: Create Listener → yields `ListenerId`

```python
# HTTPS Listener (for HTTP, omit the certificates parameter)
resp = client.create_listener(alb_models.CreateListenerRequest(
    load_balancer_id=load_balancer_id,  # ← Step 3
    listener_protocol="HTTPS",
    listener_port=443,
    default_actions=[alb_models.CreateListenerRequestDefaultActions(
        type="ForwardGroup",
        forward_group_config=alb_models.CreateListenerRequestDefaultActionsForwardGroupConfig(
            server_group_tuples=[alb_models.CreateListenerRequestDefaultActionsForwardGroupConfigServerGroupTuples(
                server_group_id=server_group_id,  # ← Step 1a
            )],
        ),
    )],
    certificates=[alb_models.CreateListenerRequestCertificates(certificate_id="cert-xxx")],
))
listener_id = resp.body.listener_id
# ⚠️ Async operation — poll GetListenerAttribute until ListenerStatus == "Running"
```

### Step 6: Configure Listener sub-resources (parallelizable)

**6a. Create Forwarding Rule**

```python
client.create_rule(alb_models.CreateRuleRequest(
    listener_id=listener_id,  # ← Step 5
    rule_name="api-route",
    priority=10,
    rule_conditions=[alb_models.CreateRuleRequestRuleConditions(
        type="Host",
        host_config=alb_models.CreateRuleRequestRuleConditionsHostConfig(values=["api.example.com"]),
    )],
    rule_actions=[alb_models.CreateRuleRequestRuleActions(
        type="ForwardGroup",
        order=1,
        forward_group_config=alb_models.CreateRuleRequestRuleActionsForwardGroupConfig(
            server_group_tuples=[alb_models.CreateRuleRequestRuleActionsForwardGroupConfigServerGroupTuples(
                server_group_id=server_group_id,  # ← Step 1a (or another ServerGroup)
            )],
        ),
    )],
))
```

**6b. Associate ACL**

```python
client.associate_acls_with_listener(alb_models.AssociateAclsWithListenerRequest(
    listener_id=listener_id,  # ← Step 5
    acl_type="White",          # White (whitelist) | Black (blacklist)
    acl_ids=[acl_id],          # ← Step 1b
))
```

### Teardown (reverse order)

Must delete from leaf resources first. See `references/resource-dependencies.md` for the full deletion sequence.

```python
# 1. Detach Listener sub-resources
client.dissociate_acls_from_listener(alb_models.DissociateAclsFromListenerRequest(
    listener_id="lsn-xxx", acl_ids=["acl-xxx"],
))
client.delete_rule(alb_models.DeleteRuleRequest(rule_id="rule-xxx"))

# 2. Delete Listener
client.delete_listener(alb_models.DeleteListenerRequest(listener_id="lsn-xxx"))

# 3. Delete ALB (disable deletion protection first)
client.disable_deletion_protection(alb_models.DisableDeletionProtectionRequest(resource_id="alb-xxx"))
client.delete_load_balancer(alb_models.DeleteLoadBalancerRequest(load_balancer_id="alb-xxx"))

# 4. Delete independent resources
client.remove_servers_from_server_group(alb_models.RemoveServersFromServerGroupRequest(
    server_group_id="sgp-xxx",
    servers=[alb_models.RemoveServersFromServerGroupRequestServers(
        server_type="Ecs", server_id="i-xxx", port=8080,
    )],
))
client.delete_server_group(alb_models.DeleteServerGroupRequest(server_group_id="sgp-xxx"))
client.delete_acl(alb_models.DeleteAclRequest(acl_id="acl-xxx"))
```

### Common operations

```python
# Start / Stop Listener
client.start_listener(alb_models.StartListenerRequest(listener_id="lsn-xxx"))
client.stop_listener(alb_models.StopListenerRequest(listener_id="lsn-xxx"))

# Disable Access Log
client.disable_load_balancer_access_log(alb_models.DisableLoadBalancerAccessLogRequest(
    load_balancer_id="alb-xxx",
))
```

### Update operations

**Update Listener (timeout, security policy, HTTP/2)**

```python
client.update_listener_attribute(alb_models.UpdateListenerAttributeRequest(
    listener_id="lsn-xxx",
    idle_timeout=60,                # seconds
    request_timeout=120,            # seconds
    security_policy_id="tls_cipher_policy_1_2",  # HTTPS only
    http_2enabled=True,             # HTTPS only
))
```

**Update Server Group (health check, scheduler, sticky session)**

```python
client.update_server_group_attribute(alb_models.UpdateServerGroupAttributeRequest(
    server_group_id="sgp-xxx",
    scheduler="Wrr",                # Wrr | Wlc | Sch | Uch
    health_check_config=alb_models.UpdateServerGroupAttributeRequestHealthCheckConfig(
        health_check_enabled=True,
        health_check_path="/health",
        health_check_interval=5,
        healthy_threshold=3,
        unhealthy_threshold=3,
        health_check_codes=["http_2xx", "http_3xx"],
    ),
    sticky_session_config=alb_models.UpdateServerGroupAttributeRequestStickySessionConfig(
        sticky_session_enabled=True,
        sticky_session_type="Server",  # Server | Insert
        cookie="SERVERID",
    ),
))
```

**Update backend server weight (blue-green, canary)**

```python
client.update_server_group_servers_attribute(alb_models.UpdateServerGroupServersAttributeRequest(
    server_group_id="sgp-xxx",
    servers=[alb_models.UpdateServerGroupServersAttributeRequestServers(
        server_type="Ecs",
        server_id="i-xxx",
        port=8080,
        weight=50,  # adjust weight for traffic shifting
    )],
))
```

**Update forwarding rule (blue-green weight switching)**

```python
client.update_rule_attribute(alb_models.UpdateRuleAttributeRequest(
    rule_id="rule-xxx",
    rule_actions=[alb_models.UpdateRuleAttributeRequestRuleActions(
        type="ForwardGroup",
        order=1,
        forward_group_config=alb_models.UpdateRuleAttributeRequestRuleActionsForwardGroupConfig(
            server_group_tuples=[
                alb_models.UpdateRuleAttributeRequestRuleActionsForwardGroupConfigServerGroupTuples(
                    server_group_id="sgp-blue", weight=80,
                ),
                alb_models.UpdateRuleAttributeRequestRuleActionsForwardGroupConfigServerGroupTuples(
                    server_group_id="sgp-green", weight=20,
                ),
            ],
        ),
    )],
))
```

### HTTP → HTTPS redirect pattern

```python
# Create HTTP:80 listener that redirects all traffic to HTTPS:443
client.create_listener(alb_models.CreateListenerRequest(
    load_balancer_id=load_balancer_id,
    listener_protocol="HTTP",
    listener_port=80,
    default_actions=[alb_models.CreateListenerRequestDefaultActions(
        type="Redirect",
        redirect_config=alb_models.CreateListenerRequestDefaultActionsRedirectConfig(
            protocol="HTTPS",
            port="443",
            http_redirect_code="301",
        ),
    )],
))
```

### QUIC listener

```python
# QUIC listener (requires an existing HTTPS listener on the same ALB)
client.create_listener(alb_models.CreateListenerRequest(
    load_balancer_id=load_balancer_id,
    listener_protocol="QUIC",
    listener_port=443,
    default_actions=[alb_models.CreateListenerRequestDefaultActions(
        type="ForwardGroup",
        forward_group_config=alb_models.CreateListenerRequestDefaultActionsForwardGroupConfig(
            server_group_tuples=[alb_models.CreateListenerRequestDefaultActionsForwardGroupConfigServerGroupTuples(
                server_group_id=server_group_id,
            )],
        ),
    )],
    certificates=[alb_models.CreateListenerRequestCertificates(certificate_id="cert-xxx")],
))
# Note: QUIC Client Hello must be ≥ 1024 bytes; see troubleshooting doc for details
```

### Health Check Template

```python
# Create a reusable health check template
resp = client.create_health_check_template(alb_models.CreateHealthCheckTemplateRequest(
    health_check_template_name="standard-http-check",
    health_check_protocol="HTTP",
    health_check_path="/health",
    health_check_method="HEAD",
    health_check_codes=["http_2xx", "http_3xx"],
    health_check_interval=5,
    health_check_timeout=3,
    healthy_threshold=3,
    unhealthy_threshold=3,
))
template_id = resp.body.health_check_template_id

# Apply template to a server group
client.apply_health_check_template_to_server_group(
    alb_models.ApplyHealthCheckTemplateToServerGroupRequest(
        server_group_id="sgp-xxx",
        health_check_template_id=template_id,
    )
)
```

## Log Analysis

ALB access log analysis is handled by the `alicloud-observability-sls-log-query` skill.

Get log config from `GetLoadBalancerAttribute`:
- `AccessLogConfig.LogProject` → SLS Project
- `AccessLogConfig.LogStore` → SLS Logstore

Common query templates: see `references/log-analysis.md`.

## Troubleshooting

See `references/troubleshooting.md` for:

1. Cannot access service / connectivity checklist
2. High latency diagnosis
3. Health check failures (first-time config, iptables blocking, source IPs)
4. HTTP status codes — full ALB error reference (400/405/408/414/463/499/500/502/503/504)
5. Certificate & HTTPS issues (expiry, wildcard rules, SNI, WAF sync)
6. Forwarding rule conflicts
7. ACL access control issues
8. Request limits (URI, header, body, keep-alive)
9. WAF integration (2.0 vs 3.0)
10. EIP & bandwidth

## API Reference

Full API list: `references/api_quick_map.md`.

## Output And Evidence

- Save outputs under `output/alicloud-network-alb/`.
- Keep command parameters and region scope in evidence files.
