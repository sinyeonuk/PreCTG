# UI Foundations

This document defines how agents determine UI goals, visual direction, implementation depth, and system-level design decisions.

## General Principles

- Prioritize clarity, consistency, and usability over visual novelty.
- Design for real user tasks rather than demonstrating technical capability.
- Make interactive elements clearly identifiable and provide appropriate feedback.
- Prevent user mistakes where reasonably possible and make recovery clear.
- Do not ask the user to choose routine visual details that can be inferred from the existing design system, surrounding interface, product context, or established conventions.

## Decision Hierarchy

When UI principles conflict, prioritize:

1. User task completion
2. Correctness and safety
3. Accessibility
4. Consistency
5. Simplicity
6. Visual polish

Do not use this hierarchy to ignore explicit requirements or applicable safety and accessibility standards. Use it to choose between otherwise valid design options.

## Determine the UI Target

Before localized, substantial, or high-risk UI design or implementation, determine the intended use and required level of finish.

First inspect available project context, including:

- instructions under `agents/project/`;
- relevant files under `docs/`;
- the project README and product requirements;
- existing design-system documentation and surrounding screens.

When the project purpose and expected UI level are clearly documented, do not ask the user to repeat them. State the inferred target before implementation, identify the supporting project context, and proceed at that level.

When the purpose or expected level is not clear, explicitly ask the user whether the UI needs production-quality finish for real users, polished demonstration or user validation, or primarily functional support for backend and logic validation. Explain briefly how the answer will affect implementation depth.

Treat UI implementation level and deployment scope as separate decisions. A production-quality UI target does not authorize deployment, commercial release, store submission, monetization, or deployment-specific work.

Do not begin consequential visual design while this choice remains unresolved. A separate question is unnecessary for trivial, style-preserving changes where the answer would not affect the result, such as correcting copy or applying an established component variant.

Do not repeatedly ask for the UI target within the same project once it has been established, unless later requirements conflict with it or the intended use materially changes.

## User and Usage Context

Before designing a new interface or materially changing a user flow, inspect or establish the context that affects design decisions:

- the primary users, their relevant domain knowledge, and their familiarity with the product;
- the task they need to complete, how often they perform it, and the cost of delay or error;
- the primary devices, screen conditions, input methods, and environments in which the task occurs;
- existing workflows, alternatives, terminology, and expectations users bring to the task; and
- relevant accessibility, localization, connectivity, privacy, or data-sensitivity needs.

- Use project evidence and actual user requirements instead of inventing personas or unsupported preferences.
- Distinguish confirmed context from assumptions when it materially affects the design.
- Do not ask the user to restate context already established by project instructions, maintained specifications, existing product behavior, or surrounding interfaces.
- Include consequential missing user or environment context in the UI target clarification rather than asking a series of low-impact design questions.
- Optimize for the primary task and users without making required secondary flows unusable.

## Implementation Levels

### Production-Quality Interface

- Deliver a polished, production-ready interface suitable for real users.
- Fully address responsive behavior, accessibility, interaction feedback, content hierarchy, important states, and visual consistency.
- Avoid placeholder content, incomplete flows, or demo-only shortcuts unless explicitly accepted.

### Polished Demonstration or User Validation

- Prioritize a convincing and coherent experience for the flows under evaluation.
- Make the demonstrated paths visually polished and realistic.
- Implement responsive behavior, accessibility, and secondary states to the degree relevant to the evaluation, and clearly identify intentional limitations.
- Do not fabricate functional depth behind interactions that are presented as working.

### Functional or Logic Validation

- Prioritize clarity, speed of use, and reliable access to the behavior being validated.
- Keep visual treatment simple but coherent and professional.
- Maintain essential accessibility, readable hierarchy, usable controls, and layout stability.
- Do not spend time on decorative polish, extensive animation, or unrelated screen refinement.
- Do not use the lower visual target as permission for broken, confusing, or inconsistent UI.

These levels control implementation depth, not correctness. Every level must remain usable, understandable, and internally consistent.

## Inspect Before Designing

Before creating or materially modifying UI:

1. Inspect existing screens that support similar user tasks.
2. Inspect the complete flow into, through, and out of the affected interface.
3. Identify reusable layouts, components, interactions, states, spacing, terminology, and content patterns.
4. Reuse a suitable precedent when one exists.
5. Create a new pattern only when existing patterns cannot support the requirement clearly.

Do not infer a design system from one isolated component when broader project evidence is available.

## Existing and New Interfaces

### Existing Interfaces

- Preserve the established design system, visual language, and interaction patterns.
- Match surrounding spacing, typography, colors, components, and behavior.
- Improve only within the requested scope; do not redesign unrelated screens.
- Do not replace an established direction merely because another style is personally preferable.

### UI Improvement Requests

- Identify concrete usability, hierarchy, consistency, accessibility, or responsiveness problems before changing the design.
- Prioritize changes with clear user value over subjective restyling.
- Prefer focused improvements over a complete redesign unless the request requires one.
- Be able to explain what each material design change improves.

### New Interfaces

- When no established design direction exists, create a coherent direction appropriate to the product purpose and selected implementation level.
- Use familiar interaction patterns for common controls and workflows.
- Establish a deliberate hierarchy, spacing system, typography, color usage, component language, and state behavior.
- Do not produce a generic showcase page when the product calls for an application interface.

## Components and Design Systems

- Reuse established components and tokens when they satisfy the requirement.
- Create a component abstraction only when it has a clear responsibility and justified reuse or consistency value.
- Do not introduce a new design system, component library, naming system, token layer, or visual abstraction unless project scale and requirements justify it.
- Do not create chains of thin wrapper components or variants that add no meaningful behavior, styling contract, or ownership boundary.
- Keep one-off UI local when promoting it into shared infrastructure would be premature.

## Visual Restraint

Avoid generic showcase styling that does not support the product's purpose, including:

- excessive gradients, glows, glass effects, and decorative shapes;
- oversized promotional text in routine application screens;
- unnecessary cards around every content group;
- excessive pill-shaped controls;
- arbitrary animations or hover transforms;
- decorative copy that obscures the primary task;
- inconsistent icon styles or ornamental icons without meaning.

Expressive visual treatments are appropriate when they support the product, brand, content, or requested direction. Do not apply them as defaults.
