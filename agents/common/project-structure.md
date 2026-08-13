# Project Structure

This document defines how agents should understand, preserve, and extend project structure without imposing a universal directory layout.

## General Principles

- Treat directory structure as a representation of ownership, responsibility, dependency boundaries, and project conventions.
- Inspect and understand the existing structure before creating, moving, renaming, or grouping files.
- Preserve the project's established feature-oriented, layer-oriented, package-oriented, workspace-oriented, or hybrid organization unless the requested change requires otherwise.
- Do not force a preferred template, architecture, or directory tree onto a project.
- Match structural complexity to the project's language, framework, size, maturity, and actual requirements.
- Prefer the simplest structure that makes ownership and navigation clear.
- Standardize repeated decisions where consistency provides real value, but do not standardize unrelated concepts merely for visual symmetry.

## Discovering the Existing Structure

Before deciding where a file belongs:

1. Read applicable instructions under `agents/project/`.
2. Inspect relevant project documentation, manifests, build configuration, and framework conventions.
3. Examine the locations of comparable existing files.
4. Identify module boundaries, dependency directions, entry points, generated areas, and public interfaces relevant to the task.
5. Prefer the established pattern when it remains suitable.

Do not ask the user to choose a routine file location when the project provides a clear precedent.

## Choosing a File Location

Use this order of precedence when placing a new file:

1. Explicit project-specific structure instructions
2. The location of comparable existing files
3. Existing feature, domain, package, or module ownership
4. Language and framework conventions already adopted by the project
5. The simplest location that preserves clear ownership and dependency direction

- Place files near the code, feature, or module that owns them.
- Keep files that change for the same reason close together when project conventions allow it.
- Keep public entry points distinct from internal implementation details when the project already makes that distinction.
- Do not place a file in a shared location merely because its ownership has not been investigated.
- Do not add temporary scripts, debug output, generated artifacts, or task notes to the repository root without an established project convention.

## File and Directory Naming

Choose names in this order:

1. Explicit project-specific naming instructions
2. Comparable existing files and directories
3. Language, framework, build-tool, and package-manager conventions already used by the project
4. The stable responsibility, feature, domain concept, or primary export represented by the path
5. The simplest predictable name that remains accurate

- Use portable ASCII names for new files and directories by default.
- Limit ordinary path names to English letters, digits, hyphens, underscores, and periods used for extensions or established special-file names.
- Avoid spaces, non-ASCII characters, emoji, quotation marks, brackets, and shell-significant punctuation in new path names unless an external contract or tool requires them.
- Treat casing and separator style as ecosystem decisions: follow the project's language, framework, build-tool, and peer-file conventions rather than forcing one global form.
- Preserve conventional and reserved names such as `README.md`, `Dockerfile`, `.gitignore`, framework entry points, package scopes, and tool-required paths.
- Allow a non-ASCII or otherwise exceptional name when required by an existing public path, external format, localization artifact, generated output, or authoritative project convention.
- Do not rename existing files or directories solely to normalize them to the ASCII default during an unrelated task.
- Follow the project's established casing, separators, suffixes, extensions, and singular or plural conventions.
- Do not impose hyphens, underscores, camelCase, PascalCase, snake_case, or another convention universally.
- Use hyphens where human-readable documents, URLs, package names, or web assets conventionally use them.
- Use underscores where importable modules, language ecosystems, datasets, generated files, or tools require or conventionally use them.
- Do not mix hyphens and underscores among peer files without a project-specific reason.
- Name a file or directory after its stable responsibility rather than a temporary implementation detail.
- Prefer names that allow a developer to predict the contents or ownership without opening the file.
- Match a file name to its primary exported symbol when the project uses one primary export per file.
- Keep source, test, fixture, mock, story, style, and related asset names recognizably associated according to project convention.
- Use framework-reserved names only for their intended framework role.
- Avoid vague permanent names such as `misc`, `stuff`, `temp`, `new`, `final`, or `other`.
- Avoid names such as `rules2`, `service-v2`, or `final-final` when version control or a stable domain distinction should represent the change.
- Avoid `utils`, `helpers`, or `common` as default catch-all names; use them only when the project has a clear, established shared responsibility matching that name.
- Do not include task numbers, developer names, dates, or temporary status in permanent source names unless a real project convention or artifact lifecycle requires them.
- Avoid names that differ only by letter case when the repository may be used on a case-insensitive file system.
- Avoid platform-reserved names, invalid characters, trailing spaces or periods, excessive path length, and names unsupported by the project's tools.

## Creating Directories

- Create a directory only when it represents a clear feature, responsibility, module boundary, package, artifact category, or established convention.
- Do not create a directory solely to contain one small file unless required by the project convention or the directory itself represents a meaningful boundary.
- Do not create speculative directories or placeholder structures for hypothetical future growth.
- Prefer shallow organization for small projects and simple modules.
- Add nesting only when each level communicates useful ownership or dependency information.
- Avoid both excessive fragmentation and oversized catch-all directories.

