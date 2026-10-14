# PRD coverage guide

Use when no template is supplied. Merge sections for a small product; expand workflows for larger releases. Replace instructional content with facts, labeled proposals, or open decisions.

## 1. Document control and evidence

Title, product, version/date, release, lifecycle/evidence status, author and reviewers if known, sources, and change history. Record approval only with evidence.

## 2. Problem and context

Who experiences the problem, current workflow, friction, consequences, and supporting evidence. Separate observations from hypotheses. Explain why this release matters. Describe existing alternatives only from available evidence.

## 3. Goals and success measures

Define outcomes rather than feature counts. Each metric has definition/formula, baseline or unknown, target, measurement window, measurement source/instrumentation, and guardrail. Label proposed targets. Separate launch acceptance from post-launch outcomes.

## 4. Actors and stakeholders

Primary/secondary users, needs, constraints, access scope, and stakeholder decisions. Prefer grounded role descriptions to invented demographic personas. Identify who may view, create, change, approve, and export information.

## 5. Scope and release boundary

In-scope capabilities, exclusions, dependencies, and deferred work. Define priority meanings and tie requirements to releases. Must means required for the specified release, not automatically approved.

## 6. Journeys and product behavior

For critical journeys: actor, trigger, preconditions, steps, successful result, alternatives, failures, denied actions, and recovery. Include relevant empty/loading/error states, notifications, and accessibility needs. Link supplied designs; label proposed designs.

## 7. Product requirements

One record per independently verifiable outcome:

| Field | Content |
|---|---|
| ID | Stable `PRD-001` |
| Requirement | Actor need and observable product outcome |
| Rationale/source | Problem or goal served; source ID and locator |
| Priority/release | Inclusion and importance |
| Acceptance criteria | Scenario IDs, conditions, action, expected result |
| Dependencies | Requirements or external preconditions |
| Status | Evidence state and lifecycle separately |

Group by capability. Include business rules/product constraints; link software details to SRS if requested. Avoid one requirement combining several independent capabilities or needless IDs for every UI label.

## 8. Data and integrations

Data needs, sources/ownership, freshness, quality assumptions, sensitivity, third parties, and limitations. Identify synthetic/demo data explicitly. Define product behavior when data or dependencies are unavailable; SRS contains technical contracts.

## 9. Quality expectations and constraints

Relevant usability/accessibility, reliability, performance, security/privacy, operational, budget, policy, and platform constraints. Cite mandated rules and avoid unsupported compliance claims. Product-level quality expectations link to detailed SRS targets when available.

## 10. Delivery, risks, and decisions

Release slices, dependencies, rollout/migration, readiness criteria, and post-launch measurement. Do not invent estimates or promised dates. Risks include impact and response; open decisions include affected IDs. Identify acceptance needs and actual reviewer or labeled proposed role.

## 11. Traceability and glossary

Connect sources/goals to PRD, acceptance criteria, and SRS when requested. Define domain terms consistently. Use the quality reference for traceability and readiness checks.

For a full package link the [business workflows, use cases, and permissions](architecture-workflows.md) and [release/implementation plan](implementation-plan.md). Keep business outcomes in PRD while the companion documents hold detailed diagrams and task records; cross-reference them instead of duplicating conflicting descriptions.
