# Paket portal peminjaman perpustakaan
Versi 0.1, 2026-10-14. Release MVP; seluruh dokumen lifecycle **draft**, belum approved. Kesiapan: **ready for stakeholder review**. Tidak ada keputusan bisnis yang perlu diblokir dari catatan yang diberikan. Pilihan desain berstatus proposed; kesiapan implementasi bergantung pada review desain dan verifikasi kontrak adapter existing.

Paket hanya perencanaan: tidak ada implementasi, deployment, UAT atau pengujian runtime yang dilakukan.

- [Catatan sumber](SOURCES.md)
- [PRD](PRD.md)
- [SRS](SRS.md)
- [Arsitektur](ARCHITECTURE.md)
- [Alur dan akses](WORKFLOWS-AND-ACCESS.md)
- [Database](DATABASE-DESIGN.md)
- [Rencana implementasi](IMPLEMENTATION-PLAN.md)
- [Verifikasi terencana](VERIFICATION.md)
- [Traceability](TRACEABILITY.md)
- [Pertanyaan](QUESTIONS.md)
- [Pemeriksaan paket](DOCUMENT-VERIFICATION.md)

Glosarium bersama: anggota = actor role member; pustakawan = actor role librarian; pending = pengajuan belum diputuskan; approved = pinjaman aktif; rejected = pengajuan ditolak; returned = pinjaman selesai dikembalikan. Buku adalah satu objek yang dapat dipinjam, bukan kelompok eksemplar. Identity external ID adalah pengenal opaque dari adapter, bukan akun portal.

Riwayat: 0.1 baseline pertama dari catatan stakeholder sintetis SRC-001; tidak ada ID retired atau approval historis.

Revision review: repair sequence punctuation, eliminate approval bypass edge, reconcile proposed librarian catalog association, add UML source DIA-011, replace generic UC steps with concrete domain exchanges.
