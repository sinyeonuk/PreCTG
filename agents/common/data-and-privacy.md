# Data and Privacy

This document defines how agents should handle user data, sensitive information, storage, logs, telemetry, and network communication.

## General Principles

- Collect, process, retain, and expose only data required for the confirmed user task.
- Prefer local processing and storage when they satisfy the requirement and no authorized product need requires external transmission.
- Treat personal, authentication, financial, health, location, private content, and user-generated data as sensitive according to its context.
- Follow `constraints.md` for secrets, external actions, cost, and authorization boundaries.

## External Communication and Telemetry

- Do not add telemetry, analytics, tracking, advertising identifiers, crash uploads, or usage reporting unless the user explicitly requests the capability or an applicable project instruction records a previously confirmed requirement.
- Do not add an external network call to a local feature when the call is unnecessary for its confirmed behavior.
- Before transmitting user or project data, identify the destination, purpose, minimum required fields, failure behavior, and applicable user control.
- Do not send secrets, unrelated project content, raw diagnostic data, or sensitive values to an external service.
- Make optional collection and transmission distinguishable from functionality required to complete the user's task.
- Respect established consent, opt-out, offline, and data-residency requirements when they exist.

## Storage and Data Lifecycle

- Store sensitive data only when persistence is required and use the project's established protected storage mechanism when one exists.
- Do not place credentials or sensitive values in source code, ordinary configuration, URLs, analytics fields, or broadly readable local storage.
- Define creation, update, retention, export, and deletion behavior when the feature owns persistent user data.
- Ensure deletion and sign-out behavior clear data that the confirmed product semantics require them to clear.
- Avoid retaining temporary exports, caches, clipboard content, previews, or debug artifacts longer than their task requires.
- Separate test, development, and demonstration data from real user or production data.

## Logs, Errors, and User Interfaces

- Minimize sensitive values in logs, traces, screenshots, notifications, clipboard operations, and error messages.
- Redact or omit secrets and personal data before recording diagnostics.
- Show sensitive values only when the user needs them for the current task, and mask them when full visibility is unnecessary.
- Do not expose internal identifiers as personal or account information when users could misinterpret them.
- Preserve useful diagnostic context without copying raw payloads or private content into user-facing errors.

## Verification

- Inspect changed data flows from input through storage, processing, output, logging, and deletion.
- Verify that external requests contain only intended data and behave safely on failure or offline operation when relevant.
- Check that logs, fixtures, snapshots, screenshots, and generated artifacts do not contain secrets or real sensitive data.
- Confirm that retention, deletion, export, masking, and access behavior match the maintained specification when the task affects them.
