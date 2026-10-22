---
title: "DNS"
description: "DNS (Domain Name System) resolves human-readable hostnames to IP addresses, enabling network connectivity for databases, Oracle listeners, and OCI cloud services."
translationKey: "glossary_dns"
aka: "Domain Name System"
articles:
  - "/posts/oracle/oracle-11g-r2-19c-su-oci-8-tb-in-finanza-un-piano-di-upgrade-con-fasi-e-rollback"
---

DNS (Domain Name System) is the distributed system that resolves symbolic hostnames into IP addresses. In database and cloud infrastructure contexts, it is the underlying mechanism that allows clients, applications, and administration tools to reach Oracle instances, OCI endpoints, and network services without hardcoding static IP addresses into connection strings.

## How it works

When an Oracle client attempts to connect to a host via `tnsnames.ora` or Easy Connect, the operating system queries the configured DNS resolver. The resolver traverses the DNS hierarchy (root → TLD → authoritative server) and returns the IP address corresponding to the hostname.

```bash
# Verify DNS resolution for an Oracle listener on OCI
nslookup db-prod.subnet.vcn.oraclevcn.com
dig +short db-prod.subnet.vcn.oraclevcn.com A
```

In OCI, each VCN includes a built-in DNS resolver that automatically manages records for tenant resources (DB Systems, Autonomous Database, Load Balancers).

## Operational context

During an Oracle 11g R2 → 19c upgrade on OCI, DNS becomes critical at three key points:

- **New DB System provisioning**: the target 19c hostname must be resolvable by all clients and migration jobs before data transfer begins.
- **Cutover and ROLLBACK**: if the plan uses a CNAME or DNS alias as the application access point, updating that record (with a pre-set low TTL) is the fastest and most reversible switch mechanism.
- **Cross-subnet connections**: in multi-tier architectures, OCI firewall rules and security lists must allow UDP/TCP traffic on port 53 to the VCN resolver.

A high TTL on DNS records can slow down a ROLLBACK: reducing it to 60–300 seconds in the hours before cutover is standard practice in low-risk migration plans.
