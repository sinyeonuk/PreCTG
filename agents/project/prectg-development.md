# PreCTG Development

This document defines the confirmed project-specific boundaries for PreCTG development.

## Specification Ownership

- Inspect `docs/product-spec.md`, `docs/data-spec.md`, `docs/architecture-and-delivery.md`, `docs/mvp-delivery-plan.md`, and `docs/source-register.md` before substantial implementation or data-generation work.
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

## Maintained Commands

- Install the local development environment with `python -m pip install -r requirements-dev.txt` from an active Python 3.11-or-newer virtual environment.
- Run `prectg status` to verify the installed package and current implementation stage.
- Run `prectg generate --rows 50000 --output data/synthetic/prectg-synthetic.csv` to generate the maintained large synthetic demonstration dataset.
- Run `prectg train --data data/synthetic/prectg-synthetic.csv --output models/prectg-demo.joblib` to train a reproducible local model bundle.
- Run `prectg predict --input <json> [--model <joblib>]` for the maintained machine-readable staged analysis flow.
- Run `prectg predict-batch --input <csv> --model <joblib> --output <csv>` for the maintained batch inference flow.
- Run `python scripts/benchmark.py` to verify the 50,000-row throughput budgets.
- Run `python -m pytest` for the maintained project tests.
- Run `ruff check .` and `ruff format --check .` for source linting and formatting verification.
- Run `streamlit run app/streamlit_app.py` for the local demonstration UI.
- Update this section with the executable configuration when adding or changing a maintained command.

## Implementation Quality

- Add type hints to public functions, model input and output contracts, and domain boundaries.
- Keep clinical rules, ML feature construction, model execution, and user-facing explanation in separate modules with focused responsibilities.
- Avoid hidden global state and pass random seeds, configuration, paths, and model dependencies explicitly.
- Keep tests independent of real network access, external services, and uncontrolled randomness.
- Do not suppress warnings, weaken validation, or disable checks merely to make a run pass.
- Validate generation and training logic on a small dataset before running 50,000-row or larger jobs.

## Definition of Done

- Treat a development step as complete only when it has an executable entry point or callable contract, focused automated tests, verified relevant failure paths, synchronized specifications, and a representative result that can be reviewed.
- Do not mark a step complete merely because its source files exist or its primary success path ran once.
- Apply the applicable Gate criteria and final completion baseline in `docs/mvp-delivery-plan.md`; do not substitute a narrower code-only definition of done.
- Treat teammate acceptance activities, including an unaided demonstration, subjective copy review, presentation rehearsal, and team approval, as user-and-team responsibilities rather than Codex implementation goals.
- Do not keep an otherwise completed Codex goal active or blocked solely because a teammate has not performed an acceptance activity. Hand off the relevant checklist without claiming that the human review passed.
- Include a human acceptance activity in a Codex goal only when the user explicitly assigns Codex an independently executable part of that activity; never impersonate a teammate or fabricate sign-off.

## Data and Leakage

- Treat all locally generated patient-like records as synthetic and label their files and outputs accordingly.
- Preserve the AIHub public field contract at the input boundary and normalize it to consistent internal names behind that boundary.
- Assign every model feature an availability timing from `docs/data-spec.md` and fail training when a target, post-window, post-delivery, unknown-timing, or generator-metadata field is selected.
- Use patient-level or mother/fetus-level grouped splits whenever stable grouping identifiers are available.
- Store generation seeds, schema versions, generator versions, evidence-rule identifiers, and checksums with synthetic dataset outputs.

## Data and Artifact Storage

- Commit only small, human-reviewable synthetic fixtures required by automated tests.
- Do not commit bulk synthetic datasets, trained model binaries, generated charts, run outputs, caches, or logs; reproduce them from tracked code and configuration.
- Never commit real medical data, patient-level records, identifiers, credentials, or unredacted data extracts to this repository.
- Keep real or restricted medical data outside the repository even when local access is authorized.
- Track generation commands, configuration, schema, evidence rules, checksums, and representative validation summaries needed to reproduce generated artifacts.

