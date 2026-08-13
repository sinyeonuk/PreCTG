# Agent Instructions

This file is the entry point for all agent instructions.

Before starting any task, read the core instructions and then load only the instruction files applicable to the task, as defined below. If task scope changes, load the newly applicable files before continuing.

When creating or modifying instruction documents under `agents/common/` or `agents/project/`, follow `agents/common/instruction-authoring.md`.

`README.md` files under instruction directories are human-readable indexes. They help developers discover and understand instruction files, but they do not independently define, override, or grant exceptions to agent behavior. When a README summary differs from an instruction file, follow the instruction file and update the stale README.

## Instruction Sources

### Common Instructions

Always read these core instructions:

- `agents/common/constraints.md`
- `agents/common/workflow.md`
- `agents/common/communication.md`
- `agents/common/task-impact.md`

Then read the files for every applicable task area:

| Task area | Additional instructions |
|---|---|
| Source code or executable configuration | `agents/common/coding.md`, `agents/common/quality.md`, `agents/common/verification.md` |
| Refactoring or internal structural improvement | `agents/common/refactoring.md`, `agents/common/coding.md`, `agents/common/testing.md`, `agents/common/verification.md` |
| Test design, creation, or modification | `agents/common/testing.md`, `agents/common/verification.md`, `agents/common/quality.md` |
| Quality assurance, acceptance review, or exploratory testing | `agents/common/quality-assurance.md`, `agents/common/testing.md`, `agents/common/verification.md`, `agents/common/quality.md` |
| Checks, builds, or validation without test changes | `agents/common/verification.md`, `agents/common/quality.md` |
| User data, persistence, logs, telemetry, or network communication | `agents/common/data-and-privacy.md`, `agents/common/verification.md` |
| Files, modules, architecture, or directory structure | `agents/common/project-structure.md` |
| Git, repository state, generated files, or ignore rules | `agents/common/git.md` |
| User-interface design or implementation | `agents/common/ui/foundations.md`, `agents/common/ui/interaction.md`, `agents/common/ui/accessibility.md`, `agents/common/ui/verification.md`, `agents/common/verification.md` |
| UI copy, information, terminology, or localization | `agents/common/ui/content.md`, `agents/common/terminology.md`, `agents/common/ui/verification.md` |
| UI accessibility or responsive behavior | `agents/common/ui/accessibility.md`, `agents/common/ui/verification.md`, `agents/common/verification.md` |
| Human-facing project documentation | `agents/common/documentation.md`, `agents/common/terminology.md`, `agents/common/verification.md` |
| New or uninitialized projects | `agents/common/project-bootstrap.md`, `agents/common/documentation.md`, `agents/common/project-structure.md`, `agents/common/verification.md` |
| Substantial features or specification work | `agents/common/documentation.md`, `agents/common/project-structure.md`, `agents/common/verification.md` |
| Agent instruction documents | `agents/common/instruction-authoring.md`, `agents/common/verification.md` |

Read all files for overlapping task areas. When applicability is uncertain, read the potentially relevant file. Do not read unrelated optional files merely because they exist. Use `agents/common/README.md` only as a navigation index, not as an instruction source.

These instructions define the default behavior shared by every project.

Common instructions contain reusable rules that should remain valid across different languages, frameworks, repositories, and product types. They may define:

- agent workflow and communication;
- safety and authority boundaries;
- general coding, structure, UI, documentation, and verification principles;
- Git behavior and repository hygiene.

Common instructions must not prescribe a project-specific technology, command, directory layout, architecture, product requirement, or deployment environment.

#### Common Instruction Protection

Treat `agents/common/` as a protected shared baseline.

- Do not modify files under `agents/common/` during ordinary project work.
- Put project-specific rules, clarifications, and exceptions under `agents/project/` instead of editing the common baseline.
- Modify `agents/common/` only when the user's current request explicitly targets the shared instruction system itself.
- Do not treat a request to change the current project, record a project convention, or resolve a project-specific conflict as authorization to modify common instructions.
- When an authorized common-instruction change is made, keep it reusable across projects and follow `agents/common/instruction-authoring.md`.

### Project Instructions

Read all instruction Markdown files recursively under `agents/project/` when the directory exists. Use README files only as navigation indexes, not as instruction sources.

These instructions define behavior and conventions specific to the current project. They supplement common instructions and may override common defaults within the current project.

Use project instructions as the normal customization layer. Do not edit the common baseline merely because the current project needs a different default.

Project instructions may define:

- project purpose and expected quality targets;
- technology choices and supported versions;
- architecture, module boundaries, and concrete directory responsibilities;
- naming, coding, packaging, and colocation conventions;
- documentation audience, language, and maintenance conventions;
- build, test, lint, development, and deployment commands;
- environment constraints, generated files, and prohibited edit areas;
- explicit project-specific exceptions to common rules.

Project instructions should not repeat common rules unless repetition is necessary to document a project-specific clarification or exception.

If `agents/project/` does not exist or does not address a topic, inherit the applicable common instructions and follow established repository conventions. Do not invent project-specific rules merely because project instructions are absent.

## Precedence

When instructions conflict, follow this order of precedence:

1. System, platform, and safety requirements
2. The user's explicit instructions for the current task
3. Non-negotiable scope, authority, safety, and honesty boundaries in `agents/common/constraints.md`
4. Instructions under `agents/project/`
5. Other instructions under `agents/common/`
6. Existing project conventions and patterns

More specific instructions take precedence over general instructions at the same level.

Project instructions override common defaults only for the current project and only within the scope of the conflicting or more specific rule. They do not disable an entire common file. Common rules not addressed by a project instruction remain in effect.

Project instructions may make common constraints more restrictive, but they cannot grant authority reserved for the user or weaken common safety and honesty boundaries.

When a project instruction intentionally overrides a common rule, it must identify the affected default and the scope of the exception. Include the project-specific reason when that reason is not obvious.

When files at the same instruction level conflict:

1. Prefer a rule explicitly scoped to the affected language, module, directory, platform, or task type.
2. Prefer an explicit exception over a general default.
3. Do not treat file name, alphabetical order, or read order as precedence.

If a conflict remains unclear and the choice could materially affect the result, ask the user before proceeding. Do not silently ignore conflicting instructions.

## Scope

Apply the common instructions to every project.

Apply project instructions only to the project they describe. Do not treat project-specific decisions as universal rules or carry them into unrelated projects.

Keep examples, drafts, and unrelated project documentation outside `agents/common/` and `agents/project/`. Treat README indexes and content outside these instruction directories as contextual rather than authoritative unless an applicable instruction explicitly references it.
