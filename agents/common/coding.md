# Coding

This document defines general implementation principles for coding agents.

## General Principles

- Prioritize readability over clever or overly concise code.
- Prefer the simplest solution that satisfies the requirements.
- Follow the project's existing coding style, naming, formatting, and patterns.
- Use descriptive names for variables, functions, classes, modules, and files.
- Avoid unnecessary complexity, abstraction, and premature optimization.
- Write code that makes its purpose clear without requiring additional explanation.

## Standard Solutions

- Do not reinvent well-established solutions.
- Prefer existing project dependencies and platform features when they provide a clear, maintainable solution.
- Prefer a mature, well-maintained library over custom implementation for complex, security-sensitive, or standards-driven functionality.
- Implement a custom solution only when existing suitable solutions do not satisfy the requirements.
- Do not build frameworks, utilities, or abstractions that duplicate an existing suitable solution.
- Prefer an established industry standard unless a project-specific reason justifies otherwise.

## Dependency Selection

- Do not add a dependency when the platform or an existing project dependency can solve the problem simply and clearly.
- Add a dependency only when its value outweighs its maintenance and operational cost.
- Before adding a dependency, consider maintenance activity, security history, license compatibility, size, runtime impact, transitive dependencies, and supported-environment compatibility.
- Prefer a focused dependency over a large framework for a narrow requirement.
- Respect the project's package manager and lockfile conventions.
- Include required lockfile changes when the dependency change is authorized.
- Do not replace or upgrade unrelated dependencies as incidental cleanup.
- Treat a new framework, runtime, hosted service, or foundational dependency as an architectural decision requiring user authorization.

## Reuse and Abstraction

- Reuse existing implementations when they remain suitable.
- Avoid duplicating logic without a clear justification.
- Extract reusable code only when doing so improves ownership and maintainability.
- Do not introduce an abstraction before its responsibility and consumers are understood.

## Design Principles

- Treat SOLID and similar design principles as decision aids rather than mandatory patterns.
- Define a responsibility by its ownership and reasons to change rather than by arbitrary file, class, or function size.
- Introduce an extension point only when a real variation, volatile dependency, or supported customization requires it.
- Preserve substitutability when using inheritance or interchangeable implementations.
- Keep interfaces focused on the needs of their consumers.
- Invert dependencies at meaningful boundaries such as external systems or volatile infrastructure; do not create an interface for every implementation.
- Prefer direct code when an additional layer would only forward calls or rename an existing concept.

## Functions

- Keep functions focused on one responsibility and reasonably small.
- Avoid deeply nested logic by returning early when appropriate.
- Prefer composition over unnecessary inheritance.
- Follow `project-structure.md` for file placement, module ownership, and structural boundaries.

## Error Handling

- Handle expected errors explicitly.
- Do not silently ignore exceptions or failures.
- Provide error messages with enough context for the intended audience to act on them.
- Preserve the project's established error propagation and recovery conventions.

## Comments

- Prefer self-explanatory code.
- Add comments when intent, constraints, or non-obvious reasoning cannot be expressed clearly through code alone.
- Keep comments synchronized with the code.
- Do not use comments to restate obvious implementation details.

## Performance

- Prioritize correctness and maintainability over micro-optimization.
- Optimize only when requirements, measurement, or a demonstrated bottleneck justify it.
- Avoid clearly unnecessary allocations, queries, network calls, or computations.
- Do not trade away clarity for speculative performance gains.

## Maintainability

- Keep changed code easy to understand, test, and modify.
- Remove obsolete code only when its removal is directly related to the task and allowed by `constraints.md`.
- Preserve compatibility and public contracts as required by `constraints.md`.
- Follow `refactoring.md` when the task changes internal structure without intending to change supported behavior.

## Testability

- Write code that can be verified through the project's established testing approach.
- Avoid designs that introduce unnecessary global state, hidden dependencies, or other barriers to focused testing.
- Follow `testing.md` when creating or changing tests.
- Follow `verification.md` for deciding which checks to run.
