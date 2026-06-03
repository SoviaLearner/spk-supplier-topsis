import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

from components.charts import render_dashboard_js
from components.styles import get_custom_css, get_header_style


st.set_page_config(
    page_title="Strategic Supplier DSS",
    layout="wide",
)


@st.cache_data
def load_and_clean_data():
    try:
        saw = pd.read_csv("data/saw_results.csv")
        topsis = pd.read_csv("data/topsis_results.csv")
        raw = pd.read_csv("data/supplier_data.csv")

        for dataset in [saw, topsis, raw]:
            dataset.columns = dataset.columns.str.strip()

        def clean_price(value):
            text = str(value).replace("$", "").replace(",", "").strip()
            try:
                return float(text)
            except ValueError:
                return 0.0

        raw["Supplier_Key"] = raw["Supplier_Name"].astype(str).str.strip().str.lower()
        saw["Supplier_Key"] = saw["Supplier_Name"].astype(str).str.strip().str.lower()
        topsis["Supplier_Key"] = topsis["Supplier_Name"].astype(str).str.strip().str.lower()

        price_map = dict(zip(raw["Supplier_Key"], raw["Unit_Price"].apply(clean_price)))
        cat_map = dict(zip(raw["Supplier_Key"], raw["Catagory"].astype(str).str.strip()))
        prod_map = dict(zip(raw["Supplier_Key"], raw["Product_Name"].astype(str).str.strip()))
        stock_map = dict(zip(raw["Supplier_Key"], raw["Stock_Quantity"]))
        turn_map = dict(zip(raw["Supplier_Key"], raw["Inventory_Turnover_Rate"]))

        df_final = pd.merge(
            saw,
            topsis[["Supplier_Key", "Skor_TOPSIS"]],
            on="Supplier_Key",
            how="inner",
        )

        df_final["Unit_Price"] = df_final["Supplier_Key"].map(price_map).fillna(0.0)
        df_final["Catagory"] = df_final["Supplier_Key"].map(cat_map).fillna("Uncategorized")
        df_final["Product_Name"] = df_final["Supplier_Key"].map(prod_map).fillna("Unknown Product")
        df_final["Stock_Quantity"] = df_final["Supplier_Key"].map(stock_map).fillna(0)
        df_final["Inventory_Turnover_Rate"] = df_final["Supplier_Key"].map(turn_map).fillna(0)

        return df_final
    except Exception as exc:
        st.error(f"Error pada pemuatan data: {exc}")
        return pd.DataFrame()


