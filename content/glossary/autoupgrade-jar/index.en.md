---
title: "autoupgrade.jar"
description: "Oracle command-line tool that automates database upgrades. In analyze mode it scans the source instance and produces a compatibility report with no changes applied."
translationKey: "glossary_autoupgrade_jar"
aka: "Oracle AutoUpgrade Utility"
articles:
  - "/posts/oracle/oracle-11g-r2-19c-su-oci-8-tb-in-finanza-un-piano-di-upgrade-con-fasi-e-rollback"
---

`autoupgrade.jar` is the Oracle-distributed JAR utility that automates the full database upgrade lifecycle, from pre-migration checks through to completion. It replaces the older manual `dbupgrade` scripts and significantly reduces human error risk in large-scale upgrade operations.

## How it works

The tool is invoked via `java -jar autoupgrade.jar` with a configuration file describing source and target environments. It supports three primary modes:

```bash
# Analyze mode: read-only, no changes to the instance
java -jar autoupgrade.jar -config upgrade.cfg -mode analyze

# Fixups mode: applies pre-upgrade corrections identified during analysis
java -jar autoupgrade.jar -config upgrade.cfg -mode fixups

# Deploy mode: executes the full upgrade
java -jar autoupgrade.jar -config upgrade.cfg -mode deploy
```

In `analyze` mode, the tool queries system views, checks object compatibility, validates initialization parameters, and produces an HTML/text report listing detected issues and recommended actions. No writes are performed against the source database.

## When to use it

The `analyze` mode is the go-to instrument during the **pre-migration assessment** phase: it allows multiple analysis passes against production environments with no downtime and no risk. It is especially relevant when the source database is still on 11g or 12c and the target is 19c, since the version gap increases the number of deprecations and incompatibilities to address.

In financial environments with multi-TB tablespaces, the generated report feeds directly into the rollback plan and maintenance window estimation.
