# ALB API Quick Map (2020-06-16)

## Regions & Zones (2)

- `DescribeRegions` — Query available regions
- `DescribeZones` — Query available zones in a region

## Load Balancer Instances (16)

- `CreateLoadBalancer` — Create an ALB instance
- `DeleteLoadBalancer` — Delete an ALB instance
- `GetLoadBalancerAttribute` — Query instance details (including ZoneMappings/VIP)
- `ListLoadBalancers` — List instances
- `UpdateLoadBalancerAttribute` — Modify instance attributes
- `UpdateLoadBalancerZones` — Modify availability zone configuration
- `UpdateLoadBalancerEdition` — Change edition (Basic/Standard/StandardWithWaf)
- `UpdateLoadBalancerAddressTypeConfig` — Switch network type (public/private)
- `EnableDeletionProtection` — Enable deletion protection
- `DisableDeletionProtection` — Disable deletion protection
- `StartShiftLoadBalancerZones` — Remove a zone from DNS resolution (Zone Shift)
- `CancelShiftLoadBalancerZones` — Restore zone DNS resolution
- `EnableLoadBalancerIpv6Internet` — Switch dual-stack IPv6 to public
- `DisableLoadBalancerIpv6Internet` — Switch dual-stack IPv6 to private
- `LoadBalancerJoinSecurityGroup` — Associate a security group
- `LoadBalancerLeaveSecurityGroup` — Disassociate a security group

## Listeners (9)

- `CreateListener` — Create a listener
- `DeleteListener` — Delete a listener
- `GetListenerAttribute` — Query listener details (including certificates/ACL)
- `ListListeners` — List listeners
- `StartListener` — Start a listener
- `StopListener` — Stop a listener
- `UpdateListenerAttribute` — Modify listener configuration
- `UpdateListenerLogConfig` — Modify listener log configuration
- `GetListenerHealthStatus` — Query listener health check status

## Server Groups (9)

- `CreateServerGroup` — Create a server group
- `DeleteServerGroup` — Delete a server group
- `UpdateServerGroupAttribute` — Modify server group configuration (health check/session persistence/scheduling algorithm, etc.)
- `UpdateServerGroupServersAttribute` — Modify backend server weight and description
- `ListServerGroups` — List server groups
- `ListServerGroupServers` — List backend servers in a server group
- `AddServersToServerGroup` — Add backend servers
- `RemoveServersFromServerGroup` — Remove backend servers
- `ReplaceServersInServerGroup` — Replace backend servers

## Forwarding Rules (7)

- `CreateRule` — Create a forwarding rule
- `CreateRules` — Create forwarding rules in batch
- `DeleteRule` — Delete a forwarding rule
- `DeleteRules` — Delete forwarding rules in batch
- `UpdateRuleAttribute` — Modify a forwarding rule
- `UpdateRulesAttribute` — Modify forwarding rules in batch
- `ListRules` — List forwarding rules

## Listener Certificates (3)

- `AssociateAdditionalCertificatesWithListener` — Associate additional certificates (SNI)
- `DissociateAdditionalCertificatesFromListener` — Disassociate additional certificates
- `ListListenerCertificates` — List certificates associated with a listener

## Common Bandwidth Packages (2)

- `AttachCommonBandwidthPackageToLoadBalancer` — Associate a shared bandwidth package
- `DetachCommonBandwidthPackageFromLoadBalancer` — Disassociate a shared bandwidth package

## Access Logs (2)

- `EnableLoadBalancerAccessLog` — Enable access logs
- `DisableLoadBalancerAccessLog` — Disable access logs

## Health Check Templates (6)

- `CreateHealthCheckTemplate` — Create a health check template
- `GetHealthCheckTemplateAttribute` — Query health check template details
- `DeleteHealthCheckTemplates` — Delete health check templates in batch
- `UpdateHealthCheckTemplateAttribute` — Modify a health check template
- `ListHealthCheckTemplates` — List health check templates
- `ApplyHealthCheckTemplateToServerGroup` — Apply a template to a server group

## Security Policies (6)

- `CreateSecurityPolicy` — Create a custom TLS security policy
- `DeleteSecurityPolicy` — Delete a security policy
- `UpdateSecurityPolicyAttribute` — Modify a security policy (TLS versions/cipher suites)
- `ListSecurityPolicies` — List custom security policies
- `ListSecurityPolicyRelations` — Query listeners associated with a security policy
- `ListSystemSecurityPolicies` — List system predefined security policies

## Access Control / ACL (10)

- `CreateAcl` — Create an access control list
- `DeleteAcl` — Delete an ACL
- `UpdateAclAttribute` — Modify ACL attributes
- `ListAcls` — List ACLs
- `ListAclEntries` — List IP entries in an ACL
- `AddEntriesToAcl` — Add IP entries
- `RemoveEntriesFromAcl` — Remove IP entries
- `AssociateAclsWithListener` — Associate ACLs with a listener
- `DissociateAclsFromListener` — Disassociate ACLs from a listener
- `ListAclRelations` — Query listeners associated with an ACL

## Tags (5)

- `TagResources` — Tag resources
- `UnTagResources` — Remove tags
- `ListTagResources` — Query resource tags
- `ListTagKeys` — Query tag keys
- `ListTagValues` — Query tag values

## Resource Groups (1)

- `MoveResourceGroup` — Move a resource to another resource group

## Async Jobs (1)

- `ListAsynJobs` — Query async jobs

## Capacity Reservation (2)

- `ModifyCapacityReservation` — Create or modify capacity reservation
- `DescribeCapacityReservation` — Query capacity reservation details

## Programmable Scripts / AScript (4)

- `CreateAScripts` — Create programmable scripts
- `UpdateAScripts` — Modify programmable scripts
- `DeleteAScripts` — Delete programmable scripts
- `ListAScripts` — List programmable scripts