## Module Boundaries

- Keep each module focused on a coherent responsibility.
- Respect existing dependency directions and public interfaces.
- Do not bypass a module boundary by reaching into another module's internal implementation when an established interface exists.
- Avoid circular dependencies and unnecessary cross-module coupling.
- Introduce a new module boundary only when it clarifies real ownership, lifecycle, reuse, or dependency constraints.
- Do not introduce architectural layers that merely forward calls without adding a meaningful boundary or responsibility.
- Treat changes to major module boundaries or dependency direction as architectural decisions and follow `constraints.md`.

## Shared Code

- Keep code with its primary owner until multiple real consumers justify sharing it.
- Extract shared code only when doing so reduces meaningful duplication or establishes a stable boundary.
- Before adding to a shared module, confirm that the code has no inappropriate dependency on one consumer's internal details.
- Do not centralize unrelated constants, types, components, or utilities solely because they have similar technical shapes.
- Keep shared APIs small and intentional; avoid exposing internal implementation for convenience.

## File and Module Size

- Split a file or module when it contains multiple responsibilities that change independently or when its internal structure has become difficult to navigate safely.
- Do not split files solely to satisfy an arbitrary line-count target.
- Do not merge distinct responsibilities merely to reduce file count.
- Prefer cohesive modules with clear names over many thin forwarding files or one large catch-all file.

## Tests and Fixtures

- Follow the project's established convention for colocated or separate tests.
- Keep test placement predictable and clearly associated with the code or behavior under test.
- Place fixtures and test helpers near their consumers unless they serve multiple genuine owners.
- Keep test-only helpers out of production modules unless the project explicitly exposes test support APIs.
- Do not move tests merely to impose a different organizational preference.

## Assets, Configuration, and Generated Files

- Keep static assets, templates, migrations, fixtures, schemas, and configuration in their established project locations.
- Separate generated files from hand-maintained source when the project supports that distinction.
- Do not manually edit generated files unless the project's workflow explicitly requires it.
- Keep code-generation inputs and outputs in the locations expected by the existing toolchain.
- Follow `git.md` for tracking, ignore rules, and generated artifacts.

## Human-Facing Documentation

- Keep human-facing project documentation under `docs/`.
- Follow `documentation.md` when creating, organizing, or updating files under `docs/`.
- Keep agent instructions under `agents/`; do not use `docs/` to define agent authority or behavior.
- Allow `README.md` under an instruction directory only as the human-readable index defined by `instruction-authoring.md`.
- Do not create a parallel documentation directory when `docs/` already owns human-facing project documentation.

## Moving and Renaming Files

- Move or rename files only when required by the task or when the current location materially obstructs a clear implementation.
- Rename a file when the new name materially improves accuracy, ownership, consistency, or compatibility; do not rename merely for personal preference.
- Do not reorganize unrelated files while implementing a behavioral change.
- Keep broad structural changes separate from unrelated behavioral changes when practical.
- After a move, update affected imports, exports, references, tests, build configuration, scripts, documentation, and ownership metadata.
- Perform case-only renames in a way that version control records reliably across supported platforms.
- Preserve compatibility entry points when required by the project's public contracts.
- Treat broad reorganization and changes to major ownership or dependency boundaries as authority-bound decisions under `constraints.md`.

## Repository Root

- Keep the repository root focused on primary entry points, workspace definitions, essential configuration, and top-level documentation.
- Use the project's established locations for developer scripts, tools, generated output, examples, and temporary artifacts.
- Keep human-facing documentation under `docs/` rather than adding miscellaneous guides to the repository root, except for conventional top-level entry documents required by the project.
- Do not create a new top-level directory when an existing location has the correct ownership.
- A new top-level directory must represent a durable and clearly distinct project-level responsibility.

## Verification

Match structural verification to the impact of the change and follow `verification.md`.

- For a newly added file, verify that its location, imports, exports, naming, and build or package inclusion match comparable files.
- For moves or renames, search for stale paths and references in code, configuration, documentation, and scripts.
- For module-boundary changes, verify affected dependency directions, public entry points, tests, and build behavior.
- Do not run broad structural or project-wide checks for a trivial file addition when focused inspection provides sufficient confidence.

## Project-Specific Structure Documentation

Use `agents/project/` when a project has structural conventions that are not obvious from the repository itself.

Project-specific structure instructions should describe only what helps agents make placement and boundary decisions, such as:

- the responsibilities of major directories and modules;
- allowed dependency directions;
- where features, tests, assets, configuration, migrations, and generated files belong;
- naming, packaging, or colocation conventions;
- public entry points and internal-only areas;
- generated directories that must not be edited;
- deliberate exceptions to the general structure.

Do not duplicate a directory tree without explaining ownership, dependency, or placement rules. Keep project-specific documentation synchronized with material structural changes.
