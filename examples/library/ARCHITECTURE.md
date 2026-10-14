# Arsitektur proposed
0.1 MVP/draft. Stack dan exposure confirmed SRC-001 S6; pembagian modul, ports, sizing, backup dan routes proposed.

## DIA-001: Konteks
MVP, proposed/draft. Links: PRD-001–009; IF-001. Editable source: [diagrams/context.mmd](diagrams/context.mmd). Legend: solid = interaction/dependency; dashed = recovery relation; shapes are logical nodes unless topology VM boundary specifies deployment.

```mermaid
flowchart LR
 A[Anggota] -->|Katalog dan loan sendiri| P[Portal satu perpustakaan]
 L[Pustakawan] -->|Keputusan dan pengembalian| P
 I[Adapter identity existing] -->|Trusted external ID dan role| P
 O[Operator di luar portal] -->|Provision akun di luar scope| I
 P -->|Data loan dan katalog| DB[(PostgreSQL16 private)]
```

## DIA-002: Komponen
MVP, proposed/draft. Links: FR-001–007; BR-001–003. Editable source: [diagrams/components.mmd](diagrams/components.mmd). Legend: solid = interaction/dependency; dashed = recovery relation; shapes are logical nodes unless topology VM boundary specifies deployment.

```mermaid
flowchart LR
 B[Browser] -->|HTTPS| R[Reverse proxy]
 R -->|HTTP loopback proposed| V[Django views dan SSR]
 I[Adapter existing] -->|Principal| V
 V --> A[Authorization dan scoped query]
 A --> C[Catalog query]
 A --> L[Loan service dan transaction]
 C --> D[(PostgreSQL16)]
 L --> D
 V -->|HTML dan feedback| B
```

## DIA-003: Topology staging dan produksi
MVP, proposed/draft. Links: NFR-002, NFR-003. Editable source: [diagrams/topology.mmd](diagrams/topology.mmd). Legend: solid = interaction/dependency; dashed = recovery relation; shapes are logical nodes unless topology VM boundary specifies deployment.

```mermaid
flowchart LR
 B[Authenticated browser] -->|HTTPS 443| R
 subgraph VM[Linux VM - satu per environment]
 R[Public TLS reverse proxy] -->|HTTP 127.0.0.1:8000 proposed| A[Django process private]
 A -->|TCP 127.0.0.1:5432 proposed| D[(PostgreSQL16 private)]
 J[Daily backup timer proposed] -->|Local dump| D
 end
 J -->|Outbound HTTPS 443 encrypted backup proposed| S[Off VM backup storage]
 X[Replacement VM] -. Restore drill .-> S
```

## DIA-004: Workflow bisnis WF-001
MVP, proposed/draft. Links: FR-002, FR-005–007; BR-001/002. Editable source: [diagrams/business.mmd](diagrams/business.mmd). Legend: solid = interaction/dependency; dashed = recovery relation; shapes are logical nodes unless topology VM boundary specifies deployment.

```mermaid
flowchart TD
 subgraph Anggota
 A[Mulai: memilih buku]
 B[Ajukan untuk diri sendiri]
 end
 subgraph Pustakawan
 E[Tolak pending]
 F[Setujui pending]
 I[Catat pengembalian]
 end
 subgraph Sistem
 C[Loan pending]
 D{Buku masih bebas dan loan pending?}
 R[rejected - selesai]
 G[approved]
 H[Konflik: pending tetap]
 J[returned - selesai]
 end
 A --> B
 B --> C
 C --> E
 C --> F
 F --> D
 E --> R
 D -->|Ya: atomic commit| G
 D -->|Tidak| H
 G --> I
 I --> J
```

## DIA-005: State loan
MVP, proposed/draft. Links: BR-001; FR-005–007. Editable source: [diagrams/states.mmd](diagrams/states.mmd). Legend: solid = interaction/dependency; dashed = recovery relation; shapes are logical nodes unless topology VM boundary specifies deployment.

```mermaid
stateDiagram-v2
 [*] --> pending: submit anggota
 pending --> approved: approve pustakawan dan buku bebas
 pending --> rejected: reject pustakawan
 approved --> returned: catat pengembalian
 rejected --> [*]
 returned --> [*]
```

## DIA-006: System sequence submit dan approval
MVP, proposed/draft. Links: FR-002/005; BR-002. Editable source: [diagrams/sequence.mmd](diagrams/sequence.mmd). Legend: solid = interaction/dependency; dashed = recovery relation; shapes are logical nodes unless topology VM boundary specifies deployment.

