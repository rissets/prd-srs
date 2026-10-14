# Quality, traceability, and readiness

## Evidence registers

Source register: `Source ID | File/URL and locator | Known version/date | Supported facts | Limitations/conflicts`.

Decision register: `Decision ID | Question/assumption | Affected IDs | Impact | Proposed resolution | Actual owner or proposed role | Status`.

Label inferences and cite supporting evidence. Priority is not approval; desired behavior is not proof of implementation. Verify changing provider, legal, or standards claims against authoritative sources or mark unverified. Do not browse simply to decorate documents.

## IDs and traceability

Honor existing conventions or use `GOAL-001`, `PRD-001`, `FR-001`, `NFR-001`, `BR-001`, `AC-001`, and `VER-001`. Identify independently normative data/interface obligations too. IDs have unique definitions across the document set; repeated references are allowed.

For complete packages also use stable `UC`, `WF`, `PERM`, `DIA`, `ADR`, entity/constraint, and `TASK` IDs or the project's equivalent. Extend the matrix with use case/workflow, permission, component/diagram, entity, implementation task, and milestone columns (or separate linked matrices when one table becomes unreadable). Check both directions: every requirement has design/task/verification coverage and every proposed design/task has an in-scope rationale.

| Source/goal | PRD | Software requirement | AC/VER | Method | Coverage |
|---|---|---|---|---|---|
| Source locator or goal ID | ID or N/A with reason | FR/NFR/BR/data/interface ID or N/A with reason | Case ID | Test/inspection/analysis/demonstration | Planned/blocked/verified with evidence |

Use explicit rows or unambiguous lists for many-to-many links. PRD-only work maps sources/goals to PRD and acceptance; an unrequested SRS is not missing coverage. SRS-only work traces directly to sources. Derived requirements cite parent, rationale, and evidence state. Product outcomes may use post-launch measurement rather than software tests.

Check every in-scope requirement, not a sample:

- Valid parent/source or labeled derivation; parents have children or coverage/exclusion rationale.
- Acceptance/verification coverage or a visible gap with readiness impact; every case traces back.
- References resolve; scope, priority, release, terms, states, roles, and thresholds agree.
- Validation, retry, expiration, and recovery conditions specify the required data/time definitions and map to schema/interface fields plus verification cases. A rule such as “expired token is rejected” is incomplete without expiry semantics; do not let generic prose introduce an unmodeled obligation.
- Retired IDs remain in history with downstream impacts; no ID reuse.

Do not claim 100% coverage without accounting for all in-scope IDs. Matrix presence is not coverage; planned coverage is not executed verification.

## Worked translation (synthetic proposals)

All details here are illustrative proposals, not actual product facts.

Weak input: “Admin bisa menyetujui pengajuan dengan aman dan cepat.”

**PRD-001:** Petugas pemeriksa yang berwenang dapat memutuskan pengajuan lengkap agar pemohon memperoleh status keputusan. Source: synthetic note; priority/release: proposed Must/MVP; evidence: proposed; lifecycle: draft.

**FR-001:** Sistem harus mengubah status dari `submitted` ke `approved` ketika pemeriksa berizin pada ruang lingkup pengajuan menyetujui pengajuan yang memenuhi `BR-001`.

**BR-001:** Kelengkapan mengikuti daftar dokumen wajib yang disepakati. Daftar belum tersedia: `DEC-001` memblokir finalisasi aturan. Jangan mengarang dokumen/legal policy.

**FR-002:** Sistem harus menolak persetujuan oleh aktor tanpa izin pada ruang lingkup pengajuan serta mempertahankan status dan data keputusan.

**FR-003:** Sistem harus merekam pemeriksa, waktu keputusan, dan perubahan status pada setiap persetujuan berhasil. Retensi audit merupakan keputusan terbuka.

**AC-001 / VER-001, planned:** Given submitted application satisfying the agreed completeness rule and an authorized reviewer, when approved, then state becomes approved and its decision record identifies reviewer and time. Links: PRD-001, FR-001, FR-003, BR-001. Blocked on DEC-001.

**AC-002 / VER-002, planned:** Given an actor without permission on the application, when approval is attempted, then access is denied and application/decision data remain unchanged. Links: FR-002 and PRD-001.

“Cepat” needs a measurable NFR with operation, load, data size, latency boundary, and threshold. Proposed values remain proposed. Add notification, concurrency, or approval-policy requirements only if actual scope calls for them.

## Quality gates

For each applicable gate record pass/gap/not applicable, evidence/IDs, and remediation:

1. Product fit: evidence, problem, users, outcomes, release, exclusions agree.
2. Atomic clarity: identifiable obligation; explicit terms, subject, units, conditions, boundaries.
3. Workflow completeness: important success, alternate, invalid, denied, failure paths and rules.
4. Data/access: ownership, lifecycle, permissions, interface boundaries sufficient for scope.
5. Verifiability: observable acceptance; measurement conditions; no unsupported guarantees.
6. Consistency/traceability: IDs resolve and cross-document rules, states, scope, coverage agree.
7. Evidence honesty: facts, proposals, assumptions, open decisions, approvals, executed tests distinct.
8. Delivery readiness: blockers identified; requested files, links, tables, format usable.
9. Architecture/topology: actual editable diagrams plus narrative; components, deployment units, interfaces, trust boundaries, and proposed decisions agree with SRS/NFRs.
10. Business/use-case/access completeness: workflows, transitions, use-case diagram/catalog, and permission matrix agree on actors, guards, effects, denied outcomes, and scope.
11. Database completeness: ERD, dictionary, cardinalities, keys/constraints, query/index rationale, lifecycle, and applicable migration design agree with workflows and permissions.
12. Implementation planning: task dependencies, phases, deliverables, acceptance, operational/release work, and requirements coverage are concrete and consistent; estimates and execution states are honest.
13. Interactive resolution: every needed unclear decision was raised with the user; unanswered questions remain pending and dependent artifacts unfinalized. Confirmed answers propagate across documents, diagrams, schema, permissions, and tasks.

For a full package use an artifact checklist covering PRD, SRS, context/component diagrams, topology, business workflow, system flow/sequence, state transitions where applicable, use-case diagram/catalog, role/permission matrix, ERD/dictionary/physical design, dependency plan, implementation tasks, and traceability/registers. Each item must contain project-specific substance or an explicit, justified nonapplicability/blocked decision. A heading, diagram filename, or generic checklist does not count as delivery.

Critical gaps in permissions, state transitions, essential rules, or acceptance prevent an implementation-ready claim. Deliver the useful draft and exact decisions needed. Avoid padding to achieve a score or silently omitting gaps.

## Guidance sources

Requirement clarity/verifiability checks draw on [NASA's checklist](https://www.nasa.gov/reference/appendix-c-how-to-write-a-good-requirement/); source-to-requirement linkage draws on [NASA requirements management](https://www.nasa.gov/reference/6-2-requirements-management/), consulted 2026-10-14. These support engineering judgment; NASA-specific processes are not user obligations. This skill's PRD/SRS structures are editorial guides, not certified compliance templates.
