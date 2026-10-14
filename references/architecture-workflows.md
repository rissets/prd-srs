# Architecture, topology, workflows, use cases, and access

For a full package all artifact families below are required. Scale each to the actual system; a small monolith still needs an honest context, components, topology, and flows. Do not introduce microservices, queues, clusters, or extra actors just to fill diagrams. Separate current, proposed, and approved views.

## Diagram delivery contract

Give each diagram a stable `DIA-001` ID, title, scope/release, status, legend, linked requirement/use-case IDs, editable source, and explanatory narrative. Explain responsibilities, connections, decisions, failure behavior, and relevant open questions. Use consistent actor/component/entity names across all artifacts.

Use Mermaid for context/component/topology flowcharts, sequence, state, and ER diagrams. Deliver the requested use-case diagram as editable UML source (for example PlantUML) with actors, system boundary, use cases, associations, and justified include/extend/generalization; an unavailable renderer does not prevent delivering the source. A Mermaid relationship map can supplement it as a preview or replace it only if the user chooses that alternative. Label a map honestly; do not invent a Mermaid `usecaseDiagram` syntax or claim a flowchart is UML.

Render and inspect diagrams using available tooling when possible. Check compatible installed runtimes/libraries as well as CLI availability before declaring a renderer unavailable. Check syntax with a compatible parser/renderer and verify legibility, edge directions, labels, and boundaries. If rendering is unavailable, supply source and disclose that rendering/syntax remain unverified; do not claim a rendered artifact exists. Keep diagram sources adjacent to narratives; separate `.mmd`/`.puml` files when useful for editing/export.

Inspect the exported artifact, not only a browser preview: the full diagram canvas must be included without clipped nodes/edges, and text must remain readable at its intended document size. Split oversized views into linked subviews rather than shrinking labels beyond readability. Report validation separately by diagram format; Mermaid validation does not validate PlantUML.

Run parser/render verification on every source when tooling is available, including companion files and embedded copies. A sequence message containing SQL-like semicolons can be split into invalid Mermaid statements: use separate messages/notes or compatible escaping and verify it, rather than pasting `BEGIN; lock; update; COMMIT` into one message. If source appears both embedded and in a file, keep the copies synchronized or embed only a link to the canonical source.

## 1. Architecture diagrams and design narrative

Provide distinct views rather than one diagram attempting to answer everything:

- **System context:** users, system boundary, external systems, direction/purpose of exchanged information, and ownership/trust boundaries.
- **Logical/component architecture:** UI clients, application modules/services, domain responsibilities, persistent stores, and actual integration adapters. Show contracts/protocols when known; mark unknowns. Detail key internal components only where needed to explain behavior or risky boundaries.
- **Runtime interactions:** sequences for every critical cross-component journey, including who authorizes, validates, writes, dispatches work, and reports results. Include failure/timeout paths where correctness depends on them.

Document each component's purpose, owning responsibility, linked FR/NFR, inputs/outputs, data owned, synchronous/asynchronous dependencies, and failure consequences. Describe authorization, transactions, audit, caching, retries/idempotency, and observability where relevant.

For substantive proposed decisions record `ADR-001`: context, constraints, considered alternatives, recommendation, rationale, tradeoffs, status, affected requirements, and question for user if unresolved. Do not use speculative scale to justify complexity. Ask before locking an unclear stack or deployment constraint.

## 2. Deployment and network topology

Show clients, public entrypoint/DNS, ingress or reverse proxy, runtime units, stores, workers/queues if needed, external providers, and network/trust boundaries. Distinguish logical modules from separately deployed units. Show traffic direction, protocols and known ports, TLS termination, public/private exposure, secret handling boundary, and relevant outbound dependencies. Do not invent real hostnames/IPs or print secrets.

Include a topology table: `Node | Environment | Purpose | Exposure | Dependencies | Protocol/port | Persistent data | Requirement/decision`. Cover development/staging/production differences needed for acceptance; avoid three duplicate diagrams when a difference table suffices.

Tie capacity, redundancy, recovery, backups, monitoring, and deployment/rollback behavior to NFRs. Unagreed sizing, availability, regions, or infrastructure providers need clarification. Label proposed counts/resources as proposed, not measured or guaranteed.

