# UI Interaction

This document defines how agents design user flows, information architecture, forms, confirmations, interface states, and feedback.

## User Flows and Information Architecture

- Design the complete in-scope user flow before optimizing individual components.
- Prioritize successful task completion over component-level perfection.
- Organize the interface around user goals and domain concepts rather than a catalog of available components.
- Show only information and controls needed for the current task and decision.
- Reveal advanced, infrequent, or conditional options progressively when immediate display would create avoidable complexity.
- Keep essential actions and information visible; do not hide them merely to make the interface appear minimal.
- Choose sensible, safe defaults that reduce user effort without concealing consequential choices.
- Preserve user context and progress across steps whenever practical.

## Navigation and Task Completion

- Define the intended destination for successful completion, cancellation, failure recovery, ordinary back navigation, and direct entry before implementing a multi-step flow.
- Distinguish temporary task steps from durable destinations that remain meaningful after the task ends.
- When a child flow completes and its existing origin is the natural destination, return to that origin and remove completed intermediate steps from the navigation stack.
- Do not push a new instance of the origin merely to simulate returning to it.
- Do not require users to traverse completed task steps with repeated back actions unless those steps remain meaningful destinations after completion.
- Use replacement, stack reset, pop-to-origin, flow dismissal, or the equivalent established by the platform and project navigation architecture.
- Preserve step-by-step back navigation while a task is in progress when returning to an earlier step remains useful.
- Treat successful completion separately from ordinary back navigation: completion may collapse the task flow while back may move through its previous steps.
- Keep a result or review screen after completion only when it supports a clear next task, confirmation need, recovery option, or user decision.
- Refresh or reconcile changed origin content without creating a duplicate origin screen when the completed task changes its data.
- Treat each top-level tab as a stable destination rather than a page pushed onto another tab's stack.
- Do not accumulate duplicate tab roots when switching tabs, reselecting a tab, or completing a task within a tab.
- Preserve or reset each tab's internal state according to established product and platform behavior; do not invent reset, scroll-to-top, or stack-clearing behavior without a relevant precedent or requirement.
- Preserve meaningful browser history, deep-link, and platform back behavior when those navigation contracts apply.

## Forms and Confirmations

- Request only information necessary for the current task.
- Clearly identify required and optional fields without relying only on color.
- Use suitable input types, labels, instructions, defaults, and autocomplete behavior.
- Validate as early as useful without interrupting users before they have had a reasonable chance to complete the input.
- Preserve entered values when validation or submission fails.
- Place validation feedback near the affected field and provide a useful summary when multiple errors would otherwise be difficult to find.
- Prevent duplicate submissions and show clear progress and completion feedback.
- Require confirmation only for destructive, high-impact, or difficult-to-reverse actions.
- Prefer prevention, clear labeling, constrained choices, or undo over repetitive confirmation dialogs for routine reversible actions.

## Asynchronous Operations and Recovery

- Give immediate feedback that an action was received without presenting completion before it actually occurs.
- Keep useful existing content and user context visible during background refresh when replacing it with a blocking loader would not help the task.
- Prevent accidental duplicate requests and make intentional repeated actions distinguishable when repetition is valid.
- Allow cancellation when an operation is long-running, no longer useful, and safely cancellable; explain when cancellation cannot stop work already committed.
- Provide a useful recovery path for timeout, offline, interrupted, and retryable failures without discarding valid user input.
- Use optimistic updates only when failure can be detected and the previous state can be restored or reconciled clearly.
- Distinguish full success, partial success, queued work, cancellation, and failure when they require different user actions.
- Do not hide partial failures behind a generic success message.
- Handle stale or concurrently changed data without silently overwriting newer user or server state.
- Show continuing status and a discoverable result for background work that outlives the initiating screen.
- Preserve task state across refresh, navigation, or reconnection when losing it would create significant user effort or risk.
- Do not imply offline support when the required operation cannot complete without a connection.

## States and Feedback

- Implement relevant hover, focus, active, selected, disabled, loading, empty, success, and error states.
- Match state coverage to the selected implementation level and the flows in scope.
- Do not leave important interactions without visible feedback.
- Make empty states explain what is absent and suggest the next useful action when one exists.
- Distinguish an empty result from loading, failure, and permission-denied states.
