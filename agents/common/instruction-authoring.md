# Instruction Authoring

This document defines how agent instruction documents must be created, extended, and maintained.

## General Principles

- Treat the instruction set as one coordinated system rather than a collection of independent notes.
- Preserve a clear responsibility for each document.
- Put each rule in the document that owns the decision or behavior it governs.
- Prefer concrete decision criteria and observable behavior over vague aspirations.
- Write rules that remain valid across the intended scope of the document.
- Do not add a rule solely to address a hypothetical problem with no plausible impact.
- Keep the instruction set concise enough that important constraints remain visible.

## Choosing the Instruction Level

- Put a rule under `agents/common/` only when it should apply across different projects, languages, frameworks, and product types.
- Put a rule under `agents/project/` when it depends on the current project's purpose, technology, architecture, commands, directory layout, environment, or conventions.
- Do not place project-specific examples in a common document if they could be mistaken for universal requirements.
- Follow the scope and precedence rules in the root `AGENTS.md`.

## Promoting Project Knowledge into Instructions

Create or update an instruction under `agents/project/` only when the information is:

- confirmed by the user, maintained project documentation, executable configuration, or a stable and unambiguous repository convention;
- specific to the current project rather than broadly reusable;
- expected to affect future agent decisions repeatedly; and
- expressed as an actionable rule, constraint, convention, command, or decision boundary.

Suitable subjects include project commands, supported environments, architectural boundaries, directory ownership, naming conventions, generated or protected areas, recurring terminology, documentation conventions, UI targets, and explicit common-rule exceptions.

Do not promote task-specific requirements, temporary plans, progress or handover notes, individual bug explanations, speculative patterns, incidental implementation details, or facts that future agents can reliably discover from stable code without extra interpretation. Put human-readable specifications, decisions, procedures, and handover material under `docs/` according to the applicable human-facing documentation policy.

When a qualifying durable rule is discovered during authorized work, record it without asking for separate permission if it faithfully documents an already confirmed project fact and does not broaden the task or establish a consequential new convention. Ask before recording a rule that would establish a new consequential project policy rather than document an existing one.

## Evidence and Maintenance of Project Instructions

- Base project instructions on explicit user decisions, maintained specifications, executable configuration, or stable and unambiguous repository conventions.
- Identify the authoritative source path or decision when a rule is consequential, non-obvious, or likely to become stale.
- Reference volatile values and commands at their executable source when practical instead of duplicating details that future changes could desynchronize.
- Record an update trigger or ownership boundary when a rule depends on a toolchain version, generated area, external contract, or operational workflow that may change.
- When project instructions conflict with executable configuration or maintained specifications, investigate which source is stale before updating either one.
- Update or remove a project instruction in the same task when its authoritative source changes and the rule would otherwise become inaccurate.
- Do not add timestamps, source annotations, or maintenance metadata mechanically when the rule is stable and its basis is already obvious.

## Choosing a Document

Before adding a rule:

1. Inspect the README index and existing instruction documents for an established owner.
2. Extend the owning document when the rule fits its existing responsibility.
3. Create a new document only when the subject has a distinct responsibility, enough substance to justify separation, and no suitable existing owner.
4. Add cross-references instead of duplicating detailed rules across documents.

Use `README.md` in each instruction directory as the human-readable catalog of document responsibilities. Use the instruction files themselves as the authoritative source of rules.

When a new document takes ownership of an existing topic, move or replace the old rules rather than leaving competing sources of truth.

Create a nested policy directory only when one policy area has multiple substantial documents with distinct responsibilities and grouping them materially improves discovery or conditional loading. Do not create nested directories merely to shorten a file or mirror a conceptual hierarchy with no maintenance value.

When using a nested policy directory:

- keep each enforceable file directly owned by that directory;
- add a human-readable `README.md` index in that directory;
- list the directory in its parent README and list its instruction files in its own README;
- reference enforceable files directly from the root loading rules rather than loading the directory README as policy; and
- avoid deeper nesting unless another independently justified policy group requires it.

## Document Structure

Use the following information order when applicable:

1. A single H1 title
2. A one-sentence purpose and scope statement
3. General principles
4. Context discovery or prerequisites
5. Decision criteria or operating levels
6. Domain-specific execution rules
7. High-impact actions, exceptions, or failure handling
8. Verification
9. User-facing reporting or project-specific documentation

This is an information order, not a mandatory template. Omit sections that add no value, and use domain-specific headings when they are clearer. Do not create empty or artificial sections merely to match the sequence.

