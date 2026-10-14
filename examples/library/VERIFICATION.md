# Planned acceptance and verification
0.1 MVP draft. Every AC below paired to same-number VER. All records **planned, not executed**. Fixtures synthetic; no user contacted. Evidence to collect per case: reproducible setup, versions/config, action log, assertion/output, screenshots for UI, timestamped result and reviewer; database invariant proof for writes. No software evidence exists yet. UAT by perwakilan pustakawan uses complete UC-001–007, denied paths, concurrency result and recovery/performance summary.

## AC-001 / VER-001
Links: FR-001; PRD-001. Method: browser E2E/integration. Environment: staging synthetic. Status: planned.
- Setup: Seed 10k books including optional ISBN; member and librarian identities.
- Action: Open paginated catalog and valid/unknown book detail; empty fixture variant.
- Expected: Title wajib shown, ISBN shown bila tersedia dan tidak fabricated bila null, correct stable pages, empty feedback, 404 unknown; only authorized principals.
- Evidence: case result and artifacts above; specific raw server latency samples for VER-011, transaction logs/count queries for VER-008, backup manifest and restore timeline for VER-012.


## AC-002 / VER-002
Links: FR-002; PRD-002; CON-006. Method: integration/E2E. Environment: staging synthetic. Status: planned.
- Setup: Member A/B, valid/invalid book, same token.
- Action: Submit own loan; spoof member; replay same token pada waktu berbeda; replay token dengan book/principal berbeda; replay tanpa valid principal; new token same book; concurrent same-token requests.
- Expected: Owner from principal; pending record; invalid/spoof no mutation; replay waktu berbeda tetap same UUID (no token expiry); payload/principal mismatch409 tanpa loan detail; unauthenticated replay denied; new token permitted; race one token record.
- Evidence: case result and artifacts above; specific raw server latency samples for VER-011, transaction logs/count queries for VER-008, backup manifest and restore timeline for VER-012.


## AC-003 / VER-003
Links: FR-003; PERM-003/007. Method: authorization integration/E2E. Environment: staging synthetic. Status: planned.
- Setup: Members A/B with loans in each state.
- Action: List A; request B UUID as A; request global list as member.
- Expected: Only A rows; 404 B detail; 403 global list; no disclosure.
- Evidence: case result and artifacts above; specific raw server latency samples for VER-011, transaction logs/count queries for VER-008, backup manifest and restore timeline for VER-012.


## AC-004 / VER-004
Links: FR-004; PRD-004. Method: integration/E2E. Environment: staging synthetic. Status: planned.
- Setup: Librarian and both members with each state.
- Action: Open global list/detail and filter state.
- Expected: All owners visible to librarian; filter correct; member denied.
- Evidence: case result and artifacts above; specific raw server latency samples for VER-011, transaction logs/count queries for VER-008, backup manifest and restore timeline for VER-012.


## AC-005 / VER-005
Links: FR-005; BR-001. Method: integration/E2E. Environment: staging PostgreSQL16. Status: planned.
- Setup: Pending free-book loan and roles.
- Action: Approve librarian; approve again; approve member; invalid UUID.
- Expected: First approved+actor/time; repeats 409 audit unchanged; member403; invalid400.
- Evidence: case result and artifacts above; specific raw server latency samples for VER-011, transaction logs/count queries for VER-008, backup manifest and restore timeline for VER-012.


## AC-006 / VER-006
Links: FR-006; BR-001. Method: integration/E2E. Environment: staging PostgreSQL16. Status: planned.
- Setup: Pending and approved/rejected/returned loan fixtures.
- Action: Reject pending as librarian; invalid-state and member attempts.
- Expected: Only pending becomes rejected with actor/time; others409/member403 unchanged.
- Evidence: case result and artifacts above; specific raw server latency samples for VER-011, transaction logs/count queries for VER-008, backup manifest and restore timeline for VER-012.


## AC-007 / VER-007
Links: FR-007; BR-001/003. Method: integration/E2E. Environment: staging PostgreSQL16. Status: planned.
- Setup: Approved and other state fixtures.
- Action: Record return; repeat return; member return.
- Expected: Returned_at written; original decision retained; repeat409/member403 unchanged.
- Evidence: case result and artifacts above; specific raw server latency samples for VER-011, transaction logs/count queries for VER-008, backup manifest and restore timeline for VER-012.


