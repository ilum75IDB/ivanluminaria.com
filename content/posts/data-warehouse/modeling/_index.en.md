---
title: "Dimensional Modeling"
date: "2026-03-10T10:00:00+01:00"
description: "Dimensional modeling in practice: hierarchies, dimensions, fact tables and the design decisions that make the difference between a DWH that delivers and one that struggles."
layout: "list"
---
Dimensional modeling looks simple.<br>
Facts and dimensions. Star schema. Snowflake. Concepts you learn in an afternoon.<br>

Then you hit production and discover the devil is in the details. A ragged hierarchy that breaks every aggregation. A poorly managed slowly changing dimension that rewrites history. The wrong granularity in the fact table that makes a report the business considers trivial impossible to build.<br>

In this section I share the real problems of dimensional modeling — the ones textbooks cover in half a page and that cost you weeks in production.