## Clinical Rule Governance

- Use a clinical rule as a default executable rule only when its source and applicability are recorded in `docs/source-register.md` and its status is approved.
- Distinguish sourced clinical thresholds from synthetic-data assumptions in configuration, code, tests, documentation, and output labels.
- Do not describe synthetic generation weights, scenario strengths, alert thresholds, or arbitrary score weights as clinical standards.
- Update the owning specification, source register, configuration, and relevant tests together when changing a rule, threshold, weight, or precedence decision.
- Leave decisions requiring clinical judgment unresolved until the user or an authorized clinical reviewer confirms them.

## Model Failure Behavior

- Return the ML result as unavailable when the model artifact is missing, incompatible, corrupt, or cannot accept the validated feature contract.
- Do not convert a rule score into a fabricated ML probability or present a deterministic fallback as a trained-model result.
- Prioritize an explicit insufficient-data state over a risk probability when required input quality is below the documented threshold.
- Do not return plausible-looking default predictions after inference, validation, or model-loading failures.
- Preserve usable rule-based results when they can be computed safely, while clearly separating them from unavailable ML results.

## Reproducibility and Model Artifacts

- Save the model version, schema version, ordered feature list, feature availability timing, synthetic generator version, random seed, training configuration, training-data checksum, and dependency versions with every trained model artifact.
- Require a loaded model artifact to match the expected schema and feature contract before inference.
- Make generated outputs reproducible from tracked code, approved configuration, and recorded metadata without relying on undocumented local state.

## RiskGate Reuse

- Reuse RiskGate only as a source of domain-independent patterns such as staged information accumulation, feature separation, leakage checks, grouped splitting, model persistence, input normalization, and explanation structure.
- Do not import RiskGate at runtime or reuse its surgery targets, surgical features, clinical rules, fallback predictions, or recommendation text in PreCTG.
- Record the source and adaptation reason when copying non-trivial RiskGate code into this repository.

## Verification

- Verify schema validation, rule boundaries, leakage rejection, deterministic generation, model persistence, and end-to-end prediction with focused automated tests.
- Treat 50,000-row generation and batch inference as throughput demonstrations, not model-performance validation.
- Keep the synthetic-data and non-clinical-use boundary consistent across the README, CLI output, and machine-readable results. In Streamlit, avoid repeated warning banners but retain a compact synthetic-demo label and the real-patient upload prohibition.

## User Interface

- Use Pretendard as the primary font for the PreCTG frontend and Streamlit demonstration UI.
- Bundle or load Pretendard in a way that remains usable in the intended offline environment; do not make core text rendering depend solely on an external font CDN.
- Use a system sans-serif fallback stack when Pretendard cannot load, and preserve Korean readability across supported screens.
- Keep the UI at the polished-demonstration level defined by `agents/common/ui/foundations.md`, with clear hierarchy, essential accessibility, a compact synthetic-demo label, and a visible real-patient upload prohibition.

## Git Workflow

- Treat `origin` as the authorized project remote for this repository and use the `main` branch unless the user explicitly requests another branch.
- Treat Git commit and push operations for this repository as delegated to Codex for the duration of the project, unless the user explicitly revokes or narrows that delegation.
- Do not ask a teammate to perform routine commit or push steps, and do not request per-commit confirmation for changes within the current task scope.
- Review the working tree and staged diff before committing, and do not include unrelated or unexplained files.
- Write commit messages in natural, concise Korean intended for the project team; describe the actual change and avoid translation-like wording, generic messages, and unnecessary prefixes.
- Group related changes into a coherent commit and choose commit boundaries pragmatically; do not create a separate commit for every small edit or intermediate step.
- Push verified commits to the configured remote at a sensible milestone, such as completion of a coherent feature, documentation unit, or stable checkpoint.
- Report the commit hash, branch, push result, and any files intentionally excluded when handing off the change.