```mermaid
sequenceDiagram
 actor A as Anggota
 actor L as Pustakawan
 participant V as Django view
 participant I as Identity adapter
 participant S as Loan service
 participant D as PostgreSQL16
 A->>V: POST submit book/token
 V->>I: Baca trusted principal
 I-->>V: external ID dan member role
 V->>S: Validasi scope, UUID dan token
 S->>D: Atomic insert pending atau lookup retry token
 D-->>S: Committed loan UUID
 S-->>V: Loan UUID dan hasil submit
 V-->>A: Redirect detail milik sendiri
 L->>V: POST approve loan
 V->>I: Baca trusted principal
 I-->>V: external ID dan librarian role
 V->>S: Authorize sebelum mutasi
 S->>D: BEGIN, lock book lalu loan, cek pending/free
 alt Guard valid
 S->>D: Update approved + decided_at + decider, COMMIT
 D-->>S: committed
 S-->>V: Approval berhasil
 V-->>L: Redirect detail sukses
 else Guard konflik atau unique violation
 S->>D: ROLLBACK
 S-->>V: Konflik dan status terkini
 V-->>L: 409 dan status terkini
 else Database gagal
 S->>D: ROLLBACK jika koneksi tersedia
 S-->>V: Database unavailable
 V-->>L: 503 tanpa sukses, reload sebelum retry
 end
```

## DIA-007: System sequence reject dan return
MVP, proposed/draft. Links: FR-006/007; BR-001/003. Editable source: [diagrams/return.mmd](diagrams/return.mmd). Legend: solid = interaction/dependency; dashed = recovery relation; shapes are logical nodes unless topology VM boundary specifies deployment.

```mermaid
sequenceDiagram
 actor L as Pustakawan
 participant V as Django view
 participant I as Identity adapter
 participant S as Loan service
 participant D as PostgreSQL16
 L->>V: POST reject atau return UUID
 V->>I: Trusted principal
 I-->>V: ID dan role
 V->>S: Authorize librarian, validasi action
 S->>D: BEGIN, lock book lalu loan
 alt reject dengan pending
 S->>D: Set rejected, decided_at, decider, COMMIT
 D-->>S: committed
 S-->>V: Rejection berhasil
 V-->>L: Detail rejected
 else return dengan approved
 S->>D: Set returned, returned_at, pertahankan decision, COMMIT
 D-->>S: committed
 S-->>V: Return berhasil
 V-->>L: Detail returned
 else Invalid state
 S->>D: ROLLBACK
 S-->>V: Konflik state
 V-->>L: 409, audit tetap
 end
```

## DIA-008: ERD proposed
MVP, proposed/draft. Links: DATA-001–003; BR-002/003. Editable source: [diagrams/erd.mmd](diagrams/erd.mmd). Legend: solid = interaction/dependency; dashed = recovery relation; shapes are logical nodes unless topology VM boundary specifies deployment.

```mermaid
erDiagram
 USER_REFERENCE ||--o{ LOAN : member
 USER_REFERENCE o|--o{ LOAN : decider
 BOOK ||--o{ LOAN : requested
 USER_REFERENCE {
 text external_id PK
 text last_observed_role
 }
 BOOK {
 uuid id PK
 text title
 text isbn UK
 }
 LOAN {
 uuid id PK
 uuid book_id FK
 text member_external_id FK
 text state
 timestamptz submitted_at
 timestamptz decided_at
 timestamptz returned_at
 text decider_external_id FK
 uuid submission_token UK
 }
```

## DIA-009: Use-case relationship map, bukan UML
MVP, proposed/draft. Links: UC-001–007. Editable source: [diagrams/usecases.mmd](diagrams/usecases.mmd). Legend: solid = interaction/dependency; dashed = recovery relation; shapes are logical nodes unless topology VM boundary specifies deployment.

```mermaid
flowchart LR
 A[Anggota] --> U1
 A --> U2
 A --> U3
 L[Pustakawan] --> U1
 L --> U4
 L --> U5
 L --> U6
 L --> U7
 subgraph Portal[single library portal]
 U1[UC-001 Lihat katalog]
 U2[UC-002 Ajukan pinjaman]
 U3[UC-003 Lihat pinjaman sendiri]
 U4[UC-004 Lihat semua pinjaman]
 U5[UC-005 Setujui pending]
 U6[UC-006 Tolak pending]
 U7[UC-007 Catat pengembalian]
 end
```

