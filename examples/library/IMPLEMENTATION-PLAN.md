# Rencana implementasi
0.1 MVP/draft. Semua tasks **planned**. Tidak ada tanggal release, staffing estimate, durasi, ukuran relatif atau critical path berbasis durasi yang dibuat. Ini perencanaan, bukan authorization menjalankan code/deploy. Diagram dependensi DIA-010 tersedia; urutan relatif M1→M2→M3→M4. Backup setup dapat paralel setelah TASK-001 tetapi drill final menunggu slice lengkap. Semua responsibilities proposed kecuali UAT representative dari source.

Milestones: M1 data/identity/catalog siap diverifikasi (entry source baseline, exit VER-001/010 dan migration checks); M2 semua journey serta concurrency (entry M1, exit VER-002–009); M3 quality dan recovery evidence (entry M2 untuk drill final, exit VER-010–013); M4 stakeholder acceptance (entry semua planned checks executed/pass, exit UAT dan keputusan release dicatat). Tidak ada perluasan later-release backlog.

## TASK-001: M1 — binding dan environment
Status: planned; links IF-001; NFR-003; design UC-001–007; DIA-001/002/003; ENT-001. Dependencies: none; inspect actual adapter contract and obtain catalog source outside portal.
Work: Document trusted principal binding; set staging/private PG16/TLS ingress; record secret handling and schema migration scaffolding.
Deliverables: binding contract/config/migration plan.
Acceptance: VER-010; valid trusted principal, deny spoof, private network verified; evidence recorded in VER case artifacts, not presumed.
Responsibility: engineer/operations proposed. Schedule: relative only, no estimate supplied/requested.
Risk/recovery: adapter mismatch; pause binding code until actual contract, preserve independent database work.


## TASK-002: M1 — katalog dan persistent model
Status: planned; links FR-001; DATA-001/002/003; BR-003; design UC-001; DIA-008; ENT-001–003. Dependencies: TASK-001.
Work: Create schema constraints/indexes, validate catalog onboarding; SSR list/detail and empty/error states; migrations verify fixtures before real input.
Deliverables: schema migrations/catalog views/templates.
Acceptance: VER-001/009/013; dictionaries and constraints realized; evidence recorded in VER case artifacts, not presumed.
Responsibility: engineer proposed. Schedule: relative only, no estimate supplied/requested.
Risk/recovery: bad ISBN data; reject invalid onboarding batch before commit.


## TASK-003: M2 — anggota submit dan pinjaman sendiri
Status: planned; links FR-002/003; IF-001; design UC-002/003; DIA-006; ENT-003. Dependencies: TASK-002.
Work: Scoped reads; owner from principal; token dedupe; submit form and feedback; denial/failure tests.
Deliverables: own-loan vertical slice and tests.
Acceptance: VER-002/003; no spoof/leak; repeat token one loan; evidence recorded in VER case artifacts, not presumed.
Responsibility: engineer/QA proposed. Schedule: relative only, no estimate supplied/requested.
Risk/recovery: scope leak; block release and fix server scopes.


## TASK-004: M2 — review keputusan dan pengembalian
Status: planned; links FR-004–007; BR-001/002/003; design UC-004–007; DIA-004–007; ENT-003; ADR-002. Dependencies: TASK-003.
Work: Librarian global reads; locked transitions; audit; race tests and browser approve/reject/return UI.
Deliverables: librarian vertical slice and concurrency tests.
Acceptance: VER-004–009; invariant preserved in PostgreSQL16; evidence recorded in VER case artifacts, not presumed.
Responsibility: engineer/QA proposed. Schedule: relative only, no estimate supplied/requested.
Risk/recovery: race/deadlock; rollback failed tx, tune lock order then rerun race.


## TASK-005: M3 — performance dan UX/access evidence
Status: planned; links NFR-001/004; NFR-003; design UC-001–007; DIA-002/003; IDX-001–004. Dependencies: TASK-004.
Work: Instrument server boundary; load test 10k/20/5min; record errors/query plan; keyboard and denied paths; tune only measured need.
Deliverables: raw latency report/access/UX evidence.
Acceptance: VER-010/011/013 thresholds meet; evidence recorded in VER case artifacts, not presumed.
Responsibility: QA/engineer proposed. Schedule: relative only, no estimate supplied/requested.
Risk/recovery: test masking errors; keep raw samples and fix before rerun.


## TASK-006: M3 — operational backup dan recovery
Status: planned; links NFR-002; design DIA-003; ADR-003; ENT-001–003. Dependencies: TASK-001; restore checks need TASK-004 for full live path.
Work: Daily dump/encryption/off-VM upload; failure/stale alert; secret/config recovery; replacement VM drill including provisioning; retain7 proposed.
Deliverables: backup config/runbook, restore timeline and manifest.
Acceptance: VER-012 actual RPO/RTO pass; no secret leakage; evidence recorded in VER case artifacts, not presumed.
Responsibility: operations/QA proposed. Schedule: relative only, no estimate supplied/requested.
Risk/recovery: dump missing/late; retry and alert, readiness blocked while RPO unmet.


## TASK-007: M4 — stakeholder UAT dan release readiness
Status: planned; links PRD-001–009; FR-001–007; NFR-001–004; design UC-001–007; all diagrams; all entities. Dependencies: TASK-005/TASK-006; stakeholder review of proposals.
Work: Run UAT with librarian representative; report planned cases results; review schema/config/backup; rehearse rollout on staging; prepare handover.
Deliverables: UAT record, release checklist/rollback runbook, approval evidence if later supplied.
Acceptance: VER-001–013 all pass; UAT signoff explicitly recorded; document approval authority still to be supplied; evidence recorded in VER case artifacts, not presumed.
Responsibility: librarian representative + engineering/operations proposed. Schedule: relative only, no estimate supplied/requested.
Risk/recovery: rejection or unsafe migration; no release; rollback app only if schema compatible, otherwise restore drill strategy.


## Proposed release/rollback/handover
Review source and proposals; stage migrations on synthetic and approved onboarding source; confirm backups/recovery and private binds; execute browser role-specific live paths; capture UAT. Production deployment remains later authorization. Rollout proposal: backup before migration, run constraint/count checks, enable traffic, verify member submit + librarian decision/return and server errors. Abort on scope leak, invariant violation, failed migrations/recovery checks or catalog p95 beyond target under defined test. App rollback only with compatible schema; irreversible data changes require restored backup and documented RPO consequence. No destructive migration presumed reversible.

Handover includes identity boundary contract, runbooks, actual operational owner to be assigned, UAT evidence and known limits. Approval authority unknown does not imply approval. No production release or software check executed in this package.