def render_business_understanding():
    st.markdown("### Business Understanding")
    st.markdown(
        """
        <div class="insight-card">
            <p>
                Proses pengadaan membutuhkan keputusan yang konsisten karena supplier tidak hanya
                dinilai dari harga termurah. Tim bisnis juga perlu mempertimbangkan ketersediaan stok,
                kecepatan perputaran barang, dan kestabilan performa agar risiko keterlambatan,
                overstock, dan biaya pembelian yang tidak efisien bisa dikurangi.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="business-grid">
            <div class="backup-card">
                <div class="rank-label">Masalah Bisnis</div>
                <div class="business-title">Pemilihan supplier belum objektif</div>
                <div class="small-muted">
                    Supplier perlu dibandingkan dengan kriteria yang sama agar keputusan tidak hanya
                    berdasarkan intuisi atau harga satuan.
                </div>
            </div>
            <div class="backup-card">
                <div class="rank-label">Tujuan Analisis</div>
                <div class="business-title">Menentukan prioritas vendor</div>
                <div class="small-muted">
                    SAW dan TOPSIS digunakan untuk menghasilkan ranking supplier utama serta
                    alternatif cadangan yang dapat dipertanggungjawabkan.
                </div>
            </div>
            <div class="backup-card">
                <div class="rank-label">Dampak Keputusan</div>
                <div class="business-title">Pengadaan lebih terkendali</div>
                <div class="small-muted">
                    Rekomendasi membantu menekan biaya, menjaga stok, dan mempercepat evaluasi
                    supplier untuk kebutuhan pembelian berikutnya.
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### Kerangka Keputusan")
    criteria = pd.DataFrame(
        [
            ["Unit Price", "Cost", "Semakin rendah harga, semakin baik nilai supplier."],
            ["Stock Quantity", "Benefit", "Semakin tinggi stok, semakin aman untuk kebutuhan pasokan."],
            ["Inventory Turnover Rate", "Benefit", "Semakin cepat perputaran, semakin baik performa operasional."],
            ["SAW & TOPSIS Score", "Decision Output", "Skor akhir digunakan untuk menyusun ranking supplier."],
        ],
        columns=["Kriteria", "Tipe", "Makna Bisnis"],
    )
    st.dataframe(criteria, use_container_width=True, hide_index=True)


df_all = load_and_clean_data()

if "theme_mode" not in st.session_state:
    st.session_state.theme_mode = "Dark"

with st.sidebar:
    st.markdown("## Supplier DSS")
    theme_mode = st.radio("Mode tampilan", ["Light", "Dark"], horizontal=True, key="theme_mode")
    st.markdown("---")
    st.markdown("### Strategic Filters")

st.markdown(get_custom_css(theme_mode), unsafe_allow_html=True)

if df_all.empty:
    st.warning("Data tidak tersedia. Pastikan file CSV pada folder data sudah lengkap.")
    st.stop()

with st.sidebar:
    cat_list = ["Semua Kategori"] + sorted(df_all["Catagory"].dropna().unique().tolist())
    selected_cat = st.selectbox("Kategori", cat_list)

    df_cat = df_all if selected_cat == "Semua Kategori" else df_all[df_all["Catagory"] == selected_cat]

    prod_list = ["Semua Produk"] + sorted(df_cat["Product_Name"].dropna().unique().tolist())
    selected_prod = st.selectbox("Produk", prod_list)
    w_saw = st.slider("Bobot Metode SAW (%)", 0, 100, 50) / 100
    st.caption("Sisa bobot otomatis digunakan untuk TOPSIS.")

df_f = df_cat if selected_prod == "Semua Produk" else df_cat[df_cat["Product_Name"] == selected_prod]
df_f = df_f.copy()
df_f["Final_Score"] = (df_f["Skor_SAW"] * w_saw) + (df_f["Skor_TOPSIS"] * (1 - w_saw))
df_f = df_f.sort_values("Final_Score", ascending=False)

st.markdown(
    get_header_style(
        "Strategic Supplier Decision Support System",
        f"Analisis hibrida SAW dan TOPSIS untuk rekomendasi supplier pada filter: {selected_prod}.",
        theme_mode,
        "Supplier Procurement Analysis",
    ),
    unsafe_allow_html=True,
)

if not df_f.empty:
    top_1 = df_f.iloc[0]
    top_2 = df_f.iloc[1] if len(df_f) > 1 else None
    top_3 = df_f.iloc[2] if len(df_f) > 2 else None

    c_main, c_backup = st.columns([1.8, 1.2])
    with c_main:
        st.markdown(
            f"""
            <div class="recommendation-card">
                <div class="recommendation-label">Rekomendasi Utama</div>
                <div class="recommendation-name">{top_1['Supplier_Name']}</div>
                <div class="recommendation-score">Total Weighted Score: {top_1['Final_Score']:.4f}</div>
                <div class="recommendation-copy">
                    Supplier ini menjadi opsi paling optimal berdasarkan kombinasi skor SAW dan TOPSIS,
                    dengan mempertimbangkan efisiensi biaya, kapasitas stok, dan performa operasional.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c_backup:
        st.markdown('<div class="section-label">Strategi Mitigasi</div>', unsafe_allow_html=True)
        for rank, row in [(2, top_2), (3, top_3)]:
            if row is not None:
                st.markdown(
                    f"""
                    <div class="backup-card">
                        <div class="rank-label">Peringkat {rank}</div>
                        <div class="vendor-name">{row['Supplier_Name']}</div>
                        <span class="score-badge">Skor: {row['Final_Score']:.4f}</span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    st.markdown("### Ringkasan Kinerja")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Indeks TOPSIS", f"{top_1['Skor_TOPSIS']:.4f}")
    m2.metric("Estimasi Harga", f"${float(top_1['Unit_Price']):,.2f}")
    m3.metric("Volume Stok", f"{int(top_1['Stock_Quantity']):,}")
    m4.metric("Total Vendor", f"{len(df_f):,}")

    risk_data = {
        "Aman": int(len(df_f[df_f["Skor_TOPSIS"] > 0.7])),
        "Waspada": int(len(df_f[(df_f["Skor_TOPSIS"] <= 0.7) & (df_f["Skor_TOPSIS"] >= 0.4)])),
        "Bahaya": int(len(df_f[df_f["Skor_TOPSIS"] < 0.4])),
    }
    avg_m = [
        float(df_f["Unit_Price"].mean()),
        float(df_f["Stock_Quantity"].mean()),
        float(df_f["Inventory_Turnover_Rate"].mean()),
    ]
    json_recs = df_f.head(10).to_json(orient="records")
    components.html(render_dashboard_js(json_recs, risk_data, avg_m, theme_mode), height=450)

    st.markdown("### Deskripsi Analisis Bisnis")
    st.markdown(
        f"""
        <div class="insight-card">
            <p>
                Berdasarkan pengolahan data menggunakan metode hibrida SAW dan TOPSIS,
                sistem menetapkan <strong>{top_1['Supplier_Name']}</strong> sebagai mitra pengadaan prioritas.
                Opsi cadangan seperti <strong>{top_2['Supplier_Name'] if top_2 is not None else '-'}</strong>
                membantu menjaga ketahanan rantai pasok ketika supplier utama memiliki kendala operasional.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### Matriks Detail Perhitungan")
    table_cols = ["Supplier_Name", "Product_Name", "Catagory", "Unit_Price", "Skor_SAW", "Skor_TOPSIS", "Final_Score"]
    st.dataframe(
        df_f[table_cols].rename(
            columns={
                "Supplier_Name": "Supplier",
                "Product_Name": "Produk",
                "Catagory": "Kategori",
                "Unit_Price": "Harga",
                "Skor_SAW": "SAW",
                "Skor_TOPSIS": "TOPSIS",
                "Final_Score": "Skor Final",
            }
        ),
        use_container_width=True,
        hide_index=True,
    )

    st.download_button(
        "Ekspor Laporan Strategis",
        df_f.to_csv(index=False).encode("utf-8"),
        "Laporan_SPK_Supplier.csv",
        "text/csv",
    )

    render_business_understanding()
else:
    st.warning("Data tidak tersedia untuk filter tersebut.")
