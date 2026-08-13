# UI Content

This document defines information density, authenticity, interface language, voice, terminology, and localization requirements.

## Authenticity and Information Density

- Display content and metadata only when they support the user's current task, decision, or understanding.
- Do not expose internal IDs, UUIDs, hashes, timestamps, versions, diagnostics, or operational metadata in normal user workflows without a user need.
- Do not fabricate dashboards, statistics, testimonials, activity, navigation items, integrations, product capabilities, or business content.
- Use realistic placeholder content only when necessary to evaluate layout or interaction, and make its placeholder status clear when users could mistake it for real data.
- Do not create controls or links that imply unavailable functionality.
- Keep expert diagnostics and operational metadata in an appropriate advanced, administrative, or developer context.

## Data Presentation

- Format dates, times, numbers, currency, percentages, and units according to the user's locale and the product's established conventions.
- Make the relevant time zone explicit when users could otherwise misinterpret a time or deadline.
- Distinguish zero, empty, unknown, unavailable, not applicable, loading, and failed-to-load values when they have different meanings.
- Show data freshness or last-updated context when decisions depend on whether information is current.
- Use predictable sorting and state the active sort or comparison basis when it is not obvious.
- Preserve access to a complete value when truncating long text, identifiers, labels, or paths is necessary for layout.
- Avoid false precision, inconsistent rounding, or abbreviated values that could materially change interpretation.
- Mask sensitive values when full visibility is unnecessary and provide deliberate reveal behavior only when the user needs it.
- Label table and chart units, scales, periods, categories, and comparison baselines clearly.
- Do not use color alone to distinguish series, trends, thresholds, or status.
- Do not imply a trend, causal relationship, completeness, or certainty that the available data does not support.

## UI Copy and Voice

- Treat interface language as part of the design system, not as incidental placeholder text.
- Follow `agents/common/terminology.md`, project-specific terminology, localization guidance, brand voice, and content standards when they exist.
- Infer the established voice from comparable nearby interface text before writing or revising copy.
- Keep peer elements consistent in grammatical form, tone, politeness level, tense, capitalization, punctuation, and sentence endings.
- Use parallel wording for items that perform equivalent roles, including tabs, navigation items, buttons, menu actions, headings, status messages, empty states, and validation messages.
- Do not mix formal and casual language, sentence and fragment styles, or different honorific levels within the same interface context without a deliberate semantic reason.
- Keep labels concise and action-oriented where appropriate, while making instructions and error messages specific enough to act on.
- Match punctuation to the component type and existing convention. For example, peer tabs or buttons should not differ arbitrarily in terminal punctuation.
- Preserve intentional differences when they communicate different roles, urgency, audiences, or states; consistency does not require identical phrasing everywhere.
- When modifying one item in a repeated set, inspect its peers and make the changed item consistent without rewriting unrelated product copy beyond the task's scope.
- Do not ask the user to choose routine wording when an established product voice or surrounding pattern provides the answer.
- Ask before establishing a new brand voice or changing the product-wide tone when no clear precedent or project instruction exists.

Write from the user's mental model rather than the implementation's internal model:

- Describe the user's action, object, progress, outcome, or next step instead of exposing internal architecture or development operations.
- Replace developer-centric process labels with user-facing meaning when the technical detail does not help the user act. For example, prefer `Finding the problem...` over `Running debug...` in a general-user interface.
- Do not expose terms such as `API`, `payload`, `schema`, `stack trace`, `exception`, `null`, internal identifiers, or service names merely because the implementation uses them.
- Translate internal failures into a clear user impact and useful recovery action while preserving diagnostic detail in appropriate logs or developer views.
- Do not reveal sensitive implementation details, infrastructure names, or raw error output in user-facing messages.
- Keep necessary domain terminology when the intended users understand it and it improves precision or actionability.
- In developer tools, administrative diagnostics, and other expert interfaces, use technical terminology deliberately and consistently when it is part of the user's task.
- Do not replace a precise, necessary term with vague wording that prevents the user from understanding the problem or taking the correct action.

Use these defaults when the project does not define a copy standard:

- Use concise action labels for buttons and menu items, such as `Save` or `Try again`, without terminal punctuation.
- Use short noun phrases for tabs, navigation items, field labels, and section headings.
- Use clear complete sentences for confirmations, errors, warnings, empty states, and explanatory text.
- State what happened before optional supporting detail in status feedback.
- Write error messages that explain the problem and, when known, the next useful action.
- Avoid unnecessary exclamation marks, humor, blame, technical jargon, and promotional language in routine product feedback.

For localized interfaces:

- Preserve the established honorific level, formality, and sentence-ending style within each language.
- Do not translate word for word when doing so produces unnatural or inconsistent interface language.
- Preserve variables, placeholders, markup, pluralization rules, and interpolation syntax exactly as required by the localization system.
- Allow natural grammatical differences between languages while preserving meaning, component role, and product voice.

When no copy convention exists and the choice materially affects the product voice, include it when determining the UI target. Once established, apply it consistently without asking about each string.
