# Planning and implementation plan

Produce an executable work breakdown grounded in requirements and design. This is planning, not authorization to implement or deploy. Do not replace tasks with generic phases such as “build backend” without deliverables and acceptance. Separate product/release planning from engineering execution details.

## 1. Planning basis

State target release, scope, requirement baseline, design status, team/capacity if supplied, dependencies, constraints, and critical open decisions. Ask about release priorities, mandated dates, staffing, or capacity when a schedule depends on them. Unknown estimates remain unknown; relative sizing or time ranges are explicitly proposed with assumptions.

## 2. Delivery strategy

Sequence coherent vertical slices that deliver complete user outcomes: data/rules, authorization, API/UI, errors, tests, and operational needs together. Begin with enabling dependencies only as needed; avoid postponing every integration and permission check to the last phase. Identify parallelizable tasks and true blockers.

Provide phases/milestones with outcomes, included requirement IDs, tangible artifacts, entry/exit criteria, dependencies, proposed responsible role, and risk. Separate MVP from later releases. Include discovery/decision work for unresolved dependencies rather than scheduling uncertain implementation as settled.

## 3. Work breakdown

Each `TASK-001` includes:

| Field | Detail |
|---|---|
| Outcome | Concrete user/system result |
| Scope/links | PRD/FR/NFR/BR, UC, diagram/component, entity IDs |
| Work | Implementable steps and affected modules/contracts |
| Dependencies | Predecessor task IDs, decisions, provider/data prerequisites |
| Deliverables | Code/schema/UI/API/config/docs as applicable |
| Acceptance | Observable completion criteria, VER IDs, evidence needed |
| Responsibility | Known owner or labeled proposed role |
| Size/schedule | Supplied estimate or proposed range with assumptions |
| Risks/recovery | Likely failure, response, reversibility constraints |
| Status | Planned/blocked/etc.; never imply execution |

Include functional development, schema/migrations, role enforcement, interfaces, quality targets, and evidence tasks. Relevant environment/CI/secrets setup, accessibility, monitoring, performance, security, data migration, release/rollback, and documentation belong in the plan when required by scope, not as automatic unrelated projects.

## 4. Dependency and milestone views

Include an editable task dependency diagram with real task IDs and blocker edges. Show milestone/release grouping and a critical path only if dependency/duration evidence supports it. A relative sequence is preferable to invented calendar dates. Use a Gantt chart when dates/durations are supplied or explicitly delegated; label proposed schedules and assumptions.

## 5. Verification and release plan

Map planned unit/integration/contract/E2E, authorization, failure-path, migration, performance, and accessibility checks to applicable requirements and risks. Define test data (synthetic versus operational), environment/provider needs, pass criteria, and evidence to collect. Name live-path checks needed beyond build/health checks.

Define stakeholder/UAT acceptance, release checklist, rollout stages, migration validation, monitoring signals, abort criteria, recovery approach, and handover. Approval owner/authority must be supplied or remain pending. Do not mark future tests/UAT/deployment as completed.

## 6. Cross-package completeness

Every in-scope release requirement has implementing/enabling tasks and planned verification, or a documented gap. Every task serves an in-scope requirement or justified dependency. No task silently expands product scope. Milestone acceptance agrees with PRD success/launch criteria and SRS quality targets. Re-plan affected tasks when a decision or requirement changes.