## 3. Business workflow

Model the business process across human and system responsibilities, preferably using swimlane-style subgraphs and labeled decision branches. Include start/end, trigger, participants, handoffs, business rules, approvals, rework/rejection/cancellation, escalation/time conditions if defined, and external/manual steps. A screen navigation diagram alone is insufficient.

Use `WF-001` records: objective, actors, trigger/preconditions, input/output, normal path, alternatives, exceptions, rule IDs, use-case/FR links, and acceptance cases. State diagrams capture meaningful record lifecycle. Define a transition table: `From | Event | Actor/scope | Guard/rule | To | Persisted effects | Failure outcome`. Resolve unclear authority or transitions with the user.

In swimlane views assign each activity to its actual performer: human review/approval actions to their role, server guards, persistence, and state updates to the system. Declare nodes within their intended lane before cross-lane edges so diagram syntax does not accidentally place a system action under a human role.

## 4. System flow and sequence

For each critical workflow show the technical path: user event, validation, authorization, domain action, data write/read, provider/async interaction, and visible result. Explain request versus background work, commit boundary, retry/duplicate behavior, and recovery where relevant. Match API names, state names, and component names to SRS; proposed endpoints stay proposed.

Business workflow and system flow can share a diagram only if both responsibilities and execution boundaries remain explicit. Use sequence diagrams for ordering across participants and state diagrams for lifecycle; neither replaces an unexplained business workflow.

Match sequence call/return paths to component contracts. For a synchronous view→service→database call, show the result returning through the service; do not imply database→view callbacks bypassing the service unless an actual callback/event contract explains them. Compact views can omit intermediate acknowledgments, but must preserve ownership and ordering semantics.

## 5. Use-case diagram and catalog

Provide a diagram covering in-scope actors and use cases, plus `UC-001` records:

| Field | Required detail |
|---|---|
| Name/goal | Business outcome and linked PRD/FR |
| Actors | Primary and supporting actors; access scope |
| Trigger/preconditions | Required state, identity, data |
| Main scenario | Numbered actor/system exchanges |
| Alternate/exception scenarios | Branch point, condition, response/recovery |
| Postconditions | Success state and failure invariants |
| Rules/data | BR IDs, entities, interface dependencies |
| Verification | AC/VER IDs; current evidence status |

Use include for shared required behavior and extend for conditional additions only when those relationships fit; do not force every use case into these constructs. Do not make CRUD actions the only use cases when real business goals involve several steps.

Write the numbered scenarios with actual domain actions, relevant inputs, validation/guards, and concrete results. Avoid repeating generic steps such as “open relevant page” for every case. Alternate/exception paths identify the originating main-step number and resulting state or unchanged-data invariant.

## 6. Role and permission design

Inventory roles with purpose, assignment/revocation authority, allowed scope, and role-combination restrictions when defined. Distinguish role permission from ownership, tenant, object state, or other contextual conditions.

Matrix: `PERM ID | Role | Resource/action | Own/team/tenant/global scope | Allowed/denied/conditional | Conditions | Enforcement surface | Audit | FR/UC/VER`.

Cover read/list/detail, create/update/delete, submit/approve/reject, export/import, sensitive fields, configuration, role assignment, and background/admin actions only where the product exposes them. Show denied outcomes and backend enforcement points. Clarify ambiguous approval authority, segregation of duties, cross-tenant/global access, and support/operator privileges rather than guessing. Do not default every actor named Admin to unrestricted access.

Check permissions against workflow guards, use-case preconditions, database ownership keys, and denied-path verification. Hidden buttons do not establish authorization. Proposed policy remains pending until the user resolves needed ambiguities.

Reconcile every allowed/conditional role–use-case pair in the permission matrix against actor associations in the use-case diagram/catalog, including proposed grants. Explain intentional exclusions; do not omit a granted action from one view. Traverse business/system diagrams against the transition table: a human-approved state change must be reachable only through the authorized actor action and guard, with no bypass edge implying automatic approval. Syntax-valid diagrams can still contradict business policy.
