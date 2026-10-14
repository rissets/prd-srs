# Traceability and registers
0.1 MVP/draft. Every row coverage **planned**; no runtime verified claims. Source SRC-001 locators S1–S8 are in SOURCES.md. GOAL-001 maps PRD-001/002/003; GOAL-002 maps PRD-004–008; GOAL-003 maps PRD-009. All PRD records have children and cases; all 18 independently normative SRS IDs included below. Slash notation abbreviates same prefix (e.g. VER-005/008 means VER-005 and VER-008); ranges inclusive. AC IDs mirror VER numbers. WF-001 covers the loan lifecycle, UC-001/003/004 cover read paths.

| SRS ID | Product | SRC-001 locator | Use case | Permission | Design | Data/constraint | Task | Milestone | Planned case |
|---|---|---|---|---|---|---|---|---|---|
| FR-001 | PRD-001 | S2 | UC-001 | PERM-001/009 | DIA-001/002/008/009 | ENT-002 | TASK-002 | M1 | VER-001 |
| FR-002 | PRD-002 | S2 | UC-002 | PERM-002 | DIA-004/006/008 | ENT-001/002/003 | TASK-003 | M2 | VER-002 |
| FR-003 | PRD-003 | S2 | UC-003 | PERM-003/007 | DIA-002/008/009 | ENT-001/003 | TASK-003 | M2 | VER-003 |
| FR-004 | PRD-004 | S2 | UC-004 | PERM-004/007 | DIA-002/009 | ENT-003 | TASK-004 | M2 | VER-004 |
| FR-005 | PRD-005 | S2/S3 | UC-005 | PERM-005/007 | DIA-004/005/006 | ENT-001/002/003 | TASK-004 | M2 | VER-005/008 |
| FR-006 | PRD-005 | S2/S3 | UC-006 | PERM-005/007 | DIA-004/005/007 | ENT-001/003 | TASK-004 | M2 | VER-006 |
| FR-007 | PRD-006 | S2/S3 | UC-007 | PERM-006/007 | DIA-004/005/007 | ENT-003 | TASK-004 | M2 | VER-007 |
| BR-001 | PRD-005/006 | S3 | UC-005/006/007 | PERM-005/006 | DIA-005/006/007 | ENT-003; CON-003 | TASK-004 | M2 | VER-005/006/007/008 |
| BR-002 | PRD-007 | S3 | UC-005 | PERM-005 | DIA-006; ADR-002 | ENT-002/003; CON-002 | TASK-004 | M2 | VER-008 |
| BR-003 | PRD-008 | S4 | UC-005/006/007 | PERM-005/006 | DIA-008 | ENT-003; CON-005 | TASK-002/004 | M1/M2 | VER-009 |
| DATA-001 | PRD-001 | S4 | UC-001/002 | PERM-001/002 | DIA-008 | ENT-002; CON-001 | TASK-002 | M1 | VER-013 |
| DATA-002 | PRD-002/008 | S4 | UC-002/005/006/007 | PERM-002/005/006 | DIA-008 | ENT-003; CON-003/004 | TASK-002/004 | M1/M2 | VER-009/013 |
| DATA-003 | PRD-008 | S4 | UC-002/005/006 | PERM-002/005 | DIA-008 | ENT-001/003 | TASK-002/004 | M1/M2 | VER-009/010 |
| IF-001 | PRD-009 | S1 | UC-001–007 | PERM-008 | DIA-001/002 | ENT-001 | TASK-001 | M1 | VER-010 |
| NFR-001 | PRD-009 | S7 | UC-001 | PERM-001 | DIA-003 | ENT-002; IDX-004 | TASK-005 | M3 | VER-011 |
| NFR-002 | PRD-009 | S7 | UC-001–007 recovery | all permissions restored | DIA-003; ADR-003 | ENT-001–003 | TASK-006 | M3 | VER-012 |
| NFR-003 | PRD-009 | S6 | UC-001–007 | PERM-008 | DIA-002/003; ADR-001 | ENT-001–003 | TASK-001/005 | M1/M3 | VER-010 |
| NFR-004 | PRD-009 derived proposal | S2 derived usability | UC-001–007 | all applicable | DIA-002 | N/A nonpersistent UI | TASK-005 | M3 | VER-013 |

Reverse coverage: TASK-001–007 serve rows above; TASK-007 acceptance encompasses all PRD/FR/NFR; DIA-010 serves task dependencies. DIA-001–009 have in-scope IDs in ARCHITECTURE.md. ENT-001–003 and CON-001–006 support DATA/BR/FR; IDX-001→FR-003, IDX-002/003→FR-004, IDX-004→FR-001. ADR-004→FR-002/CON-006/VER-002. PERM-001–009 serve FR/IF cases in access matrix. Each VER-001–013 has explicit parent obligations in VERIFICATION.md. AC record definitions live there; definitions of SRS IDs live SRS.md, PRD IDs in PRD.md, diagram IDs in ARCHITECTURE.md, entity/constraint IDs in DATABASE-DESIGN.md, task IDs in IMPLEMENTATION-PLAN.md, UC/WF/PERM in WORKFLOWS-AND-ACCESS.md. Repeated mentions are links, not new definitions.

## Decision/source register and readiness
No competing sources, retired requirements or approval evidence. ADR-001–004 are proposed/draft delegated technical designs. Questions/prerequisites tracked QUESTIONS.md; no dependent business sections stopped. Adapter integration still requires actual contract evidence, catalog source not fabricated, operational storage not selected. Reviewer actual UAT role supplied SRC-001 S8; document approver not supplied.

Readiness **ready for stakeholder review**, not approved. All desired software tests planned; document writing completion differs from deployed-system acceptance. Baseline changes preserve IDs, record source/rationale and re-review affected diagrams, data, tasks and tests; approved history remains history if supplied later.

DIA-011 UML actor/boundary use-case source covers UC-001–007/PERM-001–009; DIA-009 supplemental map agrees, including librarian proposed catalog grant.
