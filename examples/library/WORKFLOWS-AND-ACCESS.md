# Alur, use case, dan akses
MVP/draft; bisnis confirmed SRC-001 S1–S4; technical handling proposed. Diagram DIA-004–007 dan DIA-009 di ARCHITECTURE.md beserta editable sources.

WF-001: anggota mengajukan buku dari katalog; sistem menyimpan pending; pustakawan menerima daftar semua loan dan memutuskan pending. Reject mengakhiri pengajuan; approve membuka pinjaman aktif; return menutupnya. Preconditions identity valid/book ada; input book/loan UUID; output loan dan state. Guard BR-001/002. Alternatif: race pada buku menampilkan konflik tanpa menolak otomatis; denied role tidak memutasi; DB failure memungkinkan reload/retry. Tidak ada due date/escalation/cancel yang disepakati. Links UC-002/005/006/007, FR-002/005/006/007, VER-002/005–008.

## Transition table
| From | Event/actor scope | Guard | To | Persisted effects | Failure |
|---|---|---|---|---|---|
| none | submit/member sendiri | trusted member, book exists | pending | UUID/book/member/submitted_at/token | no insert on invalid/denied |
| pending | approve/librarian global | book has zero approved | approved | decided_at/decider/state atomic | 409 retains pending/audit |
| pending | reject/librarian global | pending at transaction | rejected | decided_at/decider/state atomic | 409 retains state |
| approved | return/librarian global | approved at transaction | returned | returned_at/state; decision retained | 409 retains state |

## Use-case catalog
### UC-001: Daftar/detail katalog
Links FR-001, PRD-001, WF-001 untuk mutasi; DIA-009; DATA-001/002; IF-001.
Actor/scope: anggota dan pustakawan (catalog read proposed). Trigger/preconditions: permintaan daftar/detail dengan principal valid.
1. Aktor meminta halaman katalog berhalaman; server memastikan member/librarian principal recognized.
2. Sistem membaca buku berdasarkan urutan title/UUID dan mengembalikan title/ISBN optional.
3. Aktor memilih book UUID; sistem menampilkan detail buku tersebut.
Alternatif/exceptions: Pada step2 list kosong menghasilkan pesan katalog kosong. Pada step3 UUID unknown404, malformed400; principal denied pada step1 tidak membuka data.
Postconditions: sukses seperti main scenario; failure tidak menambah/mengubah loan atau membocorkan data. AC-001/VER-001 planned; belum ada evidence software.

### UC-002: Ajukan pinjaman
Links FR-002, PRD-002, WF-001 untuk mutasi; DIA-009; DATA-001/002; IF-001.
Actor/scope: anggota, own. Trigger/preconditions: form POST dengan entity dan state sesuai transition table; principal valid.
1. Anggota memilih book UUID dari katalog dan meminta form token submit.
2. Anggota POST book UUID/token tanpa member ID; sistem mengambil member external ID dari adapter dan validasi book ada.
3. Sistem atomik menyimpan pending/submitted_at/token; token retry matching mengembalikan loan existing tanpa expiry waktu selama loan tersimpan; autentikasi/otorisasi tetap diperiksa.
4. Sistem redirect ke detail loan milik anggota setelah commit.
Alternatif/exceptions: Pada step2 spoof member ditolak tanpa loan, invalid UUID400/unknown404. Pada step3 dua token berbeda boleh menghasilkan dua pending; token sama satu record; replay token lain principal/book409 tanpa bocor detail; DB failure rollback lalu503.
Postconditions: sukses seperti main scenario; failure tidak menambah/mengubah loan atau membocorkan data. AC-002/VER-002 planned; belum ada evidence software.

### UC-003: Daftar/detail milik sendiri
Links FR-003, PRD-003, WF-001 untuk mutasi; DIA-009; DATA-001/002; IF-001.
Actor/scope: anggota, own. Trigger/preconditions: permintaan daftar/detail dengan principal valid.
1. Anggota membuka daftar pinjaman sendiri.
2. Sistem membatasi query ke external ID principal dan menampilkan loan UUID/book/state/time miliknya.
3. Anggota memilih loan UUID; sistem melakukan scoped lookup dan mengembalikan detail.
Alternatif/exceptions: Pada step2 daftar kosong menunjukkan belum ada pengajuan. Pada step3 loan milik orang lain/unknown404, tanpa data bocor.
Postconditions: sukses seperti main scenario; failure tidak menambah/mengubah loan atau membocorkan data. AC-003/VER-003 planned; belum ada evidence software.

