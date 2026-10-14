# PRD & SRS Skill

Versi **0.1.0** — rilis awal/beta untuk membuat, memperbaiki, dan mereview paket kebutuhan produk serta rencana implementasi. Bahasa mengikuti user; permintaan berbahasa Indonesia menghasilkan dokumen berbahasa Indonesia.

## Kemampuan

- PRD: masalah, pengguna, tujuan terukur, scope, prioritas, journey, dan acceptance criteria.
- SRS: functional/nonfunctional requirements, business rules, data, interface, error dan denial paths.
- Diagram context/component architecture, deployment/network topology, workflow bisnis, sequence dan state.
- Diagram UML use case dan catalog skenario utama, alternatif, serta exception.
- Matriks role/permission dengan scope kepemilikan/tenant dan enforcement.
- ERD, data dictionary, tipe/constraint/index, transaksi, concurrency, lifecycle, dan migrasi yang relevan.
- Implementation plan: fase, tasks, dependensi, deliverables, acceptance, dan release/recovery plan.
- Keterlacakan sumber → requirement → desain → tasks → verifikasi.

Skill wajib bertanya ketika keputusan yang diperlukan belum jelas, memakai ronde pertanyaan terfokus. Bagian yang bergantung pada jawaban tetap pending; asumsi/proposal tidak dianggap approval. Permintaan review atau edit terbatas tetap terbatas pada scope yang diminta.

## Instalasi

Clone repository ke folder skill Codex yang belum ada:

```sh
git clone --branch v0.1.0 --depth 1 https://github.com/rissets/prd-srs.git ~/.codex/skills/prd-srs
```

Jika direktori tersebut sudah berisi skill, periksa instalasi lama terlebih dahulu; perintah clone tidak menggantikannya. Alternatif: unduh `prd-srs-v0.1.0.zip` dari [GitHub Release](https://github.com/rissets/prd-srs/releases/tag/v0.1.0), ekstrak, lalu tempatkan folder `prd-srs` pada direktori skill. Muat ulang daftar skill atau mulai chat baru bila diperlukan oleh host Anda.

Host lain yang mendukung format `SKILL.md` dapat memuat folder ini sesuai mekanisme instalasinya. Validasi automatic discovery lintas host belum dilakukan.

## Pemakaian

```text
Gunakan $prd-srs untuk membuat paket PRD/SRS lengkap untuk [produk].
Sumber: [dokumen atau konteks].
Pengguna/role: [...]. Scope rilis: [...]. Batasan teknis: [...].
Simpan ke docs/requirements/. Tanyakan keputusan yang belum jelas.
```

```text
Gunakan $prd-srs untuk mereview SRS ini saja tanpa mengubah file.
Periksa konsistensi requirement, permission, data, dan acceptance criteria.
```

Paket lengkap biasanya menghasilkan `PRD.md`, `SRS.md`, `ARCHITECTURE.md`, `WORKFLOWS-AND-ACCESS.md`, `DATABASE-DESIGN.md`, `IMPLEMENTATION-PLAN.md`, dan `TRACEABILITY.md`, ditambah sumber diagram. Struktur menyesuaikan template dan konvensi proyek.

Lihat [contoh perpustakaan sintetis](examples/library/README.md), [ERD](examples/library/diagrams/erd.png), dan [diagram UML use case](examples/library/diagrams/usecases.png). Contoh merupakan proposal dokumentasi, bukan aplikasi yang berjalan atau baseline proyek nyata yang disetujui.

## Validasi dan batas rilis

Ringkasan pengujian tersedia di [QA.md](QA.md). Audit meliputi tiga skenario independen, dua uji interaksi lanjutan, parser/render 19 diagram, dan pemeriksaan keterlacakan/integritas dokumen. Hasil generasi awal mengandung temuan yang kemudian diperbaiki; pengguna tetap perlu menjalankan quality gates pada setiap proyek.

Untuk menjalankan pemeriksaan portable (Python 3.10+):

```sh
python3 -m pip install -r requirements-dev.txt
python3 scripts/validate_skill.py .
python3 tests/check_library_package.py examples/library
python3 -m unittest discover -s tests -p 'test_*.py'
```

Tidak ada API key atau runtime aplikasi yang diperlukan untuk memuat skill. Pemeriksaan developer memakai PyYAML. Rendering diagram membutuhkan renderer Mermaid/PlantUML yang kompatibel; dependency renderer tidak dibundel dalam skill. Source diagram tetap disediakan jika renderer tidak tersedia, dengan batas verifikasi dinyatakan.

Markdown dan diagram SVG/PNG telah diuji. Export/layout DOCX/PDF, automatic discovery global, implementasi aplikasi, SQL/migrasi, performance, restore, deployment, serta UAT tidak dinyatakan telah lulus oleh rilis ini.

## Distribusi

CI memvalidasi skill dan contoh sintetis pada push/PR. Tag `v*` membangun paket ZIP dan menerbitkan GitHub prerelease. Tag harus cocok dengan `VERSION`; release yang sudah ada digunakan kembali dan asset diperbarui secara idempotent.

Lihat [CHANGELOG](CHANGELOG.md). Lisensi belum ditentukan untuk v0.1.0.
