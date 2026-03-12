import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
from components.styles import get_custom_css, get_header_style
from components.charts import render_dashboard_js

# 1. INITIAL SETUP
st.set_page_config(
    page_title="Strategic Vendor Selection System", 
    layout="wide"
)
st.markdown(get_custom_css(), unsafe_allow_html=True)

@st.cache_data
def load_and_clean_data():
    try:
        saw = pd.read_csv("data/saw_results.csv")
        topsis = pd.read_csv("data/topsis_results.csv")
        raw = pd.read_csv("data/supplier_data.csv")
        
        # Bersihkan Nama Kolom
        for d in [saw, topsis, raw]: d.columns = d.columns.str.strip()

        def ultra_clean_price(val):
            s = str(val).replace('$', '').strip()
            try: return float(s)
            except: return 0.0

        # Normalisasi Keys untuk Merge
        raw['Supplier_Key'] = raw['Supplier_Name'].astype(str).str.strip().str.lower()
        saw['Supplier_Key'] = saw['Supplier_Name'].astype(str).str.strip().str.lower()
        topsis['Supplier_Key'] = topsis['Supplier_Name'].astype(str).str.strip().str.lower()

        # Mapping Data dari Raw ke Hasil Skor
        price_map = dict(zip(raw['Supplier_Key'], raw['Unit_Price'].apply(ultra_clean_price)))
        cat_map = dict(zip(raw['Supplier_Key'], raw['Catagory'].str.strip()))
        prod_map = dict(zip(raw['Supplier_Key'], raw['Product_Name'].str.strip()))
        stock_map = dict(zip(raw['Supplier_Key'], raw['Stock_Quantity']))
        turn_map = dict(zip(raw['Supplier_Key'], raw['Inventory_Turnover_Rate']))

        # Gabungkan SAW dan TOPSIS
        df_final = pd.merge(saw, topsis[['Supplier_Key', 'Skor_TOPSIS']], on='Supplier_Key', how='inner')
        
        # Inject data pendukung
        df_final['Unit_Price'] = df_final['Supplier_Key'].map(price_map).fillna(0.0)
        df_final['Catagory'] = df_final['Supplier_Key'].map(cat_map).fillna("Uncategorized")
        df_final['Product_Name'] = df_final['Supplier_Key'].map(prod_map).fillna("Unknown Product")
        df_final['Stock_Quantity'] = df_final['Supplier_Key'].map(stock_map).fillna(0)
        df_final['Inventory_Turnover_Rate'] = df_final['Supplier_Key'].map(turn_map).fillna(0)

        return df_final
    except Exception as e:
        st.error(f"Error pada pemuatan data: {e}")
        return pd.DataFrame()

df_all = load_and_clean_data()

# 2. SIDEBAR FILTER
st.sidebar.header("🔍 Strategic Filters")
cat_list = ["Semua Kategori"] + sorted(list(df_all['Catagory'].unique()))
selected_cat = st.sidebar.selectbox("Pilih Kategori:", cat_list)
df_cat = df_all if selected_cat == "Semua Kategori" else df_all[df_all['Catagory'] == selected_cat]

prod_list = ["Semua Produk"] + sorted(list(df_cat['Product_Name'].unique()))
selected_prod = st.sidebar.selectbox("Spesifikasi Produk:", prod_list)
w_saw = st.sidebar.slider("Bobot Metode SAW (%)", 0, 100, 50) / 100

# Perhitungan Final Score
df_f = df_cat if selected_prod == "Semua Produk" else df_cat[df_cat['Product_Name'] == selected_prod]
df_f['Final_Score'] = (df_f['Skor_SAW'] * w_saw) + (df_f['Skor_TOPSIS'] * (1 - w_saw))
df_f = df_f.sort_values("Final_Score", ascending=False)

# 3. HEADER SECTION
st.markdown(get_header_style(
    "INTEGRATED SUPPLIER STRATEGIC DECISION SUPPORT SYSTEM", 
    f"Hybrid Multi-Criteria Analysis (SAW & TOPSIS) | Unit: {selected_prod}"
), unsafe_allow_html=True)

