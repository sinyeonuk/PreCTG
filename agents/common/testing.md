# Testing

This document defines how agents should create and maintain tests that provide reliable evidence about project behavior.

## General Principles

- Test observable behavior, contracts, and outcomes rather than duplicating implementation details.
- Add or update tests when the task changes behavior and a focused automated test can prevent a plausible regression.
- Match test scope to the task impact and the project's established testing strategy.
- Prefer the lowest test level that proves the behavior without hiding important integration boundaries.
- Do not add tests solely to increase test counts or coverage percentages.
- Follow `verification.md` for deciding which checks to execute and report.

## Choosing Test Coverage

- Reproduce a fixed defect in a regression test when the behavior is stable and the test is practical.
- Cover important success, failure, boundary, and recovery paths affected by the change.
- Preserve existing public behavior in tests when compatibility is required.
- Use snapshots only when reviewing the complete serialized or rendered output is meaningful and stable; do not use them as a substitute for behavioral assertions.

## Test Perspectives

- Prefer black-box tests for public APIs, user-visible behavior, and stable contracts.
- Use white-box tests for important internal invariants, complex algorithms, recovery branches, or failure paths that cannot be exercised reliably through a public boundary.
- Assert the relevant invariant or outcome in a white-box test without coupling the test to incidental call order, private names, or replaceable implementation structure.
- Replace or revise a white-box test when it prevents a behavior-preserving refactor without protecting a meaningful invariant.

## Test Levels and Boundaries

- Use focused unit or component tests for isolated decisions and transformations.
- Use contract tests where independently changing components, services, adapters, or providers must agree on an interface.
- Use integration tests when the risk lies in wiring, serialization, persistence, framework behavior, or communication across a real boundary.
- Use end-to-end tests for critical user journeys and system-level risks that lower test levels cannot represent faithfully.
- Avoid broad end-to-end coverage for behavior that a focused lower-level test proves more reliably and cheaply.
- Choose a small combination of test levels when different risks cannot be represented honestly at one level.

## Isolation and Test Doubles

- Keep tests independent of execution order and unrelated shared state.
- Control time, randomness, environment, filesystem, network, and concurrency when they would otherwise make the result nondeterministic.
- Mock external or expensive boundaries when appropriate, but do not mock the behavior under test.
- Prefer small, explicit fakes or fixtures over deep mock chains that reproduce implementation structure.
- Keep fixtures minimal, readable, and representative of the behavior being verified.
- Do not use real user data, production credentials, or uncontrolled paid or external services in tests.

## Assertions and Failures

- Make assertions specific enough that a failure identifies the violated behavior.
- Avoid assertions that pass despite missing output, swallowed errors, or incomplete execution.
- Verify user-visible or contractually significant error behavior when failure handling changes.
- Do not weaken assertions, delete relevant tests, add unconditional retries, or increase timeouts merely to make a failing test pass.
- Investigate flaky tests and remove their nondeterministic cause when it was introduced or exposed by the current task.

## Test Maintenance

- Update or remove tests only when the corresponding requirement or supported behavior has changed.
- Keep test names aligned with the behavior and condition they verify.
- Remove temporary diagnostics and test-only shortcuts introduced during investigation.
- Keep helpers close to their consumers until multiple real test owners justify sharing them.
- Do not rewrite unrelated tests to impose a preferred style during a scoped task.
- Treat coverage reports, mutation scores, and similar metrics as diagnostic evidence rather than completion targets.
