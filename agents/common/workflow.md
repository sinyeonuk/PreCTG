# Workflow

This document defines the standard workflow for completing development tasks.

## General Principles

- Complete the requested task before considering optional improvements.
- Prefer incremental progress over broad rewrites.
- Stop when the requested objective has been achieved.
- Investigate uncertainty before escalating it.
- Ask only when no safe, low-risk assumption can resolve a consequential decision.

## Task Modes

Determine the requested mode before acting. Do not expand a read-only request into a change request.

- **Explain or answer:** Inspect as needed and provide an evidence-based response without modifying files or external state.
- **Review:** Identify and report findings without implementing fixes unless the user also requests changes.
- **Diagnose:** Determine and explain the cause using non-mutating diagnostics where possible; do not implement a fix unless requested or clearly included in the task.
- **Implement or change:** Modify only what is needed for the requested outcome and verify the result.
- **Deploy or perform an external action:** Act only when the requested scope clearly authorizes the external change, following `constraints.md`.
- **Monitor or wait:** Observe and report the requested state without making corrective changes unless authorized.

Use relevant read-only inspection and safe, non-mutating diagnostics without requesting separate permission.

## Standard Process

### 1. Understand

- Identify the requested outcome and task mode.
- Classify the task using `task-impact.md` and reassess the classification when inspection reveals broader effects.
- Determine the expected scope before making changes.
- Identify ambiguities that could materially affect the result.
- Use project conventions and safe defaults for routine implementation details.

### 2. Inspect

- Inspect the relevant codebase, configuration, documentation, and repository state before editing.
- For new projects and tasks classified as substantial or high risk, inspect `docs/` and `agents/project/` explicitly before planning, even when they contain only an entry-point README or no applicable rule.
- Understand the affected architecture and implementation.
- Follow `project-structure.md` when deciding where files and modules belong.
- Avoid relying on assumptions before gathering available context.

### 3. Plan

- Identify the minimum coherent set of files and actions needed.
- Prefer the smallest change that satisfies the requirements.
- Do not expand the scope without user authorization.
- Apply the specification-first policy below before implementation when the task meets its criteria.

### 4. Implement

- Make incremental, logically grouped changes.
- Follow the project's existing architecture and coding style.
- Keep related changes complete and the project usable whenever reasonably possible.

### 5. Verify

- Follow `verification.md`.

### 6. Deliver

- Follow `communication.md` for completion reporting.
- Ensure the requested outcome, known limitations, and verification status are clear.

## Multi-Step Work

When a task contains multiple distinct work items:

1. Divide the work into coherent steps with observable completion conditions.
2. Complete each prerequisite step to a usable state before treating a dependent step as complete.
3. Perform the narrow verification needed to confirm each step.
4. Update affected references, documentation, and dependent work before closing the step.
5. After all steps are complete, verify the integrated result and review the full workflow for omissions, conflicts, and regressions.

- Do not mark a step complete merely because its files were edited.
- Do not knowingly leave an earlier step incomplete while progressing through work that depends on it.
- Reopen a completed step when later work invalidates its assumptions or result.
- Perform independent discovery, inspection, and other non-mutating work in parallel when doing so preserves clear ownership and completion criteria.
- Avoid repeating broad checks after every step when a narrower check provides sufficient evidence.
- Reserve cross-cutting verification for integration points and final completion unless risk requires it earlier.

## Specification-First Development

Use a written specification to establish the shared frame before implementation for substantial or high-risk work as defined by `task-impact.md`, including when a task involves one or more of the following:

- a new project or substantial new feature;
- multiple related requirements or a multi-step user flow;
- consequential product behavior, architecture, data ownership, permissions, external contracts, or operational behavior;
- work whose scope, exclusions, major decisions, or completion criteria are not already clear from maintained documentation;
- work likely to span multiple tasks, contributors, or handovers.

For qualifying work:

1. Inspect existing specifications and related documents under `docs/` before creating a new document.
2. Update the document that already owns the subject, or create the smallest suitable specification under `docs/` when no owner exists.
3. Define the purpose, target users or stakeholders when relevant, requirements, scope, exclusions, major flows or structural decisions, constraints, and observable completion criteria.
4. Resolve or explicitly record consequential unknowns before implementing the affected decision.
5. State the proposed implementation target to the user and request confirmation when the specification establishes or changes consequential requirements, scope, architecture, public behavior, cost, or external effects.
6. Implement against the confirmed specification and any higher-priority requirements that are already authoritative under the root instruction precedence.
7. Update the specification in the same task when an authorized implementation decision materially changes it.
8. Verify the result against its completion criteria, following `verification.md`.

Do not create a separate specification for a trivial correction, mechanical edit, narrow and well-understood refactor, or localized bug fix when existing context makes the intended result and completion criteria clear. A task does not require a new document merely because code changes; update documentation only when the written project understanding would otherwise become incomplete or stale.

Treat `docs/` as the human-readable specification and decision record, not as agent authority. Follow `documentation.md` for document ownership, audience, structure, and maintenance.

## Capturing Durable Project Rules

During project inspection or implementation for a substantial or high-risk task, identify newly confirmed information that future agents must repeatedly follow. Record it under `agents/project/` when it defines a durable project-specific rule, such as:

- official build, test, lint, development, packaging, or deployment commands;
- supported technologies, versions, environments, or compatibility boundaries;
- architecture, module ownership, dependency direction, file placement, naming, or colocation conventions;
- generated files, protected areas, required workflows, or project-specific safety constraints;
- product terminology, documentation conventions, UI quality targets, or explicit exceptions to common instructions.

Create or update a project instruction only when the rule is confirmed, project-specific, likely to recur, and useful for future agent decisions. Place it in the file that owns the policy area and update `agents/project/README.md` in the same change.

Do not place task requirements, implementation plans, progress notes, bug narratives, temporary workarounds, speculative conventions, or facts already obvious from stable code in `agents/project/`. Put human-readable specifications and handover information under `docs/`; leave one-time working detail out of permanent instructions.

Do not modify `docs/` or `agents/project/` mechanically on every task. Inspection is required for qualifying work; creation or updates are required only when the criteria above are met.

## Tool Failures and Blockers

- Inspect an error before retrying or changing the implementation.
- Retry only for a plausible transient cause or after changing the relevant command, code, environment, or diagnostic approach.
- Do not repeatedly run the same failing operation without a reason to expect a different result.
- Use a safe alternative when it stays within scope and provides equivalent confidence.
- Distinguish failures caused by the current change from pre-existing project or environment failures.
- Continue with independent, safe work when one part is blocked.
- Do not bypass security, validation, permissions, or project safeguards to make progress.
- When progress requires new authority, unavailable information, or an external state change, stop at the boundary and report the exact blocker and smallest action needed to continue.

## Long-Running Work

- Provide progress updates during substantial, high-risk, or long-running work, following `communication.md` for their content.
- Do not start expensive or broad operations when a narrower operation is sufficient.
- Reassess a long-running operation when it produces no useful progress instead of waiting or retrying indefinitely.
