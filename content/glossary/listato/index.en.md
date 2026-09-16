---
title: "Listing"
description: "Complete source code printed or displayed line by line. In 1980s home computing, listings were published in magazines to be typed in manually by readers."
translationKey: "glossary_listato"
aka: "program listing, source listing"
articles:
  - "/posts/project-management/il-dottore-tutto-pazzo-un-commodore-64-una-porta-chiusa-e-il-mestiere-di-capire"
---

A **listing** is the complete textual representation of a program's source code, presented line by line in the order an interpreter or compiler processes it. The term was standard in computing from the 1970s through the 1980s, when printing or publishing code was the primary distribution method available to the general public.

## How it works

On 8-bit home computers (Commodore 64, ZX Spectrum, MSX), a listing typically meant a line-numbered BASIC program:

```basic
10 PRINT "HELLO WORLD"
20 GOTO 10
```

Magazines such as *COMPUTE!* or *Your Commodore* published listings spanning dozens of pages. Readers typed them in manually, keystroke by keystroke. A single mistyped character could render the program broken or produce unpredictable behavior — with no copy-paste, no diff tool, and no version control to help locate the mistake.

## Operational context

The listing as a software distribution mechanism is historically significant for understanding the debugging culture of the era. Errors were hunted by visually comparing the typed text against the printed page, line by line, with close attention to syntactic detail. That discipline — reading code carefully rather than running it and hoping for the best — maps directly onto skills that remain relevant today: reviewing SQL migration scripts, auditing configuration files, or tracing logic in stored procedures.

In modern technical usage the term survives in IDE "Listing" export features and informally to describe full schema dumps (e.g., the output of `pg_dump` as a "listing" of a PostgreSQL schema).
