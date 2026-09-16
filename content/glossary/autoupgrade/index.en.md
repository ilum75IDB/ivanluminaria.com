---
title: "AutoUpgrade"
description: "Java utility (autoupgrade.jar) that from Oracle 21c is the single tool for pre-upgrade analysis, fixes and database upgrade. Replaces preupgrade.jar, no longer distributed."
translationKey: "glossary_autoupgrade"
aka: "AutoUpgrade Utility (autoupgrade.jar)"
articles:
  - "/posts/oracle/oracle-12c-21c-su-12-tb-transportable-tablespaces-rman-incremental-e-la"
---

AutoUpgrade is the Java utility shipped with Oracle Database that from 21c onwards has become the single tool for managing the entire upgrade lifecycle: pre-upgrade analysis, automatic remediation of detected issues, upgrade execution and post-upgrade fix-ups. It permanently replaces `preupgrade.jar`, no longer distributed in recent releases.

## How it works

AutoUpgrade operates in four main modes, controlled by the `-mode` parameter:

- **`analyze`** — read-only, produces a compatibility report without modifying anything. This is the mode to use in production weeks before the upgrade window.
- **`fixups`** — applies automatic corrections to issues resolvable without human intervention (e.g. recompiling invalid objects, removing deprecated components).
- **`deploy`** — performs the full upgrade from source to target database.
- **`upgrade`** — runs only the dictionary upgrade phase, skipping fixups and post-upgrade tasks.

```bash
# Pre-upgrade analysis (read-only, safe in production)
java -jar $ORACLE_HOME_21C/rdbms/admin/autoupgrade.jar \
  -preupgrade "target_version=21,dir=/tmp/preupg" -mode analyze

# Full upgrade from a config file
java -jar $ORACLE_HOME_21C/rdbms/admin/autoupgrade.jar \
  -config upgrade.cfg -mode deploy
```

## When to use it

In every Oracle upgrade scenario from 12.2 or above towards 19c, 21c, 23ai. The most common use case is `analyze` mode as the first step of any migration project: it produces a detailed report of invalid objects, obsolete parameters, components to remove and application-level incompatibilities. The report must be read and discussed with application developers before planning the downtime window — many of the fixes require changes to customer code that cannot be applied during the cutover weekend.
