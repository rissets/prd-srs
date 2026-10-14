# SRS
Baseline 0.1, MVP, lifecycle draft. FR confirmed dari SRC-001 S2/S3; detail UI, HTTP dan penanganan teknis di tabel berstatus proposed. Seluruh FR Must/MVP. Keputusan teknis tidak mengubah kewenangan atau state bisnis.

## Kebutuhan fungsional
Semua GET/POST memerlukan identity adapter terpercaya. UUID sintaks invalid menghasilkan 400; not found 404. Semua POST memiliki validasi server dan CSRF proposed. Sukses POST memakai redirect ke detail setelah commit (proposal). Database unavailable menghasilkan halaman 503 generik, tanpa detail SQL atau sukses palsu.

| ID | Perilaku | Aktor | Input, precondition, hasil, kegagalan | Parent | Acceptance |
|---|---|---|---|---|---|
| FR-001 | Daftar/detail katalog | anggota; pustakawan proposed | GET dengan book UUID valid; list berhalaman proposed 50 item; title wajib ditampilkan; ISBN ditampilkan bila tersedia; unknown UUID menghasilkan 404; empty list pesan kosong | PRD-001 | AC-001 / VER-001 |
| FR-002 | Ajukan pinjaman | anggota | POST book UUID yang ada; member diambil dari adapter, field member client ditolak; hasil loan UUID pending dan submitted_at; buku tidak ada 404; role salah 403; pending boleh banyak termasuk buku aktif karena syarat ketersediaan hanya pada approval | PRD-002 | AC-002 / VER-002 |
| FR-003 | Daftar/detail milik sendiri | anggota | Query di-scope ke external ID terpercaya; semua state terlihat; UUID loan milik orang lain menghasilkan 404 tanpa data; pagination proposed 50; empty state eksplisit | PRD-003 | AC-003 / VER-003 |
| FR-004 | Daftar/detail seluruh loan | pustakawan | Seluruh anggota dan state satu perpustakaan tersedia; filter state proposal; tanpa pustakawan 403 untuk daftar global | PRD-004 | AC-004 / VER-004 |
| FR-005 | Setujui pending | pustakawan | POST loan UUID; guard pending dan belum ada approved lain pada buku; atomik status approved, decided_at, decider; pelanggaran guard konflik 409; gagal tidak mengubah record | PRD-005 | AC-005 / VER-005 |
| FR-006 | Tolak pending | pustakawan | POST loan UUID; guard pending; atomik rejected, decided_at, decider; state lain 409, role salah 403; tidak ada alasan wajib yang diciptakan | PRD-005 | AC-006 / VER-006 |
| FR-007 | Catat pengembalian | pustakawan | POST loan UUID; guard approved; atomik returned dan returned_at; pertahankan decided_at/decider; state lain 409; tanpa role 403 | PRD-006 | AC-007 / VER-007 |

## Aturan bersama
BR-001 — confirmed/draft, Must/MVP, SRC-001 S3: transisi hanya pending→approved/rejected dan approved→returned. Case VER-005–008.

BR-002 — confirmed/draft, Must/MVP, SRC-001 S3: tiap buku memiliki paling banyak satu loan approved; pending tak dibatasi. Case VER-008; tidak ada auto rejection bagi pending lain.

BR-003 — confirmed/draft, Must/MVP, SRC-001 S4: decision audit tetap disimpan selama loan, loan tidak dihapus MVP. Case VER-009.

## Data dan boundary interface
DATA-001 — confirmed/draft, Must/MVP, SRC-001 S4: book UUID/title wajib, ISBN opsional unik. Null berulang boleh, string kosong dinormalisasi null (proposal); ISBN disimpan teks trimmed tanpa mengasumsikan format/standar tertentu. VER-013.

DATA-002 — confirmed/draft, Must/MVP, SRC-001 S4: loan memuat UUID/book/member/state/submitted_at/decided_at/returned_at/decider sesuai lifecycle. Dictionary di DATABASE-DESIGN.md; VER-009/013.

DATA-003 — confirmed/draft, Must/MVP, SRC-001 S4: user reference mempertahankan external ID/role; keputusan dapat ditelusuri ke decider meski role adapter berubah; desain snapshot tidak memberi akses dari role cache. VER-009/010.

IF-001 — confirmed/draft, Must/MVP, SRC-001 S1: principal user ID/role berasal adapter existing; login/session tetap tanggung jawab adapter. Proposal binding: normalisasi trusted principal ke external_id dan role, hanya member/librarian recognized; missing/invalid principal mengikuti entrypoint login adapter atau denial, tidak fallback ke role lokal. Contract test harus cocok dengan adapter nyata, tanpa mengarang timeout/expiry/provider endpoint. VER-010.

## Nonfungsional
| ID | Metric/threshold/condition | Method dan boundary | Sumber/status |
|---|---|---|---|
| NFR-001 | p95 server request katalog ≤500ms; 10k buku, 20 concurrent authenticated users, staging; 5 menit steady | Timer server ingress sampai response siap, excluding browser/network; laporkan jumlah/error/all latency samples dan p95, cold/warm conditions; VER-011 | SRC-001 S7 confirmed/draft |
| NFR-002 | Backup harian; RPO≤24h dan RTO≤8h pada replacement VM | Backup success age dan restore drill; RPO dari newest recoverable committed data vs incident; RTO incident declaration sampai aplikasi siap dan data tervalidasi, termasuk provision VM; VER-012 | SRC-001 S7 confirmed/draft |
| NFR-003 | TLS public proxy, app/DB private, PostgreSQL16, Django SSR monolith pada satu Linux VM; staging sama bentuk | Inspect network/runtime; external probes tidak dapat mengakses app/DB; VER-010 | SRC-001 S6 confirmed/draft |

NFR-004 — proposed/draft, Must/MVP derived dari PRD-009: label form, navigasi keyboard dan error terhubung ke input untuk seluruh UC; inspeksi/manual keyboard VER-013. Tidak ada klaim compliance standar aksesibilitas tertentu.

Tidak ada uptime SLA, latensi identity provider, target biaya, support browser version atau retensi diagnostic log yang diklaim approved. Proposal browser verification: satu Chromium desktop terkini yang direkam versinya ketika test. Tidak ada AI, offline, payment, geo, reporting atau multi-tenant requirement.

## Mutasi, retry, dan audit
Proposal FR-002: token form satu kali terikat principal/book; retry token sama mengembalikan loan sama, tidak membuat duplikat akibat retry transport. Pengajuan baru token baru tetap boleh pending berganda. Token disimpan pada loan, bukan state browser saja. Token idempotensi tidak memiliki expiry waktu: disimpan selama loan dan replay hanya menghasilkan loan yang sama bila principal/member dan book cocok. Replay token dengan principal atau payload berbeda ditolak 409 tanpa mengungkap detail loan. Token bukan kredensial dan tidak memberi akses tanpa autentikasi/otorisasi; validitas session/CSRF tetap mengikuti adapter dan kebijakan POST portal, terpisah dari token idempotensi. Proposal mutasi decision/return di-state guard: retry setelah sukses mendapat 409 state tidak sesuai sambil menampilkan state terkini; tidak mengubah audit asli. Tidak ada client retry otomatis tanpa feedback.

Semua requirement ditelusuri ke source, task dan kasus di TRACEABILITY.md; verification software tetap planned.