if not df_f.empty:
    top_1 = df_f.iloc[0]
    top_2 = df_f.iloc[1] if len(df_f) > 1 else None
    top_3 = df_f.iloc[2] if len(df_f) > 2 else None

    # 4. TOP RECOMMENDATION CARDS
    c_main, c_backup = st.columns([1.8, 1.2])
    with c_main:
        st.markdown(f"""
            <div class="glow-card">
                <div class="glow-label">⭐ REKOMENDASI UTAMA</div>
                <div class="glow-name">✨ {top_1['Supplier_Name']} ✨</div>
                <div class="glow-score">Total Weighted Score: {top_1['Final_Score']:.4f}</div>
                <hr style="border:0.5px solid #30363d; margin: 15px 0;">
                <p style="color: #8b949e; font-size: 13px; line-height: 1.5;">
                    Supplier ini diidentifikasi sebagai mitra paling optimal berdasarkan perimbangan efisiensi biaya, 
                    kapasitas inventaris, dan stabilitas pasokan.
                </p>
            </div>
        """, unsafe_allow_html=True)

    with c_backup:
        st.markdown('<div style="color:#58a6ff; font-weight:bold; font-size:11px; margin-bottom:10px; letter-spacing:1px;">🥈 STRATEGI MITIGASI (CADANGAN)</div>', unsafe_allow_html=True)
        for i, row in enumerate([top_2, top_3], 2):
            if row is not None:
                st.markdown(f"""
                    <div class="backup-card">
                        <div class="rank-label">PERINGKAT {i}</div>
                        <div class="vendor-name">{row['Supplier_Name']}</div>
                        <span class="score-badge">Skor: {row['Final_Score']:.4f}</span>
                    </div>
                """, unsafe_allow_html=True)

    # 5. KEY PERFORMANCE METRICS
    st.markdown("---")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Indeks TOPSIS", f"{top_1['Skor_TOPSIS']:.4f}")
    m2.metric("Estimasi Harga", f"${float(top_1['Unit_Price']):,.2f}")
    m3.metric("Volume Stok", f"{int(top_1['Stock_Quantity'])}")
    m4.metric("Total Vendor", f"{len(df_f)}")

    # 6. VISUALIZATION (Distribusi & Radar)
    risk_data = {
        "Aman": int(len(df_f[df_f['Skor_TOPSIS'] > 0.7])),
        "Waspada": int(len(df_f[(df_f['Skor_TOPSIS'] <= 0.7) & (df_f['Skor_TOPSIS'] >= 0.4)])),
        "Bahaya": int(len(df_f[df_f['Skor_TOPSIS'] < 0.4]))
    }
    avg_m = [
        float(df_f['Unit_Price'].mean()), 
        float(df_f['Stock_Quantity'].mean()), 
        float(df_f['Inventory_Turnover_Rate'].mean())
    ]
    json_recs = df_f.head(10).to_json(orient='records')
    components.html(render_dashboard_js(json_recs, risk_data, avg_m), height=450)

    # 7. ANALISIS DESKRIPTIF
    st.subheader("💡 Deskripsi Analisis Bisnis")
    st.markdown(f"""
    Berdasarkan pengolahan data menggunakan metode hibrida **SAW** dan **TOPSIS**, sistem menetapkan **{top_1['Supplier_Name']}** sebagai mitra pengadaan prioritas. 
    Kualitas pemilihan ini didasarkan pada perimbangan bobot kriteria harga (cost) dan performa operasional (benefit). 
    Penyediaan opsi cadangan seperti **{top_2['Supplier_Name'] if top_2 is not None else '-'}** bertujuan untuk menjaga ketahanan rantai pasok terhadap potensi kendala di masa mendatang.
    """)

    # 8. DATA TABLE
    st.subheader("📋 Matriks Detail Perhitungan")
    st.dataframe(df_f[['Supplier_Name', 'Product_Name', 'Catagory', 'Unit_Price', 'Final_Score']], use_container_width=True)

else:
    st.warning("Data tidak tersedia untuk filter tersebut.")

st.download_button("📥 Ekspor Laporan Strategis", df_f.to_csv(index=False).encode('utf-8'), "Laporan_SPK_Supplier.csv", "text/csv")