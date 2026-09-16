---
title: "REM"
description: "BASIC instruction that introduces a comment in source code: the line is ignored by the interpreter and exists solely to document the program."
translationKey: "glossary_rem"
aka: "REMark"
articles:
  - "/posts/project-management/il-dottore-tutto-pazzo-un-commodore-64-una-porta-chiusa-e-il-mestiere-di-capire"
---

`REM` is a BASIC language instruction — short for **REMark** — that marks a line as a comment in the source code. The interpreter skips the entire line without executing anything: no output, no computation, no side effects. Its sole purpose is to communicate intent to whoever reads the listing.

## How it works

When the BASIC interpreter encounters `REM`, it advances to the next line number and continues execution from there. In most dialects (Commodore BASIC, GW-BASIC, QBasic), a line number precedes the instruction:

```basic
10 REM VAT calculation program
20 LET RATE = 0.22
30 REM Enter the net price
40 INPUT PRICE
50 LET VAT = PRICE * RATE
60 PRINT "VAT: "; VAT
```

Several dialects also accept a shorthand apostrophe (`'`) as a synonym for `REM`, behaving identically at runtime.

## When it matters

`REM` was often the only mechanism available to leave a human-readable explanation inside a program at a time when IDEs, diff tools, and version control systems did not exist. A listing without `REM` statements could become opaque even to its original author within weeks.

Today `REM` is primarily a historical and cultural reference: it marks the origin of inline code documentation, a practice that evolved in modern languages into docstrings, annotations, and structured comment formats.
