# Database design and ERD

Deliver an actual model, not an entity-name list. Use existing schema and naming conventions when supplied. Distinguish logical model, proposed physical design, and verified current schema. Ask about unclear ownership, cardinality, uniqueness, lifecycle, history/retention, or storage-engine constraints before finalizing dependent choices.

## 1. Domain model and ERD

Identify entities from workflows/rules, their responsibilities and sources of truth. Provide an editable Mermaid ERD or compatible ER notation with entity names, key attributes, primary/foreign keys, cardinality, optionality, and join entities. Every relationship has a business explanation. Distinguish external provider references from locally owned entities.

ERD scope must cover persistence for all in-scope use cases, including ownership, approval/history, attachments, and audit when required. Do not model nonpersistent UI state as a table without reason. A many-to-many relationship requiring attributes needs an explicit association entity.

## 2. Data dictionary

For every table/entity document purpose, related requirement/use-case IDs, lifecycle, source, access scope, and fields:

`Field | Logical/physical type | Size/precision/unit | Nullable | Default/generated behavior | PK/FK/reference | Unique/check constraint | Meaning/validation | Sensitivity`.

Specify IDs, business keys, enum/state definitions, timestamps/time-zone behavior, decimal precision for monetary quantities when relevant, and optional values deliberately. JSON fields require defined structure/validation and reasons; avoid unstructured storage replacing needed relationships.

## 3. Physical design

If an engine is agreed, provide engine-appropriate table/column types, constraints, foreign-key delete/update behavior, and index plan. If not, provide logical design and ask the user before presenting engine-specific design as settled. DDL is useful when requested or needed to make the specification precise; mark illustrative/proposed DDL and do not execute it as part of documentation.

For constraints state which invariant they enforce and whether enforcement is database, application, or both. Cover uniqueness scope (global versus tenant/owner), null semantics, referential integrity, soft/hard deletion, and prevention of invalid state/data. Explain normalization and justified denormalization with synchronization behavior.

Index table: `Index | Columns/order/predicate | Query/use case | Expected benefit | Write/storage cost | Evidence/proposal`. Derive indexes from real access patterns; do not add an index to every field or invent performance results.

## 4. Transactions, concurrency, and ownership

For stateful writes specify atomic boundary, conflicting actions, expected consistency, duplicate/idempotency behavior, and concurrency policy when needed. Connect them to workflow transition rules. Describe tenant/owner isolation, shared records, sensitive fields, and audit history. Proposed constraints must support the permission matrix and cannot rely on client-supplied privileged ownership alone.

## 5. Lifecycle and operations

Define creation/update/deletion/archival, retention requirements and source, backup/restore implications, imports/exports, and reconciliation with external data. Distinguish business history from diagnostic logs. Clarify retention/legal deletion conflicts rather than inventing durations.

For existing systems add migration mapping, transformation/backfill, data-quality checks, ordering, compatibility window, acceptance/reconciliation, and recovery approach. Explain destructive/irreversible migrations and possible restore/forward-fix strategy; do not claim every migration can safely roll back.

## 6. Design verification

- ERD and dictionary agree on every entity, key, reference, cardinality, and optionality.
- Workflow states/rules map to supported fields and constraints.
- Permission scopes map to ownership relationships and enforceable queries/rules.
- All required reads/writes and historical records have a persistence design or explicit nonpersistent rationale.
- Query/index assumptions, migration risks, privacy/retention questions, and unverified engine semantics remain visible.
- Link entities/constraints to FR/BR and planned verification; writing an ERD is not proof the schema runs.
