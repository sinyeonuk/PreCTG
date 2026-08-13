# Task Impact

This document defines a shared impact classification for planning, clarification, documentation, implementation, communication, and verification decisions.

## General Principles

- Classify the task by its highest applicable impact before choosing process depth.
- Base impact on affected behavior, users, contracts, data, systems, reversibility, and failure cost rather than line count or file count.
- Reassess the classification when inspection reveals broader effects than the request initially suggested.
- Use the classification to scale process and verification; do not treat it as authority for an otherwise unauthorized action.

## Trivial

A task is trivial when it cannot affect runtime behavior, layout, generated output, structured meaning, public contracts, user data, security, or external systems.

Examples include:

- correcting ordinary prose, comments, or punctuation;
- formatting a non-executable document without changing its structure or meaning; and
- applying an already established, behavior-preserving local style correction.

For trivial tasks:

- proceed without a separate specification or routine clarification;
- inspect the changed content and immediate context; and
- do not run unrelated builds, linters, test suites, smoke tests, or broad visual checks.

## Localized

A task is localized when it changes observable behavior or maintained structure within one well-understood feature, component, module, document, or workflow without changing major boundaries or high-impact contracts.

Examples include:

- fixing a contained defect;
- adding or changing one established interaction or validation rule;
- extending a module without changing its public contract or dependency direction; and
- updating structured documentation, configuration, or UI copy whose effects remain narrowly scoped.

For localized tasks:

- inspect the affected flow and direct dependencies;
- use a short plan when multiple coordinated edits are required;
- document the change only when maintained project understanding would otherwise become stale; and
- run the narrowest checks that exercise the changed behavior and plausible failure paths.

## Substantial or High Risk

A task is substantial or high risk when it introduces a new project or major feature, spans multiple owned areas, changes consequential user flows, or affects architecture, public contracts, permissions, security, user data, persistence, migrations, concurrency, foundational dependencies, build systems, paid resources, deployment targets, or external state.

Treat a task as high risk even when the code change is small if failure could expose data, lose work, break compatibility, create charges, publish externally, or be difficult to reverse.

For substantial or high-risk tasks:

- apply the specification-first workflow;
- inspect `docs/` and `agents/project/` before deciding the implementation;
- obtain user authorization for consequential decisions and actions reserved by `constraints.md`;
- define observable completion criteria, important failure paths, compatibility needs, and recovery expectations; and
- run focused checks first, then relevant broader regression, static, build, security, migration, or visual checks when they add meaningful confidence.

## Resolving Borderline Cases

- Choose the higher classification when uncertainty concerns security, privacy, data loss, cost, external effects, or difficult reversibility.
- Choose the lower classification when the only difference is implementation size and the behavioral impact remains clearly contained.
- Do not ask the user to classify the task when repository evidence and these criteria provide a safe answer.
- State the classification only when it materially changes the process, requires confirmation, or helps explain a limitation.
