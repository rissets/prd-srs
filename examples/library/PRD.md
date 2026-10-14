# PRD
Baseline 0.1, MVP, draft. Pembaca: stakeholder perpustakaan, engineering, QA. Evidence confirmed berarti eksplisit di SRC-001, bukan approval dokumen.

## Masalah, outcome, dan bukti
Portal menyediakan alur katalog → pengajuan → keputusan → pengembalian. Workflow saat ini dan tingkat friksi belum diketahui; hipotesis manfaat adalah pencatatan dan keterlacakan terpusat, bukan klaim riset.

GOAL-001: anggota dapat mengajukan dan melihat status pinjaman sendiri. GOAL-002: pustakawan mengelola seluruh siklus secara konsisten. GOAL-003: layanan dapat diakses secara internal melalui ingress publik dan dipulihkan dari backup. Semua bersumber SRC-001 S1–S7.

Indikator penerimaan peluncuran: seluruh kasus VER-001 sampai VER-013 lulus; zero buku dengan lebih dari satu approved setelah race; latensi dan recovery sesuai NFR. Baseline operasional tidak tersedia. Ukuran manfaat pascapeluncuran belum ditargetkan; tidak ada klaim adopsi atau efisiensi.

## Aktor dan lingkup
Anggota: katalog, pengajuan sendiri, daftar/detail pinjaman sendiri. Pustakawan: katalog sebagai proposal pendukung review buku, daftar/detail semua loan, keputusan, pengembalian. Operator akun di luar boundary; role/grant/revoke mengikuti adapter, tanpa UI portal untuk itu. Tidak ada tenancy atau admin tanpa batas.

MVP hanya kemampuan tersebut. Semua kebutuhan tabel adalah Must/MVP. Denda, due date, notifikasi, file, ekspor, dashboard metrik, public signup, kelola akun, CRUD katalog interaktif, pembatalan, renewal dan penghapusan loan tidak masuk MVP. CRUD katalog tidak diminta; provisioning data menjadi dependensi teknis onboarding, bukan fitur tambahan.

## Kebutuhan produk
| ID | Outcome | Sumber | Anak SRS | Penerimaan | Evidence/lifecycle |
|---|---|---|---|---|---|
| PRD-001 | Katalog tersedia bagi anggota | SRC-001 S2 | FR-001 | VER-001 | confirmed/draft |
| PRD-002 | Anggota mengajukan pinjaman untuk dirinya | SRC-001 S2 | FR-002 | VER-002 | confirmed/draft |
| PRD-003 | Anggota melihat pinjaman sendiri | SRC-001 S2 | FR-003 | VER-003 | confirmed/draft |
| PRD-004 | Pustakawan melihat seluruh pinjaman | SRC-001 S2 | FR-004 | VER-004 | confirmed/draft |
| PRD-005 | Pustakawan memutuskan pending | SRC-001 S2/S3 | FR-005, FR-006 | VER-005, VER-006 | confirmed/draft |
| PRD-006 | Pustakawan mencatat pengembalian approved | SRC-001 S2/S3 | FR-007 | VER-007 | confirmed/draft |
| PRD-007 | Persetujuan aman terhadap perebutan buku | SRC-001 S3 | BR-002 | VER-008 | confirmed/draft |
| PRD-008 | Keputusan tetap dapat ditelusuri selama loan | SRC-001 S4 | DATA-003, BR-003 | VER-009 | confirmed/draft |
| PRD-009 | Portal memenuhi akses internal, kapasitas dan pemulihan | SRC-001 S1/S6/S7 | IF-001, NFR-001, NFR-002, NFR-003 | VER-010, VER-011, VER-012 | confirmed/draft |

## Journey, data, dan kegagalan
Journey rinci UC-001–UC-007 dan WF-001 ada di WORKFLOWS-AND-ACCESS.md. Katalog kosong menampilkan pesan kosong; pinjaman kosong menampilkan belum ada pengajuan. Proposal UI: server-rendered daftar berhalaman, detail buku, formulir POST konfirmasi, pesan validasi dekat input, status teks, label dan fokus keyboard. Kegagalan commit tidak boleh menampilkan sukses; pengguna dapat retry melalui form yang sama. Tidak ada notifikasi terpisah.

Data katalog dan loan dimiliki satu perpustakaan; identity ID/role bersumber adapter. Nama/email user tidak dibutuhkan. Semua test fixture sintetis. Tidak ada integrasi pihak ketiga selain adapter dan penyimpanan backup operasional proposed.

## Rilis dan risiko
Urutan relatif di IMPLEMENTATION-PLAN.md. UAT: perwakilan pustakawan (SRC-001 S8). Otoritas approval dokumen belum ditentukan, sehingga paket tidak approved. Risiko utama adalah race approval, scope leak, adapter mismatch, dan backup tidak dapat dipulihkan; VER-008, VER-003/010, VER-010, VER-012 mengatasinya. Risiko katalog belum dipasok ditangani sebagai prasyarat TASK-001.
