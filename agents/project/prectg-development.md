# PreCTG Development

This document defines the confirmed project-specific boundaries for PreCTG development.

## Specification Ownership

- Inspect `docs/product-spec.md`, `docs/data-spec.md`, `docs/architecture-and-delivery.md`, and `docs/source-register.md` before substantial implementation or data-generation work.
- Update the document that owns a changed product, data, architecture, or evidence decision in the same task as the implementation change.
- Keep unverified clinical thresholds and unresolved AIHub field timing out of default executable rules until the source register marks the supporting rule as approved.

## Product Boundary

- Build PreCTG as a local, CPU-compatible MVP for functional demonstration with synthetic data.
- Do not represent synthetic-data metrics as clinical performance or use PreCTG for diagnosis, treatment, or real patient decisions.
- Keep deployment, hospital integration, cloud services, deep learning, and raw CTG image extraction outside the MVP unless the user expands the scope.

## Technology and Environment

- Use Python 3.11 as the local development target.
- Use LightGBM as the primary tabular ML model and scikit-learn-compatible pipelines for preprocessing and evaluation.
- Keep the runtime offline-capable and avoid external inference APIs, telemetry, and services that require network access.
- Prefer dependencies listed in `docs/architecture-and-delivery.md`; ask before introducing a new framework, runtime, service, or foundational dependency.

## Data and Leakage

- Treat all locally generated patient-like records as synthetic and label their files and outputs accordingly.
- Preserve the AIHub public field contract at the input boundary and normalize it to consistent internal names behind that boundary.
- Assign every model feature an availability timing from `docs/data-spec.md` and fail training when a target, post-window, post-delivery, unknown-timing, or generator-metadata field is selected.
- Use patient-level or mother/fetus-level grouped splits whenever stable grouping identifiers are available.
- Store generation seeds, schema versions, generator versions, evidence-rule identifiers, and checksums with synthetic dataset outputs.

## RiskGate Reuse

- Reuse RiskGate only as a source of domain-independent patterns such as staged information accumulation, feature separation, leakage checks, grouped splitting, model persistence, input normalization, and explanation structure.
- Do not import RiskGate at runtime or reuse its surgery targets, surgical features, clinical rules, fallback predictions, or recommendation text in PreCTG.
- Record the source and adaptation reason when copying non-trivial RiskGate code into this repository.

## Verification

- Verify schema validation, rule boundaries, leakage rejection, deterministic generation, model persistence, and end-to-end prediction with focused automated tests.
- Treat 50,000-row generation and batch inference as throughput demonstrations, not model-performance validation.
- Keep the synthetic-data and non-clinical-use warning consistent across the README, CLI output, machine-readable results, and Streamlit UI.
