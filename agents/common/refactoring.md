# Refactoring

This document defines how agents should improve internal code structure while preserving supported behavior.

## General Principles

- Refactor to address a concrete maintenance problem, risk, or requested objective.
- Preserve externally observable behavior and public contracts unless a behavior change is explicitly authorized.
- Prefer small, reviewable transformations over a broad rewrite.
- Keep refactoring proportional to the task and avoid unrelated cleanup.
- Apply the established implementation principles and follow `testing.md` for test design.

## Establishing a Baseline

- Identify the behavior, contracts, invariants, and compatibility requirements that must remain unchanged.
- Inspect existing tests and verification commands before restructuring the implementation.
- Add a focused characterization or regression test when important current behavior lacks practical protection.
- Record uncertain or apparently accidental behavior instead of silently treating it as either required or disposable.
- Ask before preserving or removing ambiguous behavior when the choice could materially affect users or integrations.

## Planning the Change

- State the concrete problem being reduced, such as duplicated policy, mixed ownership, cyclic dependencies, hidden state, excessive coupling, or an unstable boundary.
- Choose the smallest structural change that meaningfully reduces that problem.
- Separate behavior changes from structural changes when practical so each can be reviewed and verified independently.
- Avoid replacing a working implementation solely to impose a preferred pattern, architecture, or naming style.
- Require explicit authorization for architectural changes covered by `constraints.md`.

## Performing the Refactor

- Work in coherent increments that keep the affected area understandable and recoverable.
- Preserve stable entry points while moving responsibilities behind them when compatibility is required.
- Update callers, tests, documentation, configuration, and generated references affected by a move or rename.
- Remove superseded code after its consumers have moved and its behavior is covered.
- Remove an abstraction when it adds indirection without a clear responsibility, boundary, or consumer benefit.
- Do not mix mass formatting, dependency upgrades, or unrelated renaming into the same refactor.

## Verification

- Run the narrowest relevant checks after an intermediate step when early feedback materially reduces risk.
- Run the proportional final verification required by `verification.md`.
- Compare observable behavior before and after the change when preservation cannot be established by automated tests alone.
- Verify dependency direction and absence of unintended cycles when module boundaries change.
- Do not declare a refactor complete while temporary compatibility paths, duplicate implementations, or migration scaffolding remain without an explicit reason.

## Reporting

- Explain the maintenance problem resolved and the behavior intentionally preserved.
- Report any compatibility layer, known debt, or follow-up work that remains.
