---
title: "?SYNTAX ERROR"
description: "Commodore 64 BASIC error message signaling a syntax rule violation, pointing to the line where the interpreter detected the problem."
translationKey: "glossary_syntax_error"
aka: "Syntax Error (Commodore BASIC)"
articles:
  - "/posts/project-management/il-dottore-tutto-pazzo-un-commodore-64-una-porta-chiusa-e-il-mestiere-di-capire"
---

`?SYNTAX ERROR` is the message the Commodore 64 BASIC interpreter emits when a line of code violates the language's grammatical rules. The leading question mark is part of the standard Commodore error format (KERNAL + BASIC V2), not a typographical quirk.

## How it works

The C64 BASIC interpreter processes code line by line, either at runtime or when a statement is entered in direct mode. When it encounters an unrecognizable token — a misspelled keyword, an unbalanced parenthesis, a misplaced operator — it halts and prints the message followed by the offending line number:

```
?SYNTAX ERROR IN 100
READY.
```

The line number shown is where the interpreter *detected* the problem, not necessarily where it *originated*. An incomplete expression on line 90 can surface as an error on line 100, where the interpreter tries to consume tokens that are no longer available.

## Operational context

When debugging BASIC programs on the C64, `?SYNTAX ERROR` is often a misleading starting point: the reported line must be read alongside the preceding lines, especially with multi-token constructs like `IF...THEN`, `FOR...NEXT`, or command chains separated by `:`. The absence of a symbolic debugger makes the entire process manual. This behavior — the error reported somewhere other than its root cause — is a pattern that recurs across sequential parsing systems, from compilers to SQL engines, and is a reminder not to trust reported line numbers at face value.
