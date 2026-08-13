# Quality

This document defines the minimum completion quality for code and configuration changes.

## General Principles

- Ensure the implementation satisfies the requested requirements.
- Preserve required behavior and compatibility as defined in `constraints.md`.
- Complete all requested changes.
- Do not leave partially implemented behavior or placeholder implementations unless explicitly requested.

## Reliability

- Handle expected errors appropriately.
- Avoid silent failures.
- Consider common edge cases relevant to the changed behavior.
- Keep affected behavior deterministic and recoverable where the project requires it.

## Documentation

- Follow `documentation.md` for human-facing project documentation.
- Follow `coding.md` for code comments.
- Do not declare completion when the current change leaves affected documentation or comments inaccurate.

## Cleanliness

- Remove unused imports, variables, dead code, temporary diagnostics, and debugging output introduced by the change.
- Do not leave commented-out code unless explicitly requested.
- Keep modified files internally consistent and usable.

## Build Integrity

- Do not knowingly leave the affected project or module broken or unbuildable.
- Follow `verification.md` before declaring completion.

## Quality Assurance

- Follow `quality-assurance.md` when the task requires acceptance review, exploratory testing, or evidence across multiple quality risks.
- Do not treat a successful build, lint result, or test suite as proof of qualities it does not evaluate.

## Improvement Requests

- Treat requests to improve, optimize, or refactor as requests for meaningful improvement rather than perfection.
- Follow `refactoring.md` when improving internal structure while preserving supported behavior.
- Prioritize changes with clear value in readability, maintainability, correctness, reliability, accessibility, or performance.
- Stop when the requested objective has been achieved with a meaningful improvement.
- Do not continue refining with diminishing returns.
- Ignore trivial or purely subjective improvements unless explicitly requested.
- Report low-impact further improvements as optional recommendations instead of implementing them.

## Completion Standard

- Deliver all modified files in a coherent and usable state.
- Do not declare completion while known task-caused failures or required work remain unresolved.
- Follow `communication.md` for the final user-facing report.
