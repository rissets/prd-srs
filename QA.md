# QA — v0.1.0

Audit dilakukan 2026-10-14. Proyek, data, dan keputusan stakeholder pada fixture bersifat sintetis.

| Pemeriksaan | Hasil |
|---|---|
| Struktur skill, YAML, code fences, referensi | Lulus |
| Negative controls: referensi/invocation/fence rusak | 3/3 terdeteksi |
| Tiga skenario independen | Konteks ambigu, paket lengkap, review-only konflik sumber |
| Dua uji lanjutan | Klarifikasi terfokus dan pencatatan approval eksplisit terbatas |
| Mermaid | 18/18 sumber parse/render lulus setelah koreksi: 8 draf ambigu + 10 paket lengkap |
| PlantUML | 1/1 sumber syntax check dan SVG/PNG render lulus |
| Integritas contoh lengkap | 13 pemeriksaan lulus; 18 requirement terpetakan, 14 field ERD/dictionary cocok |

Temuan awal mencakup semicolon sequence yang gagal diparse, bypass aksi approval, UML source yang belum disediakan, asosiasi permission yang hilang, pertanyaan terlalu padat, langkah use case generik, expiry token yang belum terdefinisi, opsionalitas field ambigu, swimlane yang salah pemilik, dan response chain yang melewati service. Skill dan contoh diperbaiki, kemudian diverifikasi ulang. Parser valid tidak menggantikan review makna bisnis.

Bukti: [integritas](tests/evidence/package-results.json), [Mermaid paket lengkap](tests/evidence/mermaid-results.json), [PlantUML](tests/evidence/plantuml-results.json), [negative controls](tests/evidence/negative-controls.json). Renderer audit: Mermaid 11.17.2 dan PlantUML 1.2026.8 dengan Smetana. Binary renderer tidak dibundel; CI menjalankan structural/regression checks, tidak mengulang rendering atau evaluasi model independen.

Contoh akhir tersedia di [examples/library](examples/library/README.md). Skenario menerima constraints PostgreSQL16/Django SSR/single VM dari stakeholder sintetis, dengan detail teknis tersisa didelegasikan sebagai proposal. Tidak ada permintaan klarifikasi kepada user nyata selama simulasi.

Tidak ada implementasi aplikasi, eksekusi SQL/migrasi PostgreSQL, load/performance test, restore drill, deployment, atau UAT yang dilakukan. VER-001–013 pada contoh adalah rencana verifikasi masa depan. Validasi layout DOCX/PDF dan automatic discovery global juga belum dilakukan.
