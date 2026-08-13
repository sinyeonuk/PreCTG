# Documentation

This document defines how agents should create and maintain human-facing project documentation under `docs/`.

## General Principles

- Treat instruction files under `agents/` as rules for agent behavior and `docs/` as information for people who use, develop, operate, review, or inherit the project.
- Treat `README.md` files under instruction directories as the limited human-readable index exception defined by the root `AGENTS.md` and `instruction-authoring.md`.
- Keep behavioral commands directed at agents, agent authority rules, and system-prompt content out of `docs/`; user-facing development and operation commands remain appropriate when they serve the document's audience.
- Write documentation to help a defined audience understand a decision, complete a task, operate the project, or assess its current state.
- Prefer useful, maintainable documents over comprehensive-looking documentation with no clear reader or purpose.

## Audience and Purpose

Before creating or substantially rewriting a document:

1. Identify the primary reader.
2. Identify the question, task, or decision the document must support.
3. Determine whether an existing document already owns that purpose.
4. Choose the smallest document type and scope that serves the reader.

- Separate documents when they serve materially different audiences or lifecycles.
- Do not combine onboarding, operational procedures, product requirements, and historical notes into one catch-all document without a clear navigation structure.
- State prerequisites and expected outcomes for procedural documents.

## Documentation Entry Point

- Use `docs/README.md` as the entry point for human-facing project documentation.
- Give `docs/README.md` a useful purpose even when it is the only document: identify the intended audience, describe the available documentation, and explain where to find essential project information.
- Link each maintained document from the entry point and briefly state when a reader should use it.
- Do not create empty documents, speculative sections, or placeholder document trees merely to make the project appear documented.
- Add new documents when a real workflow, decision, operational responsibility, or handover need justifies them.

## Specifications

- Use `docs/` for human-readable project, product, feature, architecture, and operational specifications.
- Follow the specification-first criteria in the standard task workflow before implementing qualifying work.
- Update an existing specification when it already owns the subject; do not create a competing plan or feature document for the same decision.
- Keep a specification focused on durable shared understanding rather than a chronological transcript of agent activity.
- Include purpose, scope, exclusions, requirements, constraints, major decisions or flows, and observable completion criteria when they are relevant.
- Distinguish confirmed decisions from open questions, assumptions, and deferred work.
- Record the reason and impact of a consequential decision when future readers could not safely infer them from the implementation.
- Keep implementation-level detail only when it constrains behavior, compatibility, ownership, operation, or future changes.
- Do not treat an unconfirmed draft as authorization for consequential implementation decisions.
- Keep specifications synchronized when implementation changes their documented behavior or completion criteria.

## Language and Tone

- Write internal human-facing documentation in clear, natural Korean unless the user, project instructions, existing documentation, or external audience requires another language.
- Follow `terminology.md` and applicable project terminology when writing Korean documentation.
- Preserve an established project language when changing only part of an existing document set.
- Prefer concrete actions and outcomes over internal implementation jargon.
- Use one term consistently for the same concept throughout a document set.
- Avoid language that judges the reader, such as describing a step as obvious, trivial, or easy.

## Structure and Readability

- Start with a clear Korean title and a brief statement of purpose when the purpose is not obvious.
- Organize content in the order a reader needs it rather than the order in which the system was implemented.
- Use descriptive headings that allow readers to locate information quickly.
- Keep paragraphs focused on one idea and procedures focused on one task.
- Use numbered lists for ordered procedures and bullets for unordered information or checks.
- Put warnings before the action that creates the risk and explain both the impact and prevention.
- Use examples only when they clarify a decision, format, or non-obvious boundary.
- Use concise English ASCII file names for new documentation by default, while keeping titles and body text in the language appropriate to the intended reader.
- Prefer lowercase kebab-case for human-readable documentation files when repository conventions and tooling do not require another form.
- Preserve conventional entry names such as `README.md` and established public or ecosystem naming conventions.
- Keep a document's file name and title conceptually aligned.
- Use one separator convention among peer documents; do not mix hyphens and underscores without a project-specific reason.
- Avoid vague or temporary document names such as `문서.md`, `기타.md`, `새-문서.md`, `최종.md`, `진짜-최종.md`, or unexplained version suffixes.
- Use dates in file names only when chronology is part of the document type, such as meeting notes, reports, or dated decision records.
- Do not rename unrelated documents merely to normalize style during a scoped task.

## Procedures

- Write procedures as observable actions in execution order.
- Include prerequisites, required access, expected results, and recovery steps when relevant.
- Keep commands and file paths exact and visually distinct from explanatory prose.
- Explain what a consequential command changes before asking the reader to run it.
- Do not include commands that are known to be unsafe, obsolete, incomplete, or dependent on undocumented local state.
- Link to the source configuration instead of duplicating volatile values when practical.

## Checklists

- Write each checklist item as a verifiable condition or action.
- Keep checklist items specific enough that different readers can determine whether each item is complete.
- Order items according to the real workflow and place irreversible checks before the corresponding action.
- Do not mix background explanation into checklist items; link to supporting detail when needed.
- Separate required checks from optional recommendations.
- Avoid checklist items such as `Review everything` or `Confirm it works` that have no observable completion criterion.

## Handover Documents

- Describe the current project state rather than retelling the entire development history.
- Identify completed work, work in progress, remaining work, known problems, risks, external dependencies, and the next useful actions.
- Distinguish confirmed facts from assumptions and recommendations.
- Include relevant locations, owners, dates, or environment details when they affect continuation of the work.
- Do not include secrets, personal credentials, or sensitive operational data.
- Remove stale handover claims when later work changes the documented state.

## Source of Truth

- Treat project instructions under `agents/project/` as authoritative for project-specific agent behavior within the scope and precedence defined by the root `AGENTS.md`.
- Treat executable code, configuration, schemas, migrations, and automation as authoritative for implemented behavior unless the project explicitly defines another source of truth.
- Treat `docs/` as the human-readable explanation of the project, not as an automatic override of implementation or agent instructions.
- When documentation conflicts with implementation, investigate which is stale before changing either one.
- When the current task changes documented behavior, update the affected documentation as part of the same task.
- Do not copy large amounts of code, configuration, or generated output into documentation when a stable reference is more maintainable.

## Maintenance

- Update an existing document instead of creating a competing document with the same purpose.
- Remove or revise stale instructions, links, screenshots, examples, and status claims affected by the current task.
- Preserve historical decisions in an appropriate decision record rather than leaving outdated guidance in active procedures.
- Keep document ownership and update triggers explicit when staleness would create operational risk.
- Do not rewrite unrelated documentation for style consistency during a scoped implementation task.

## Verification

- Review changed documentation from the intended reader's perspective.
- Verify headings, links, references, terminology, commands, and file paths relevant to the change.
- Confirm ordered procedures are complete enough to follow and checklists have observable completion criteria.
- Confirm Korean prose is natural, consistent, and free of unnecessary language mixing when Korean is the selected language.
- Follow `verification.md` and do not run unrelated builds or test suites for documentation-only changes.

## Reporting

- Follow `communication.md` when reporting documentation changes.
- Describe which reader need or workflow the document now supports.
- Mention unresolved factual gaps, stale external references, or unverified procedures only when they materially limit the document's reliability.