## DIA-010: Dependensi task relatif
MVP, proposed/draft. Links: TASK-001–007. Editable source: [diagrams/dependencies.mmd](diagrams/dependencies.mmd). Legend: solid = interaction/dependency; dashed = recovery relation; shapes are logical nodes unless topology VM boundary specifies deployment.

```mermaid
flowchart LR
 T1[TASK-001 Binding dan lingkungan] --> T2[TASK-002 Katalog dan data]
 T2 --> T3[TASK-003 Pengajuan dan scope sendiri]
 T3 --> T4[TASK-004 Review dan return atomic]
 T4 --> T5[TASK-005 Performance dan akses]
 T1 --> T6[TASK-006 Backup dan recovery]
 T5 --> T7[TASK-007 UAT dan release review]
 T6 --> T7
```

## Tanggung jawab dan failure
Browser menampilkan HTML dan feedback; tidak menentukan ownership. Django view menjalankan interface/CSRF; authorization memvalidasi role principal dan scopes reads; catalog hanya read book; loan service memiliki transisi dan audit transaction. PostgreSQL menyimpan user references, books, loans dan constraints. Adapter owns identity/session; kegagalan atau principal tidak trusted menyebabkan denial sesuai contract, bukan default role. DB failure membatalkan mutasi, menampilkan unavailable. Tidak ada worker/queue/cache lintas proses yang dibutuhkan.

## Topology table
| Node | Environment | Purpose/exposure | Dependency/protocol | Persistence | Link |
|---|---|---|---|---|---|
| TLS proxy | prod/staging | public ingress | client HTTPS443; app loopback HTTP8000 proposed | TLS cert/config | NFR-003 |
| Django SSR | prod/staging | private process | adapter binding existing; DB loopback5432 | no durable app files | FR-001–007 |
| PostgreSQL16 | prod/staging | private local DB | only app/backup local | all domain data | DATA-001–003 |
| Backup timer | prod/staging | private scheduled operation | local dump, outbound HTTPS443 proposed | encrypted off-VM object | NFR-002 |
| Replacement VM | recovery drill | same topology | restore off-VM backup | restored database | NFR-002 |

Dev uses local isolated DB/synthetic fixtures, TLS optional local; staging matches prod topology and initial proposed size (2 vCPU, 4GB RAM, 40GB durable disk) for meaningful performance tests. Proposed single VM has no failover; RTO relies replacement provisioning. Never label sizing as measured sufficient. Secrets via restricted environment file owned by runtime identity; no secret values in docs/backups/logs; least privilege app database role proposed. Proxy only publicly listens 443; administrative access policy is environment setup, not portal role. Existing adapter network requirements must be inspected, not invented.

## Decision records
| ADR | Context and alternatives | Proposal/rationale | Tradeoff | Links/status |
|---|---|---|---|---|
| ADR-001 | One VM constraint; Unix socket versus loopback HTTP/TCP | loopback8000/5432 simplifies repeatable staging setup | secure via bind/firewall; no VM redundancy | NFR-003, DIA-002/003; proposed/draft |
| ADR-002 | Concurrent approved per book; app-only checks versus DB unique + locking | book-row lock plus partial unique index and state guards | serialization per book; race tests required; no global lock | BR-001/002, DIA-006; proposed/draft |
| ADR-003 | Daily backup/RPO24h/RTO8h; local-only vs off-VM | encrypted daily logical dump to independent storage; retain 7 daily copies proposed; alert at age>24h | interval plus missed run can violate RPO; dump restore must be drilled; storage/provider not selected | NFR-002; proposed/draft |
| ADR-004 | Retry submit may duplicate intent | unique form submission token stored in loan without time-based expiry; authentication/authorization checked per replay | extra technical field retained with loan; matching old token retrieves same loan, mismatched principal/book rejected; new token still permits additional pending | FR-002; proposed/draft |

Operational diagnostics proposed: request ID, operation, status, duration, exception class; no principal/session secrets. Metrics operational only, no dashboard feature. Catalog request timer supplies NFR-001 samples. Rollout and abort policy in TASK-007; no deploy performed. No unresolved question required for delegated technical proposals; actual adapter wiring and backup storage are implementation prerequisites.

## DIA-011: UML use-case diagram
MVP proposed/draft. Links UC-001–007, PERM-001–009. Editable UML source: [diagrams/usecases.puml](diagrams/usecases.puml). Actor associations enumerate allowed actions; librarian catalog grant remains proposed. Portal rectangle defines boundary. Include/extend unnecessary for independent goals. DIA-009 remains supplemental preview only. PlantUML syntax/render/visual export have not been verified; Mermaid validation cannot validate UML.