## Instruction File Naming

- Write enforceable instruction files in English so they remain consistent across projects; use Korean only for the human-readable README index unless a higher-priority requirement specifies otherwise.
- Name instruction files in lowercase English kebab-case.
- Name each instruction file after the policy area it owns.
- Use `README.md` only for the human-readable directory index.
- Do not encode precedence or read order with numeric prefixes or alphabetical naming.
- Do not use vague or incremental names such as `rules2.md`, `extra.md`, `new-rules.md`, or `misc.md`.
- Keep the existing file name when it remains accurate; do not rename instruction files solely for cosmetic consistency.
- When renaming an instruction file, update all references and the README index in the same change.

## Rule Style

- Write one primary requirement per bullet.
- Start rules with a direct action or prohibition such as `Inspect`, `Use`, `Prefer`, `Ask`, `Do not`, or `Never`.
- Use `Never` only for unconditional safety, honesty, or authority boundaries.
- Use `Ask before` only when explicit user input is genuinely required.
- Use `Prefer` for defaults that may have justified exceptions.
- State the condition before the required action when a rule applies only in certain circumstances.
- Define ambiguous qualifiers such as significant, broad, expensive, or high risk with criteria or examples when practical.
- Avoid slogans, rhetorical advice, and subjective adjectives that do not change agent behavior.
- Use consistent terminology for the same concept across documents.

## Examples and Lists

- Use examples to clarify a boundary, not to create an accidental exhaustive list.
- Introduce non-exhaustive examples with wording such as `Examples include`.
- Keep examples technology-neutral in common instructions unless a concrete example is necessary to explain a universal risk.
- Use numbered lists for ordered procedures and precedence.
- Use bullets for unordered rules, criteria, and examples.

## References and Duplication

- Reference another instruction document with the shortest unambiguous path in backticks.
- Use the file name alone for a document in the same directory and a repository-relative path when referencing across instruction directories.
- Keep detailed policy in one owning document; references elsewhere should explain when that policy applies, not restate it.
- Do not duplicate a rule for emphasis.
- Remove or update stale references when renaming, moving, or replacing a document or section.
- Do not rely on file name, alphabetical order, or read order to resolve conflicts.

## README Indexes

- Use `README.md` in any instruction directory only as a human-readable index of its direct instruction files and child policy directories.
- Write README indexes in clear, natural Korean unless the intended developer audience requires another language.
- Describe each instruction file's related area, purpose, and important relationship to other instruction files.
- Keep descriptions concise enough that readers can choose the correct source file without mistaking the summary for the full policy.
- Do not place independent agent rules, authority grants, safety exceptions, precedence changes, or detailed operational policy in a README index.
- Do not use a README summary to override, reinterpret, or replace an instruction file.
- When a README conflicts with an instruction file, treat the instruction file as authoritative and update the README.
- When adding, removing, renaming, or changing the responsibility of an instruction file or policy directory, update the README in the same directory and its parent index as applicable in the same change.
- List only files that exist and remove entries for deleted or renamed files.
- In `agents/project/README.md`, describe project purpose and common-rule relationships only as navigation context; put every enforceable project rule and explicit override in a separate instruction file.

## Updating Instructions

When modifying instruction documents:

1. Identify the intended behavioral change.
2. Inspect related documents for overlap, contradiction, and established terminology.
3. Make the smallest coherent change across all affected instruction files.
4. Remove superseded or duplicate rules.
5. Preserve project-specific exceptions and unrelated user changes.
6. Review the resulting instruction flow as a whole, not only the edited paragraph.

Do not change operational policy as incidental wording cleanup. If reorganization reveals a substantive conflict, resolve it according to the root precedence rules or report it to the user.

## Verification

For instruction changes:

- Run the repository's instruction validator when it is available.
- Review the final diff for changed meaning, duplication, contradictions, and misplaced responsibility.
- Verify headings, lists, references, and terminology are consistent.
- Confirm new common rules are not project-specific.
- Confirm project rules override only the intended common defaults and do not weaken common safety, authority, or honesty boundaries.
- Use `verification.md` to avoid unrelated executable checks for documentation-only changes.

## Maintaining This Standard

- Apply this document whenever adding, removing, splitting, merging, or substantially editing instruction content under `agents/common/` or `agents/project/`.
- Update this document when the instruction system gains a new document responsibility or a recurring authoring pattern changes.
- Do not exempt this document from its own clarity, structure, duplication, and verification requirements.
