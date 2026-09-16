---
title: "BASIC"
description: "BASIC is an interpreted programming language from the 1980s, designed for home computers with numbered lines and human-readable syntax accessible to non-specialists."
translationKey: "glossary_basic"
aka: "Beginner's All-purpose Symbolic Instruction Code"
articles:
  - "/posts/project-management/il-dottore-tutto-pazzo-un-commodore-64-una-porta-chiusa-e-il-mestiere-di-capire"
---

BASIC (Beginner's All-purpose Symbolic Instruction Code) is a programming language created in 1964 at Dartmouth College that became the dominant language on home computers throughout the 1980s. On machines like the Commodore 64, ZX Spectrum, or Apple II, BASIC was often the only development environment available at boot time.

## How it works

BASIC programs are sequences of numbered lines, executed in ascending order by the interpreter. The line number also serves as the target for conditional jumps (`GOTO`) and subroutine calls (`GOSUB`).

```basic
10 PRINT "Enter a number: "
20 INPUT N
30 IF N > 10 THEN GOTO 60
40 PRINT "Small number"
50 GOTO 70
60 PRINT "Large number"
70 END
```

The interpreter reads and executes each line at runtime, with no separate compilation step. This makes the edit-run cycle immediate, but performance suffers compared to compiled languages.

## Operational context

BASIC was designed for non-specialist users: students, hobbyists, and professionals who wanted to automate calculations without formal programming training. The simplicity of the syntax came at a clear cost — no complex data structures, manual memory management via `PEEK` and `POKE`, and a reliance on `GOTO` that made programs beyond a few hundred lines difficult to maintain.

In 1980s business environments, BASIC was used for basic management software, rudimentary spreadsheets, and report automation on minicomputers. Today it survives in embedded environments and modern dialects such as FreeBASIC or QB64, but its most significant historical role was introducing an entire generation to programming as a practical everyday tool.
