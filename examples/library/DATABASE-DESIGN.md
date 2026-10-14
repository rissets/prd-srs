# Database design
0.1 MVP/draft. Domain confirmed SRC-001 S4, all physical types/constraints proposed for PostgreSQL16. DIA-008 ERD in ARCHITECTURE.md; no schema/DDL executed.

ENT-001 user_reference: external identity reference, adapter source, shared FK target; snapshot role for traceability only. ENT-002 book: single borrowable object, library source; global catalog read. ENT-003 loan: portal source, member owns read scope, librarian global; never deleted MVP. One book has 0..many loans, each loan one book; user has 0..many member loans, each loan one member; decider relationship nullable before decision, one user can decide many loans. External ID immutable opaque proposal; identity deletion does not delete local historical refs.

## Complete dictionary
| Entity.field | Logical/physical type, size/unit | Null/default | Key/check | Meaning/source/sensitivity |
|---|---|---|---|---|
| ENT-001.external_id | opaque text/text, no invented length limit | no/adapter | PK | adapter ID; personal identifier |
| ENT-001.last_observed_role | role/text member or librarian | no/adapter | check enum | snapshot; never authority; access-sensitive |
| ENT-002.id | identifier/uuid 128bit | no/generated UUID | PK | book ID/public catalog |
| ENT-002.title | title/text | no/no default | nonblank trimmed | source catalog title; nonpersonal |
| ENT-002.isbn | optional business key/text | yes/null | global unique non-null; blank→null | trimmed exact string unique; no invented ISBN format; nonpersonal |
| ENT-003.id | identifier/uuid 128bit | no/generated UUID | PK | loan identifier/access-sensitive |
| ENT-003.book_id | book reference/uuid | no/no default | FK ENT-002.id RESTRICT | requested book |
| ENT-003.member_external_id | user reference/text | no/adapter current principal | FK ENT-001.external_id RESTRICT | owner personal identifier |
| ENT-003.state | state/text enum | no/pending on create | pending/approved/rejected/returned | loan lifecycle/access-sensitive |
| ENT-003.submitted_at | instant/timestamptz UTC, microsecond | no/server creation clock | immutable | submit time/access-sensitive |
| ENT-003.decided_at | instant/timestamptz UTC, microsecond | yes/null until decision | required for approved/rejected/returned | original decision time/access-sensitive |
| ENT-003.returned_at | instant/timestamptz UTC, microsecond | yes/null until return | present only returned | return time/access-sensitive |
| ENT-003.decider_external_id | user reference/text | yes/null until decision | FK ENT-001.external_id RESTRICT | original decision actor; required after decision, optional in domain before decision |
| ENT-003.submission_token | technical id/uuid 128bit | no/form-generated | global unique | ADR-004 retry identifier; no business authority; no expiry, retained with loan |

Timestamp rendering proposal UTC with explicit timezone label, no locale-specific obligation. Snapshot role upsert on authenticated interaction, no periodic sync promise. External ID change requires adapter contract reconciliation, not guessed account migration.

## Constraints and indexes
| ID | Enforcement/design | Reason/query | Cost/status |
|---|---|---|---|
| CON-001 | DB global unique non-null ISBN; multiple null permitted | DATA-001 | index writes; proposed |
| CON-002 | DB partial unique (book_id) WHERE state='approved' | BR-002 independent backstop | active loan index maintenance; proposed |
| CON-003 | DB state/timestamp/decider check: pending none; approved/rejected decided+decider with return null; returned all decision+return fields | DATA-002/003 | checks every write; proposed |
| CON-004 | DB timestamp order submitted≤decided≤returned when present | audit integrity | application clock monitored; proposed |
| CON-005 | DB FKs RESTRICT and app no loan delete capability | BR-003, ownership | references retained; proposed |
| CON-006 | DB unique submission_token and app matching member/book on replay | FR-002 retry | extra index/storage; proposed |
| IDX-001 | loan(member_external_id, submitted_at DESC, id) | FR-003 own chronological pages | writes/storage; proposed |
| IDX-002 | loan(state, submitted_at DESC, id) | FR-004 state-filter pending queue | writes/storage; proposed |
| IDX-003 | loan(submitted_at DESC, id) | FR-004 all chronological pages | writes/storage; proposed |
| IDX-004 | book(title, id) | FR-001 deterministic alphabetical catalog | writes/storage; proposed |

FK referenced PK indexes implicit; no assumption that all FK indexes are automatic. No title search required; avoid invented full-text/trigram indexing. Pagination offsets bounded by 10k catalog and proposed default page50; profile actual queries before further indexes. Fields normalized, no JSON/blob/file. Books/users cannot be deleted while referenced; no account CRUD portal. No loan deletion/archival process introduced.

## Transactions and concurrent operations
Submit transaction validates book/current member and inserts loan with unique token; duplicate-token race loads matching committed loan, foreign token/payload denies409 without loan disclosure. Submission token has no time-based expiry and remains with the nondeleted loan; adapter/session authorization still checked on every replay. Upsert external reference and loan creation commit together; failure does not leave a loan.

All decision/return transactions acquire same book row then target loan row, re-read state and existing approved after locks. Approval writes state/decision actor/time atomically, conditional on pending/free; partial unique index adds DB defense. Locks held until commit. Approve versus return on same book serializes; final state may legitimately permit a new approval only after committed return. Approve versus reject same pending: one commits, loser 409. Two different pending approvals same book: one succeeds, other remains pending. Deadlock/timeout rolls back and shows retryable generic failure; no automatic duplicate business write.

Diagnostic logs do not replace audit: decided_at/decider/state survive returned transition. There is only one original decision per lifecycle, so a separate event history table is unnecessary for scope. Pending have null decision fields; rejected/returned terminal. Role updates do not rewrite decider IDs or loan timestamps.

## Onboarding and recovery
New schema; no existing database migration mapping supplied. Proposed migrations create tables, checks, indexes; pre-load validates unique ISBN and book UUID/title before commit; input provenance must be supplied by library outside portal. Synthetic fixtures only for QA. No fabricated live catalog source. Schema version and app config included in encrypted off-VM backup package; restoration validates count/state/FK/uniqueness and audit samples. Production onboarding cannot complete without actual catalog/adapter contract.

Backup every day (ADR-003), 7 retained copies proposed; audit retained in live loans rather than guaranteed forever in diagnostic logs. SQL/database behavior and migrations need future VER-008/009/013, not proven by dictionary writing.
