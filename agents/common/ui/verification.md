# UI Verification

This document defines proportionate rendered, interaction, and delivery verification for user-interface changes.

## Visual Verification

Match UI verification effort to the impact of the change and follow `agents/common/verification.md`.

For localized, substantial, or high-risk UI changes that can affect rendering or interaction:

- Inspect the rendered result instead of relying only on source code.
- Check the primary target viewport and at least one materially different viewport when responsive behavior is affected.
- Exercise important interaction and state changes relevant to the modified flow.
- Check for overflow, clipping, misalignment, unreadable contrast, unstable layout, and inconsistent styling.
- Compare peer interface text for consistent terminology, grammatical form, tone, and punctuation when copy is added or changed.
- Compare the result with the established design system and surrounding screens.

Do not perform broad visual regression, multi-viewport review, or exhaustive state checks for trivial copy edits or changes that cannot affect layout or behavior.

## Interaction and Recovery Verification

For changes that affect asynchronous operations or recoverable user input:

- Exercise success, retryable failure, non-retryable failure, cancellation, timeout, and offline behavior that is relevant to the modified flow.
- Confirm repeated activation does not create unintended duplicate submissions or operations.
- Verify that failed validation, submission, retry, and reconnection preserve valid user input and context.
- Check optimistic and partial updates for clear rollback, reconciliation, and result status.
- Confirm stale or concurrently changed data is not silently overwritten when the affected system exposes that risk.
- Verify that background work remains discoverable after leaving or revisiting the initiating screen when it is designed to continue.

## Accessibility Verification

For localized, substantial, or high-risk changes to interactive UI:

- Complete the primary flow with a keyboard when the target platform supports keyboard interaction.
- Check focus order, visible focus, temporary-layer focus containment, and focus restoration.
- Inspect accessible names, roles, states, relationships, validation feedback, and dynamic announcements relevant to the change.
- Check text enlargement or zoom and at least one materially narrower layout when content can reflow.
- Check reduced motion, high contrast, forced colors, touch targets, and non-pointer input when the change or target environment makes them relevant.
- Use automated accessibility checks as supporting evidence rather than a substitute for exercising the actual flow.

## Navigation Verification

For changes that affect navigation or multi-step tasks:

- Complete the flow and use back navigation to confirm that completed intermediate steps do not reappear when they no longer have meaning.
- Confirm that completion returns to the intended existing destination without adding a duplicate origin or tab root.
- Exercise ordinary back, cancellation, successful completion, and failure recovery separately when they have different intended destinations.
- Repeat the flow and switch or reselect relevant tabs to confirm that duplicate screens and task steps do not accumulate.
- Check direct entry, deep links, browser history, and platform back behavior when the modified flow supports them.
- Confirm that returning to the origin shows the completed task's current data without unnecessarily replacing the origin screen.

## Delivery

- State which UI implementation level was used and why when it materially affected the work.
- Mention intentional limitations, deferred states, or unverified visual risks.
- Mention a newly established or intentionally changed UI copy convention when it materially affects the interface.
- Do not describe a prototype or demonstration as production-ready when production requirements were not implemented and verified.
