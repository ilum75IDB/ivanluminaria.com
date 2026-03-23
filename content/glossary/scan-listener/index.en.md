---
title: "SCAN Listener"
description: "Single Client Access Name — Oracle RAC component that provides a single access point to the cluster, distributing connections across available nodes."
translationKey: "glossary_scan_listener"
aka: "Single Client Access Name"
articles:
  - "/posts/oracle/oracle-cloud-migration"
---

The **SCAN Listener** (Single Client Access Name) is the Oracle RAC component that provides a single DNS name for cluster access. Applications connect to the SCAN name without needing to know individual nodes: the listener automatically distributes connections among active nodes.

## How it works

SCAN is a DNS name that resolves to three virtual IP addresses (VIPs) distributed across cluster nodes. When a client connects to the SCAN name, DNS returns one of the three IPs, and the listener on that IP redirects the connection to the most appropriate node based on the requested service and load.

The advantage is that application connection strings never change: if a node is added to or removed from the cluster, SCAN handles everything transparently.

## Typical configuration

A connection string using SCAN:

    jdbc:oracle:thin:@//scan-name.example.com:1521/service_name

The three SCAN VIPs run on any cluster node. In a two-node cluster, one node hosts two VIPs and the other hosts one (or vice versa).

## In migrations

In OCI migrations, the SCAN listener is reconfigured with the new infrastructure's DNS. It's one of the cutover steps: updating connection strings to point to the new SCAN name on OCI. If naming is well managed, it's a change in a single place (the application's connection pool), not in dozens of scattered configuration files.
