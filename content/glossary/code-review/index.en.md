---
title: "Code Review"
description: "Practice of reviewing code by a colleague before merging, to catch bugs, improve quality and share knowledge within the team."
translationKey: "glossary_code-review"
articles:
  - "/posts/project-management/ai-github-project-management"
---

**Code Review** is the practice where a colleague examines code written by another developer before it is incorporated into the main branch. On GitHub it happens inside Pull Requests.

## How it works

The developer opens a Pull Request with their changes. An assigned reviewer examines the code diff, leaves comments, suggests improvements and eventually approves or requests changes. The process is asynchronous: no meetings needed, the review happens on the tool. Only after approval is the code merged into the main branch.

## What it's for

Code review catches bugs that automated tests don't find, improves code quality, and — an often underestimated aspect — spreads codebase knowledge across the team. If only one person knows a module and they leave, the project has a problem. With code reviews, at least two people know every piece of code.

## When to use it

On every Pull Request, without exceptions. It's not a formality: it's an investment in quality. Time spent in review is always less than time spent fixing bugs in production discovered too late.
