# Integrated Supplier Strategic Decision Support System

**Tugas Mata Kuliah: Analisa Bisnis**  
Politeknik Elektronika Negeri Surabaya (PENS)

## Link Deploy

- Supplier Procurement Analysis: https://supplier-procurement-analysis.streamlit.app/
- Strategic Supplier TOPSIS Dashboard: https://spk-supplier-topsis.streamlit.app/

## Deskripsi Proyek

Proyek ini adalah sistem pendukung keputusan berbasis web untuk membantu proses pemilihan supplier secara lebih objektif dan berbasis data.

Dalam kegiatan procurement, supplier tidak cukup dinilai dari harga termurah saja. Keputusan pengadaan juga perlu mempertimbangkan ketersediaan stok, kecepatan perputaran barang, umur simpan, dan stabilitas performa operasional. Karena itu, sistem ini membandingkan supplier menggunakan pendekatan Multi-Criteria Decision Making (MCDM).

Versi terbaru aplikasi sudah dipoles dengan tampilan yang lebih modern dan konsisten, termasuk mode **Light** dan **Dark**, kartu rekomendasi supplier, visualisasi interaktif, tabel ranking, export laporan, serta bagian **Business Understanding** di frontend.

## Business Understanding

### Masalah Bisnis

Pemilihan supplier yang hanya mengandalkan intuisi atau harga satuan dapat menimbulkan risiko, seperti stok tidak aman, produk lambat berputar, barang mendekati kedaluwarsa, dan biaya pengadaan yang tidak optimal.

### Tujuan Analisis

Sistem ini membantu menentukan supplier prioritas dan supplier cadangan berdasarkan kriteria yang terukur. Hasil ranking digunakan sebagai dasar rekomendasi pengadaan yang lebih transparan dan dapat dipertanggungjawabkan.

### Nilai Bisnis

Dashboard membantu tim procurement untuk:

- memilih supplier secara lebih objektif;
- membandingkan supplier berdasarkan beberapa kriteria;
- mengurangi risiko keputusan yang bias;
- menjaga ketersediaan stok;
- mendukung evaluasi vendor secara cepat dan konsisten.

## Aplikasi

### 1. Supplier Procurement Analysis (`app.py`)

Aplikasi ini digunakan untuk evaluasi supplier aktif dan eksplorasi data mentah. Fitur utamanya:

- evaluasi supplier aktif dan backordered;
- simulasi bobot kriteria harga, turnover, dan umur simpan;
- perhitungan SAW dan TOPSIS secara langsung;
- rekomendasi supplier terbaik berdasarkan filter produk atau kategori;
- audit post-mortem untuk supplier discontinued;
- download normalized matrix, weighted matrix, SAW results, dan TOPSIS results;
- mode Light dan Dark.

### 2. Strategic Supplier TOPSIS Dashboard (`dashboard.py`)

Aplikasi ini digunakan untuk dashboard strategis hasil integrasi SAW dan TOPSIS. Fitur utamanya:

- filter kategori dan produk;
- pengaturan bobot metode SAW terhadap TOPSIS;
- ranking supplier berdasarkan final weighted score;
- kartu rekomendasi utama dan supplier cadangan;
- metrik kinerja supplier;
- visualisasi scatter, radar, dan distribusi risiko;
- export laporan strategis;
- bagian Business Understanding;
- mode Light dan Dark.

## Metode yang Digunakan

Sistem menggunakan pendekatan **Multi-Criteria Decision Making (MCDM)** dengan dua metode utama: **SAW** dan **TOPSIS**.

### SAW (Simple Additive Weighting)

SAW menghitung skor supplier dengan cara menormalisasi setiap kriteria, mengalikan nilai normalisasi dengan bobot, lalu menjumlahkan seluruh nilai.

Rumus:

```text
Vi = sum(wj * rij)
```

Keterangan:

- `Vi` = skor akhir supplier;
- `wj` = bobot kriteria;
- `rij` = nilai hasil normalisasi.

Supplier dengan nilai `Vi` terbesar dianggap memiliki performa terbaik.

### TOPSIS (Technique for Order Preference by Similarity to Ideal Solution)

TOPSIS menentukan supplier terbaik berdasarkan kedekatan terhadap solusi ideal positif dan jarak dari solusi ideal negatif.

Rumus:

```text
Ci = D- / (D+ + D-)
```

Keterangan:

- `D+` = jarak ke solusi ideal positif;
- `D-` = jarak ke solusi ideal negatif;
- `Ci` = nilai kedekatan supplier terhadap solusi ideal.

Supplier dengan nilai `Ci` terbesar menjadi alternatif terbaik.

## Kriteria Penilaian Supplier

| Kriteria | Tipe | Penjelasan |
| --- | --- | --- |
| Unit Price | Cost | Harga produk dari supplier. Semakin rendah semakin baik. |
| Stock Quantity | Benefit | Jumlah stok yang tersedia. Semakin tinggi semakin aman. |
| Inventory Turnover Rate | Benefit | Kecepatan perputaran barang. Semakin tinggi semakin baik. |
| Shelf Life Days | Benefit | Umur simpan produk. Semakin panjang semakin baik. |
| SAW & TOPSIS Score | Output | Skor akhir untuk menyusun ranking supplier. |

## Struktur Proyek

```text
Code Program/
├── app.py
├── dashboard.py
├── CodeProgram.ipynb
├── README.md
├── requirements.txt
├── components/
│   ├── __init__.py
│   ├── charts.py
│   └── styles.py
└── data/
    ├── supplier_data.csv
    ├── normalized_matrix.csv
    ├── weighted_matrix.csv
    ├── saw_results.csv
    └── topsis_results.csv
```

## Cara Menjalankan Program

### 1. Install dependency

```bash
pip install -r requirements.txt
```

### 2. Menjalankan Supplier Procurement Analysis

```bash
streamlit run app.py
```

### 3. Menjalankan Strategic Supplier Dashboard

```bash
streamlit run dashboard.py
```

Secara default Streamlit akan membuka aplikasi pada:

```text
http://localhost:8501
```

Jika ingin menjalankan dua aplikasi sekaligus, gunakan port berbeda:

```bash
streamlit run app.py --server.port 8501
streamlit run dashboard.py --server.port 8502
```

## Teknologi

- Python
- Streamlit
- Pandas
- NumPy
- Plotly
- ECharts
- HTML/CSS custom components

## Penulis

**Tim Project Analisa Bisnis**  
Mahasiswa Sains Data Terapan  
Politeknik Elektronika Negeri Surabaya (PENS)

---

Project Analisa Bisnis - PENS