## AC-008 / VER-008
Links: BR-001/002; CON-002; ADR-002. Method: concurrency integration; DB constraint inspection/test. Environment: PostgreSQL16 staging. Status: planned.
- Setup: Two pending loans one free book, two independent DB transactions.
- Action: Synchronize two approvals at barrier; approve vs reject same loan; return vs approve same book; direct DB attempt two approved.
- Expected: Max approved count1 always; losing approval pending409; same-loan one transition; serialized return/approval; DB constraint rejects invalid write.
- Evidence: case result and artifacts above; specific raw server latency samples for VER-011, transaction logs/count queries for VER-008, backup manifest and restore timeline for VER-012.


## AC-009 / VER-009
Links: DATA-002/003; BR-003; CON-003/004/005. Method: integration/schema inspection. Environment: staging synthetic. Status: planned.
- Setup: Loan lifecycle and identity role-change fixtures.
- Action: Inspect fields across states; change actor role in adapter; try deletion/invalid timestamp fixture.
- Expected: Required/null fields match dictionary, decision IDs/time stable; invalid checks/FKs fail; no portal deletion route.
- Evidence: case result and artifacts above; specific raw server latency samples for VER-011, transaction logs/count queries for VER-008, backup manifest and restore timeline for VER-012.


## AC-010 / VER-010
Links: IF-001; NFR-003; PERM-008. Method: contract test/network probes/config inspection. Environment: staging plus adapter test environment. Status: planned.
- Setup: Actual adapter test contract, prod-shaped staging, recognized/missing/unrecognized principal.
- Action: Contract test trusted ID/role and revoke/session behavior inherited; forge identity; external connect app/DB; inspect TLS/process/DB version.
- Expected: No role fallback; spoof denied; session matches adapter evidence; only proxy public; TLS ingress; app/DB private; PG16 SSR monolith.
- Evidence: case result and artifacts above; specific raw server latency samples for VER-011, transaction logs/count queries for VER-008, backup manifest and restore timeline for VER-012.


## AC-011 / VER-011
Links: NFR-001. Method: load test/server instrumentation. Environment: prod-shaped staging. Status: planned.
- Setup: 10k synthetic books,20 concurrent authenticated virtual users; recorded VM/app/PG versions.
- Action: Warm-up separately; then 5min steady catalogue requests; collect server start-to-ready durations, all successes/errors and percentile method.
- Expected: p95≤500ms for steady server samples excluding network/browser; no hidden error filtering; errors reported and functional cases still pass.
- Evidence: case result and artifacts above; specific raw server latency samples for VER-011, transaction logs/count queries for VER-008, backup manifest and restore timeline for VER-012.


## AC-012 / VER-012
Links: NFR-002; ADR-003. Method: recovery drill/backup inspection. Environment: replacement staging VM. Status: planned.
- Setup: Daily encrypted off-VM backup, synthetic data, replacement VM provision path.
- Action: Simulate source VM unavailable; time incident→replacement provision→restore→checks→portal ready; calculate newest recovered commit age.
- Expected: Backup run daily; RPO≤24h; total RTO≤8h; count/FK/state/audit checks and member/librarian live path pass.
- Evidence: case result and artifacts above; specific raw server latency samples for VER-011, transaction logs/count queries for VER-008, backup manifest and restore timeline for VER-012.


## AC-013 / VER-013
Links: DATA-001; NFR-004; CON-001; FR-001–007. Method: schema integration/manual keyboard/E2E. Environment: staging synthetic. Status: planned.
- Setup: Synthetic ISBN null/duplicate/blank/title fixtures; keyboard browser.
- Action: Validate data checks; keyboard full submit/approve/return path; induce DB unavailable and CSRF-invalid requests.
- Expected: Multiple null ISBN allowed, non-null unique, blank normalized; labels/focus/errors usable; DB failure no success/partial write; unsafe POST denied.
- Evidence: case result and artifacts above; specific raw server latency samples for VER-011, transaction logs/count queries for VER-008, backup manifest and restore timeline for VER-012.


Post-launch measures unspecified, no invented metric target. Runtime failures require rerun affected cases after fix; test outcomes never substituted by a build or health response.
