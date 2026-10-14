# SRS coverage guide

This is an adaptable guide, not a claim of ISO/IEEE conformity. A mandated standard/template takes precedence; obtain its applicable requirements before claiming compliance.

## 1. Document control and purpose

System, version/date, release, evidence/lifecycle status, scope, audience, terminology, sources, and canonical PRD or stakeholder needs. Distinguish current behavior, target behavior, and migration requirements.

## 2. System context

Boundary, actors/external systems, environments, responsibilities, assumptions, constraints, and dependencies. Use a context diagram when helpful. Record stack/hosting choices only when constrained; label proposed architecture or put it in a separate design document.

## 3. Actors and authorization

Identity/authentication, roles, allowed actions, resource scopes, ownership/tenant boundaries, and denial behavior. Use a role/action matrix when useful. Include grant/revocation and session behavior if relevant. UI visibility alone does not specify enforcement.

## 4. Functional requirements

Each independently verifiable obligation gets `FR-001` and a parent PRD/source link:

- Subject, required observable behavior, and conditions.
- Source/rationale, priority/release, evidence/lifecycle.
- Actor/scope, trigger/preconditions, inputs and validation.
- State changes, persisted effects, outputs, business rules.
- Failure/denial and recovery behavior.
- Acceptance/verification IDs and dependencies.

Use shared `BR-001` records for repeated domain rules. Specify duplicate submission, retry, concurrency, and transaction outcomes where correctness depends on them. Split independent behavior; avoid prescribing framework internals without a constraint.

## 5. Data requirements

Entities/domain fields, types/units, optionality, uniqueness, relationships, state/lifecycle, validation, source of truth, ownership, retention/deletion, imports/exports, and missing/stale/duplicate data. Separate domain data dictionary from proposed physical database schema.

## 6. External and user interfaces

For relevant interfaces: direction, provider/consumer, known protocol/format, operations, fields, authentication/authorization, validation, errors, timeout/retry, rate/size limits, versioning, and fallback. Cite provider contracts or mark them open; do not invent guarantees.

For UI: navigation, required states, input feedback, accessibility, and agreed device/browser support. Link designs. For async integrations: delivery expectations, duplicate/out-of-order outcomes, reconciliation when applicable.

## 7. Nonfunctional requirements

Each `NFR-001` includes metric, threshold, operating conditions, measurement boundary, method, source, and status. Consider applicable categories:

| Category | Conditions for verification |
|---|---|
| Performance/capacity | Operation, percentile, data size, concurrency, environment, time window |
| Availability/reliability | Service boundary, observation period, exclusions, failure behavior |
| Recovery | RPO/RTO, incident, backup/restore method |
| Security/privacy | Resource, access/threat condition, enforced outcome, evidence |
| Accessibility/usability | Mandated standard/version if any, task/device, method |
| Compatibility | Supported clients/versions and behavior |
| Operations/maintainability | Diagnostic/audit need, retention/redaction, observable criteria |

Avoid undefined “fast,” “secure,” or “scalable.” Unknown thresholds are open decisions or labeled proposals, not confirmed numbers.

## 8. Conditional domain requirements

Only when relevant: localization/time zones/currency, report formulas, geospatial validity, payments/reconciliation, offline sync, backward compatibility/migration, regulated records, and AI.

For AI: deterministic rules versus suggestions, human authority, allowed data scope, output evidence/uncertainty, fallback, evaluation dataset/quality targets, prompt-injection boundaries, and privacy. Do not promise model factual correctness or invent automated decision authority.

## 9. Verification and release acceptance

Map in-scope FR/NFR/BR/data/interface obligations to planned cases or justified inherited coverage. Specify setup, action/input, expected result, method (test/inspection/analysis/demonstration), environment, and evidence to collect. Include failure, denied, invalid, and boundary cases proportionate to risk. Cases remain planned until executed.

## 10. Traceability, risks, and decisions

Use the shared matrix/gates. Expose orphan requirements, conflicts, unconfirmed targets, dependencies, migration risks, and blockers. Unknown owners/dates remain unknown or labeled proposals. Record downstream impact of baseline changes.

For a full package link concrete [architecture, topology, flows, and access designs](architecture-workflows.md), [database design and ERD](database-design.md), and [implementation tasks](implementation-plan.md). These companion artifacts are required parts of the delivery; a list of proposed future diagrams is insufficient. Keep requirements and proposed design choices distinguishable.
