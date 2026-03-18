---
title: "Pull Request"
description: "Mechanism for proposing and reviewing code changes on platforms like GitHub. Enables code review, discussion and approval before merging into the main branch."
translationKey: "glossary_pull-request"
aka: "PR, Merge Request"
articles:
  - "/posts/project-management/ai-github-project-management"
---

A **Pull Request** (PR) is a formal request to incorporate changes from a development branch into the repository's main branch. It is the central collaboration mechanism on GitHub and similar platforms.

## How it works

The developer works on a dedicated branch (e.g. `fix/issue-234-calculation-error`), completes the changes, and opens a PR. The PR shows the code diff, allows colleagues to comment line by line, request changes or approve. Only after approval is the code merged into the main branch. This ensures that "good" code stays good.

## What it's for

The PR transforms development from an individual activity into a team process. It prevents accidental overwrites, catches bugs before they reach production, and creates a complete history of who did what, when and why. In chaotic projects, it's the difference between control and disorder.

## When to use it

On every code change, without exceptions. Even small fixes go through a PR, because the value is not just in the review but in traceability. On GitLab platforms the same functionality is called Merge Request.
