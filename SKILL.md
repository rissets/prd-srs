---
name: prd-srs
description: Create, improve, or review detailed PRD and SRS packages with architecture and topology diagrams, business and system flows, use cases, role permissions, ERD, database design, and implementation plans. Clarify unresolved decisions interactively and trace requirements through design and planned verification. Use for requirements and solution planning, not executing implementation.
metadata:
  version: "0.1.0"
---

# PRD & SRS

Produce a detailed requirements and solution-planning package that product stakeholders can evaluate and engineering/QA can implement and verify. Follow the user's language; use Indonesian for Indonesian requests. PRD describes problems, users, outcomes, and product scope. SRS specifies observable system behavior, rules, data, interfaces, and quality constraints. Companion designs explain how the proposed solution satisfies them without disguising proposals as approved constraints. A feature-name inventory, list of headings, or technology shopping list is insufficient.

## Establish the document contract

- For a new complete package, deliver PRD, SRS, architecture/topology, workflow/use cases/permissions, database design/ERD, and implementation plan. Honor explicit narrower requests (for example review one PRD section); do not regenerate unrelated artifacts. SRS without a PRD traces to stakeholder/system needs rather than an invented approved PRD.
- Read supplied sources, relevant repository instructions, and existing document structure. Honor mandated templates; use the references as coverage guides. In a codebase, distinguish observed behavior from proposed future behavior.
- Identify audience, product boundary, release, source versions, constraints, format, and destination. Use the interactive clarification protocol below whenever a needed decision is unclear; continue only work independent of the answer.
- If the user has not answered, preserve a useful draft and pending questions. Do not finalize the dependent design using an unconfirmed assumption. Never invent research, baselines, budgets, dates, legal obligations, provider capabilities, or approval.
- Default to Markdown at the requested destination, established docs location, or `docs/requirements/` in the active workspace. For requested DOCX/PDF, use available document tooling and verify rendering; if unavailable, preserve the source and report the limitation. Do not silently substitute a cloud document.

## Load relevant guidance

| Work | Reference |
|---|---|
| PRD or product half of a paired request | [PRD structure](references/prd.md) |
| SRS or specification half of a paired request | [SRS structure](references/srs.md) |
| Architecture, deployment topology, business/system flows, use cases, permissions | [Architecture and workflows](references/architecture-workflows.md) |
| ERD and detailed logical/physical database design | [Database design](references/database-design.md) |
| Delivery planning, implementation phases, work breakdown and acceptance | [Implementation plan](references/implementation-plan.md) |
| Every creation, update, or review | [Quality and traceability](references/quality.md) |

Adapt depth to the product and release. Complete means relevant decisions and acceptance paths are covered, not every conceivable feature is included. Explain irrelevant areas briefly or omit them when the template permits. Do not present empty headings as complete content.

## Interactive clarification protocol

Ask the user whenever missing, ambiguous, or conflicting information prevents a concrete requirement or design decision. In particular clarify product boundaries, actors and approval authority, business states, tenant/data ownership, integrations, deployment constraints, schema-critical rules, release priorities, and acceptance targets. Read supplied evidence first; do not ask questions already answered there.

1. Identify the exact gap, affected artifacts/IDs, and why the answer matters.
2. Ask in small rounds (normally one to three individual decisions), using the available user-input tool or a direct question if no tool is available. Start with the highest-impact blockers and defer lower-priority questions to later rounds. Do not disguise a long questionnaire as three numbered groups containing many separate questions. Offer a recommendation and meaningful options where useful; do not bury questions in a long draft.
3. Await answers for dependent work. Elapsed time or no reply is not agreement. Continue independent sections and keep the affected sections explicitly pending.
4. Record answers and their source, update all affected documents/diagrams, and ask a follow-up when the answer still leaves a needed decision unclear. Avoid repeated resolved questions.
5. Routine editorial choices can be made directly. If the user explicitly delegates design decisions, choose within that delegated scope and document rationale; delegation never makes an invented business fact true.

Before calling the package complete, show unresolved decisions and ask the user to resolve any remaining necessary ambiguity. If the user requests a draft despite open decisions, deliver it with its blocked scope identified; do not claim implementation readiness.

Record a clear user adoption/approval decision as evidence for that decision and version when the user actually gives it; do not require an invented signing ceremony. Distinguish approval of a proposal from approval of the entire package, and resolve contradictory status instructions explicitly.

## Build requirements

1. Register sources with stable IDs and locators. Resolve conflicting versions when evidence permits; otherwise record the conflict and affected requirements for decision.
2. Define actors, goals, boundaries, and journeys before features. Cover important failure/denial behavior and separate excluded or later-release work.
3. Assign stable IDs, source/rationale, priority, release, and status. Separate evidence state (`confirmed`, `proposed`, `assumed`, `open`) from lifecycle (`draft`, `reviewed`, `approved`). Preserve IDs on revision; retire removed IDs without reuse.
4. Write atomic, observable requirements with acceptance criteria. Specify actors, inputs, preconditions, validation, state changes, outputs, and failure behavior where applicable. See the quality reference's worked translation.
5. Specify quality targets with metric, threshold, operating conditions, and verification method. Unsupported targets remain proposals. Keep implementation choices optional unless constrained by sources or established project decisions.
6. Link product requirements to SRS and planned acceptance/verification cases. Paired documents share one glossary, release boundary, role model, and ID convention.
7. Build linked design artifacts: context and component architecture, deployment/network topology, business workflow, system flows/sequences, use-case diagram/catalog, permission matrix, ERD/data dictionary, and implementation plan. Read all three companion references for a complete package. Each diagram needs actual nodes/relationships and explanatory text, not merely a promised diagram heading.
8. Apply quality gates to the whole package; fix contradictions and dangling references. Resolve necessary uncertainty interactively and keep unresolved decisions visible.

## Deliver and maintain

Deliver requested documents with source, traceability, and open-decision registers inside them or as shared companion files when useful. For reviews, give prioritized findings with section/requirement IDs, impact, and corrections; edit only when requested.

Default complete-package layout (adapt to existing project conventions): `PRD.md`, `SRS.md`, `ARCHITECTURE.md`, `WORKFLOWS-AND-ACCESS.md`, `DATABASE-DESIGN.md`, `IMPLEMENTATION-PLAN.md`, and a shared `TRACEABILITY.md` under the chosen requirements directory. Embed editable diagram source alongside its explanation; provide rendered diagrams when the requested format or renderer permits. Shared registers can live in TRACEABILITY.md. Small packages may combine files, but retain all required coverage. Deliver a linked artifact inventory and check every internal file/section/requirement reference.

Report readiness separately from writing completion: `draft — unresolved decisions`, `ready for stakeholder review`, or `approved — evidence linked`. A complete draft can remain unready for implementation. State verification and critical open decisions; reviewing requirements does not execute software tests.

For baseline updates, record version/date, changed/retired IDs, rationale, and downstream impacts. Preserve approvals as history; changed approved requirements need re-review. Requirements drafting does not authorize implementation, publication, external tickets, or messages.
