# Quality Assurance

This document defines risk-based quality assurance for determining whether changed behavior is fit for its intended use.

## General Principles

- Derive quality assurance from requirements, acceptance criteria, supported use, and changed risks.
- Treat automated tests as evidence within quality assurance rather than as the whole quality assurance process.
- Scale scenario depth to task impact and concentrate effort where failure would be costly, difficult to detect, or difficult to recover from.
- Verify only environments, platforms, and compatibility promises the project actually supports.
- Follow `verification.md` for proportional command execution and `testing.md` for automated test design.

## Preparing the Review

- Identify the user, system, or operator outcomes that define successful completion.
- Trace each consequential requirement or acceptance criterion to at least one form of evidence.
- Identify affected boundaries, dependencies, stored data, permissions, and recovery paths.
- Reuse existing project checklists and acceptance procedures when they remain current.
- Resolve unclear completion criteria before relying on assumptions that could materially change the result.

## Scenario Selection

- Cover the primary successful workflow and the most plausible failure modes introduced or affected by the change.
- Include relevant boundary values, empty states, invalid input, interruption, retry, cancellation, partial completion, and recovery.
- Check backward compatibility, migration, and existing-data behavior when formats, persistence, or public contracts change.
- Check authorization, privacy, and data-loss risks when the change handles user data or privileged actions.
- Check accessibility and supported viewport or input modes when the user interface changes.
- Check performance only against a requirement, established budget, or demonstrated risk.

## Automated and Exploratory Evidence

- Automate stable, repeatable scenarios when the expected value exceeds the maintenance cost.
- Use focused exploratory testing when behavior depends on interaction, integration, environment, timing, or usability that automation does not represent faithfully.
- Keep exploratory checks bounded by a stated risk or question instead of performing an undefined general review.
- Record reproducible steps, expected behavior, actual behavior, and relevant environment details for a discovered defect.
- Do not substitute screenshots, coverage percentages, or a successful build for evidence that the required behavior works.

## Defect Handling

- Classify a defect by user impact, likelihood, scope, recoverability, and data or security consequences.
- Block completion for a defect that violates a required outcome, corrupts data, weakens security or privacy, or leaves a critical workflow unusable.
- Fix task-caused defects within scope and recheck the affected scenario.
- Report unrelated or lower-impact defects without silently expanding the task.
- Re-run only the scenarios and checks affected by a fix, plus broader checks when shared boundaries or high-risk behavior changed.

## Completion Evidence

- Confirm that every required outcome has credible evidence or an explicitly reported verification gap.
- Distinguish what was automated, manually inspected, inferred, or not verified.
- Report remaining risks in terms of user or system impact rather than internal tool output alone.
- Do not claim general product quality from checks limited to the changed area.
