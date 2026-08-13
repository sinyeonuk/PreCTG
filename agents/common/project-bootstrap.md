# Project Bootstrap

This document defines the one-time initialization of copied baseline instructions for a new or previously undocumented project.

## When Bootstrap Applies

Apply bootstrap when the user explicitly requests project initialization, or during the first localized, substantial, or high-risk implementation or specification task as classified by `task-impact.md`, when the repository contains the baseline instruction structure but its `docs/README.md` or `agents/project/README.md` still describes the reusable baseline, contains only generic placeholders, or does not describe the current project.

- Do not bootstrap during a read-only, review, diagnostic, trivial, or unrelated task.
- Do not repeat bootstrap after the current project's purpose and applicable durable rules have been established.
- Do not rewrite accurate documentation in the baseline instruction repository itself merely because it describes the baseline.

## Bootstrap Process

1. Inspect the repository README, manifests, executable configuration, source entry points, existing documentation, and established commands.
2. Identify the project purpose, primary users, current maturity, supported environment, confirmed technology choices, and important workflows that can be established from evidence.
3. Ask only for consequential missing information that cannot be inferred safely and materially affects the requested work.
4. Replace stale baseline-specific content in `docs/README.md` with a concise entry point for the current project's human-readable documentation.
5. Record confirmed, recurring project-specific rules in appropriately owned English files under `agents/project/`.
6. Update `agents/project/README.md` as the human-readable project-purpose and instruction index.
7. Record the imported baseline version from `VERSION` and its source repository, release, or commit in `agents/project/README.md`.
8. Review existing agent instructions, Git settings, documentation, and CI configuration for conflicts with imported template assets.
9. Keep common defaults inherited rather than copying them into project instructions.
10. Run the repository instruction validator and its regression tests when available.

## Bootstrap Content

Document only information that is confirmed and useful for future work, such as:

- project purpose, primary users, and current development intent;
- supported runtimes, platforms, and package or build tools;
- authoritative build, test, lint, run, and generation commands;
- major directory and module ownership;
- generated, protected, or externally managed areas;
- UI implementation target, terminology, or documentation language when applicable; and
- explicit project-specific exceptions to common defaults.

Do not create empty policy files, speculative architecture, deployment plans, paid-service assumptions, or rules copied from `agents/common/`. Preserve the common zero-additional-cost and no-deployment defaults unless the user has explicitly established project-specific alternatives.

## Completion Criteria

Treat bootstrap as complete only when all applicable conditions are satisfied:

- `docs/README.md` describes the actual project and its maintained documentation rather than the reusable baseline.
- `agents/project/README.md` describes the project purpose, primary users, imported baseline version and source, and every project instruction file.
- Confirmed recurring commands, environment constraints, generated areas, and other durable project rules are recorded in the instruction file that owns them.
- When inspection finds no project-specific rule to add, the project index states that conclusion instead of retaining a generic placeholder.
- Existing agent instructions, Git settings, documentation, and CI configuration have been reviewed for conflicts.
- The instruction validator and its regression tests pass when they are available.

## Maintenance Boundary

- Treat bootstrap as initialization, not a requirement to rewrite project instructions on every task.
- Update project documents later only when the current task confirms a durable change or would otherwise leave maintained information stale.
- Preserve evidence sources and update triggers according to `instruction-authoring.md`.
