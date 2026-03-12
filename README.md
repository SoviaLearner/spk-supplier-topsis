# Integrated Supplier Strategic Decision Support System (IS-SDSS) 🚀

**Tugas Mata Kuliah: Analisa Bisnis**
Politeknik Elektronika Negeri Surabaya (PENS)

---

# Deskripsi Proyek

Proyek ini adalah **sistem pendukung keputusan berbasis web** untuk membantu proses pemilihan supplier secara lebih objektif dan berbasis data.

Dalam kegiatan pengadaan, memilih supplier tidak hanya melihat **harga**, tetapi juga perlu mempertimbangkan **ketersediaan stok** dan **performa operasional**. Oleh karena itu, sistem ini dibuat untuk membantu membandingkan beberapa supplier berdasarkan beberapa kriteria sekaligus.

Hasil analisis ditampilkan dalam bentuk **dashboard interaktif** sehingga pengguna dapat melihat peringkat supplier serta memahami alasan di balik rekomendasi yang diberikan.

---

# Metode yang Digunakan

Sistem ini menggunakan pendekatan **Multi-Criteria Decision Making (MCDM)** dengan dua metode, yaitu **SAW** dan **TOPSIS**.

## 1. SAW (Simple Additive Weighting)

Metode **SAW** digunakan untuk menghitung skor supplier berdasarkan bobot setiap kriteria.

Langkah dasarnya:

1. Menormalisasi nilai setiap kriteria
2. Mengalikan nilai dengan bobot kriteria
3. Menjumlahkan seluruh nilai untuk mendapatkan skor akhir

Rumus SAW:

```
Vi = Σ (wj × rij)
```

Keterangan:

* **Vi** = skor akhir supplier
* **wj** = bobot kriteria
* **rij** = nilai hasil normalisasi

Supplier dengan nilai **Vi terbesar** dianggap memiliki performa terbaik.

---

## 2. TOPSIS (Technique for Order Preference by Similarity to Ideal Solution)

Metode **TOPSIS** menentukan supplier terbaik berdasarkan kedekatan dengan solusi ideal.

Prinsipnya:

* Supplier terbaik harus **paling dekat dengan solusi ideal positif**
* dan **paling jauh dari solusi ideal negatif**

Nilai kedekatan dihitung dengan rumus:

```
Ci = D- / (D+ + D-)
```

Keterangan:

* **D+** = jarak ke solusi ideal positif
* **D-** = jarak ke solusi ideal negatif
* **Ci** = nilai kedekatan

Supplier dengan **nilai Ci paling besar** menjadi pilihan terbaik.

---

# Dashboard Analisis

Aplikasi ini menampilkan hasil analisis dalam bentuk **dashboard interaktif** yang berisi:

* Ranking supplier menggunakan metode **SAW**
* Ranking supplier menggunakan metode **TOPSIS**
* Visualisasi perbandingan performa supplier
* Highlight **supplier terbaik**
* Grafik analisis keputusan

Dashboard dibuat menggunakan **Streamlit** sehingga dapat dijalankan langsung melalui browser.

---

# Struktur Proyek

Berikut struktur folder dalam proyek ini:

```
CODE PROGRAM
│
├── components
│   ├── charts.py
│   ├── styles.py
│   └── __init__.py
│
├── data
│   ├── supplier_data.csv
│   ├── normalized_matrix.csv
│   ├── weighted_matrix.csv
│   ├── saw_results.csv
│   └── topsis_results.csv
│
├── dashboard.py
├── app.py
├── CodeProgram.ipynb
├── requirements.txt
└── README.md
```

---

# Cara Menjalankan Program

## 1. Install Library

Buka terminal pada folder proyek, lalu jalankan:

```
pip install -r requirements.txt
```

## 2. Menjalankan Dashboard

Jalankan perintah berikut:

```
streamlit run dashboard.py
```

Setelah itu aplikasi akan terbuka di browser pada alamat:

```
http://localhost:8501
```

---

# Kriteria Penilaian Supplier

Supplier dievaluasi berdasarkan tiga kriteria utama:

| Kriteria                | Tipe    | Penjelasan                  |
| ----------------------- | ------- | --------------------------- |
| Unit Price              | Cost    | Harga produk dari supplier  |
| Stock Quantity          | Benefit | Jumlah stok yang tersedia   |
| Inventory Turnover Rate | Benefit | Kecepatan perputaran barang |

---

# Tujuan Proyek

Proyek ini dibuat untuk membantu:

* memilih supplier secara **lebih objektif**
* membandingkan supplier berdasarkan **beberapa kriteria**
* mendukung **pengambilan keputusan pengadaan**
* menampilkan hasil analisis dalam bentuk **dashboard yang mudah dipahami**

---

# Penulis

**TIM**
Mahasiswa Sains Data Terapan
Politeknik Elektronika Negeri Surabaya (PENS)

---

© Project Analisa Bisnis – PENS
