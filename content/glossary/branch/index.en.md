---
title: "Branch"
description: "Independent development line in a version control system. Allows working on isolated changes without affecting the main code until merge."
translationKey: "glossary_branch"
articles:
  - "/posts/project-management/ai-github-project-management"
---

A **Branch** is an independent development line in a Git repository. Each branch contains a copy of the code that can be worked on without affecting the main branch or other developers' work.

## How it works

When a developer creates a branch (e.g. `fix/issue-234-calculation-error`), Git creates a pointer to the current code version. From that point, changes made on the branch remain isolated. When work is complete, changes are proposed to the team via Pull Request and, after approval, merged into the main branch.

## What it's for

Branches eliminate the problem of accidental overwrites and unmanaged conflicts. Every developer works in their own isolated area: they don't overwrite others' work and don't break working code. The main branch always stays in a "good" state because it only receives approved code.

## When to use it

A branch is created for every task, bug fix or feature. Naming conventions help identify the purpose: `fix/` for bugs, `feature/` for new features, `hotfix/` for urgent fixes. The branch is deleted after merge to keep the repository clean.
