# Register sumber
| ID | Locator dan versi | Fakta | Batasan |
|---|---|---|---|
| SRC-001 | Catatan stakeholder sintetis, pesan simulasi pengujian, baseline 2026-10-14; bagian S1–S8 di bawah | Seluruh constraint pengguna | Bukan wawancara nyata; tidak membuktikan sistem existing maupun hasil runtime |

S1. Portal internal satu perpustakaan, tanpa multi-tenant. Anggota dan pustakawan. Akun dibuat operator di luar portal; adapter existing memberi user ID dan role; login/session mengikuti adapter dan implementasinya di luar desain.

S2. Anggota melihat katalog, mengajukan untuk dirinya, melihat pinjaman sendiri. Pustakawan melihat semua pinjaman, approve/reject pending, mencatat pengembalian approved.

S3. pending → approved/rejected; approved → returned. Maksimal satu approved per buku; pending boleh banyak; concurrent approval harus mempertahankan invariant.

S4. User external ID/role; book UUID/title/ISBN unik opsional; loan UUID/book/member/state/submitted_at/decided_at/returned_at/decider optional. Audit keputusan selama loan; loan tidak dihapus MVP.

S5. Tidak ada denda, notifikasi, file, ekspor, dashboard metrik atau public signup. Tidak ada tanggal MVP atau estimasi durasi; urutan relatif.

S6. PostgreSQL 16, Django monolith server-rendered, satu VM Linux; reverse proxy TLS publik, app/DB private; staging sama bentuk. Sizing/protokol internal dan detail teknis lain boleh diusulkan mandiri; nama asli tidak dibutuhkan.

S7. Backup harian; RPO24h/RTO8h pada replacement VM; teknis backup boleh dipilih. 10k buku, 20 concurrent authenticated users; p95 katalog server request ≤500ms di staging, network/browser excluded, steady test 5 menit.

S8. UAT perwakilan pustakawan. Belum approved. Pertanyaan bisnis unresolved ditulis di QUESTIONS.md dan hanya bagian dependen dihentikan; tidak menghubungi user nyata.

Tidak ada data aktual, baseline adopsi, staffing, budget, kontrak lengkap adapter, hasil test, atau provider backup yang tersedia. Detail itu tidak dipresentasikan sebagai fakta.
