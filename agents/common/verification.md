# Verification

This document defines how agents must verify changes before declaring a task complete.

## General Principles

- Match verification effort to the behavioral impact, risk, and scope of the change.
- Use the least expensive check that provides meaningful confidence.
- Start with the narrowest relevant check and expand only when the change or results justify it.
- Do not run checks mechanically merely because they are available.
- Do not claim that a change works based only on inspection when executable verification is warranted and available.
- Do not weaken, disable, or bypass existing checks merely to make verification pass.

## Proportional Verification

Use the shared classification in `task-impact.md`. Verification is based on behavioral impact, risk, and scope rather than line count.

### Trivial Changes

Examples include correcting prose, comments, labels, or formatting that cannot affect execution, layout, generated output, or structured behavior.

- Review the changed content and final diff.
- Perform artifact-specific inspection when another applicable domain policy requires it.
- Do not run builds, linters, test suites, or smoke tests unless the project has a specific inexpensive check for that artifact or the change could affect layout or generated output.
- Treat inspection as sufficient and report the change as reviewed rather than tested.

A text-only edit is not necessarily non-behavioral. Changes to identifiers, configuration keys, commands, paths, templates, snapshots, localization placeholders, layout-sensitive interface copy, structured documentation, or generated inputs may require targeted verification.

### Localized Changes

- Review the final diff.
- Run the narrowest test or check that exercises the affected behavior.
- Run a formatter, linter, type checker, or compiler only when it is relevant to the changed files or likely to catch a plausible error.
- Avoid project-wide checks when a focused check provides sufficient confidence.

### Substantial or High-Risk Changes

Examples include changes to public APIs, shared infrastructure, authentication, authorization, persistence, migrations, concurrency, build configuration, foundational dependencies, or dependency and toolchain changes with broad effects.

- Run focused checks for the changed behavior first.
- Run broader regression tests, static checks, and builds when practical and relevant.
- Check important error paths, compatibility concerns, and recovery or rollback behavior when applicable.

## Discovering Verification Commands

Before choosing commands:

1. Read the applicable project instructions.
2. Inspect existing scripts, build files, task runners, CI configuration, test configuration, and project documentation.
3. Reuse the project's documented commands and workflows.
4. Prefer commands scoped to the affected files, module, or behavior.
5. Do not invent a new verification workflow when the project already defines one.

## Execution Order

Unless the project defines another order:

1. Review the changed files and final diff.
2. Classify the behavioral impact and choose the minimum sufficient verification.
3. Run focused tests or checks when warranted.
4. Expand to static checks, builds, smoke tests, or broader regression tests only when they add meaningful confidence.
5. Perform a final diff and working-tree review.

Consider the expected runtime and resource cost of a check. Do not run expensive checks when their likely value is negligible for the change.

## Specification Conformance

When the task is governed by a maintained specification:

- Verify the implemented result against the specification's observable completion criteria.
- Check the documented scope and exclusions so verification does not silently omit required behavior or expand into deferred work.
- Treat a mismatch between implementation and specification as unresolved until the implementation is corrected or the specification change is authorized and documented.
- Confirm affected specifications remain synchronized with material implementation decisions.
- Do not claim the feature is complete merely because tests pass when documented completion criteria remain unmet.

## Handling Failures

When a verification command fails:

1. Determine whether the failure was introduced by the current change.
2. Fix failures caused by the current change and rerun the relevant check.
3. Do not hide, suppress, or ignore failures.
4. Do not fix unrelated pre-existing failures unless the user requests it or the fix is necessary to verify the task.
5. Clearly report pre-existing failures and explain why they appear unrelated.
6. Report verification blocked by missing tools, dependencies, permissions, services, or environment limitations.

## Reporting

- Preserve accurate evidence of the checks performed and their outcomes.
- Distinguish automated verification from inspection or manual review when that distinction matters to confidence.
- Report remaining failures, environment limitations, and meaningful unverified risks.
- Follow the verification-integrity constraints in `constraints.md`.

Use precise language:

- "Tests passed" means the relevant test command completed successfully.
- "Reviewed only" means the change was inspected but not executed.
- "Not tested" means no executable verification was performed where testing may have been relevant.
- "Could not verify" means verification was attempted but blocked, with the reason stated.