### UC-004: Daftar/detail seluruh loan
Links FR-004, PRD-004, WF-001 untuk mutasi; DIA-009; DATA-001/002; IF-001.
Actor/scope: pustakawan, global. Trigger/preconditions: permintaan daftar/detail dengan principal valid.
1. Pustakawan membuka daftar seluruh loan, optional filter state proposed.
2. Sistem memastikan librarian dan membaca semua anggota/state satu perpustakaan sesuai filter.
3. Pustakawan memilih loan UUID; sistem menampilkan book/member/state/decision timestamps.
Alternatif/exceptions: Pada step1 member403; step2 filter enum invalid400; step3 unknown UUID404. Tidak ada mutasi di seluruh langkah.
Postconditions: sukses seperti main scenario; failure tidak menambah/mengubah loan atau membocorkan data. AC-004/VER-004 planned; belum ada evidence software.

### UC-005: Setujui pending
Links FR-005, PRD-005, WF-001 untuk mutasi; DIA-009; BR-001/002/003.
Actor/scope: pustakawan, global pending. Trigger/preconditions: form POST dengan entity dan state sesuai transition table; principal valid.
1. Pustakawan memilih pending loan UUID lalu mengirim POST approve.
2. Sistem memvalidasi principal librarian dan UUID, kemudian transaction lock book lalu loan.
3. Sistem re-read pending dan memastikan tidak ada approved pada book; tulis approved/decided_at/decider atomik.
4. Setelah commit sistem redirect ke detail approved dengan decision audit.
Alternatif/exceptions: Pada step2 member403/unknown404 tanpa write. Pada step3 state berubah atau buku terambil409; loser tetap pending jika buku terambil, audit tidak ditulis; DB failure rollback503.
Postconditions: sukses seperti main scenario; failure tidak menambah/mengubah loan atau membocorkan data. AC-005/VER-005 planned; belum ada evidence software.

### UC-006: Tolak pending
Links FR-006, PRD-005, WF-001 untuk mutasi; DIA-009; BR-001/002/003.
Actor/scope: pustakawan, global pending. Trigger/preconditions: form POST dengan entity dan state sesuai transition table; principal valid.
1. Pustakawan memilih pending loan UUID lalu POST reject.
2. Sistem memastikan librarian, lock book lalu loan dan re-read pending.
3. Sistem menulis rejected/decided_at/decider atomik lalu redirect ke detail.
Alternatif/exceptions: Pada step2 member403 atau state nonpending409 mempertahankan state/audit. Pada step3 DB failure rollback503; retry sukses sebelumnya409 dan original decision retained.
Postconditions: sukses seperti main scenario; failure tidak menambah/mengubah loan atau membocorkan data. AC-006/VER-006 planned; belum ada evidence software.

### UC-007: Catat pengembalian
Links FR-007, PRD-006, WF-001 untuk mutasi; DIA-009; BR-001/002/003.
Actor/scope: pustakawan, global approved. Trigger/preconditions: form POST dengan entity dan state sesuai transition table; principal valid.
1. Pustakawan memilih approved loan UUID lalu POST return.
2. Sistem memastikan librarian, lock book lalu loan dan re-read approved.
3. Sistem menulis returned/returned_at atomik, mempertahankan decided_at/decider lalu redirect detail returned.
Alternatif/exceptions: Pada step2 role member403/state nonapproved409 tanpa write. Pada step3 DB failure rollback503; duplicate return409 dan waktu pengembalian pertama tetap.
Postconditions: sukses seperti main scenario; failure tidak menambah/mengubah loan atau membocorkan data. AC-007/VER-007 planned; belum ada evidence software.

## Permission matrix
Roles berasal adapter; grant/revoke/operator accounts di luar scope. Cache role tidak mengotorisasi. Tidak ada role-combination authority yang diciptakan: binding hanya menerima role adapter recognized; contract actual harus diverifikasi.
| ID | Role | Resource/action | Scope/status/condition | Enforcement/audit | Links |
|---|---|---|---|---|---|
| PERM-001 | member | book list/detail | global read allowed | server principal check; no business audit | FR-001, UC-001, VER-001/010 |
| PERM-002 | member | loan create | own, member from adapter | server ownership; submitted_at | FR-002, UC-002, VER-002 |
| PERM-003 | member | loan list/detail | own only | scoped query; other owner 404 | FR-003, UC-003, VER-003 |
| PERM-004 | librarian | loan list/detail | global allowed | role check | FR-004, UC-004, VER-004 |
| PERM-005 | librarian | approve/reject | global pending only; approval book free | server state+transaction; decision audit | FR-005/006, UC-005/006, VER-005/006/008/009 |
| PERM-006 | librarian | return | global approved only | server guard; returned_at | FR-007, UC-007, VER-007 |
| PERM-007 | member | decide/return/global loan list | denied | 403 no mutations; safe diagnostic | FR-003–007, VER-003–007/010 |
| PERM-008 | unrecognized/missing principal | portal data/actions | denied or adapter login entrypoint | fail closed, no role cache fallback | IF-001, VER-010 |
| PERM-009 | librarian | catalog | global read proposed | same server role check | FR-001, VER-001 |

No portal delete/export/import/account management/configuration/book update actions exposed; operator outside portal does not acquire portal superuser. Query authorization applies before rendering or mutating, hidden buttons are only UX.
