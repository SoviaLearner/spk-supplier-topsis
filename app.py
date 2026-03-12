import streamlit as st  
import pandas as pd
import plotly.express as px
import numpy as np
import os

# ==========================================
# 1. KONFIGURASI HALAMAN
# ==========================================
st.set_page_config(page_title="Supplier Intelligence DSS", page_icon="🏢", layout="wide")

# ==========================================
# 2. FUNGSI CACHE & PREPROCESSING DATA
# ==========================================
@st.cache_data
def load_data():
    df = pd.read_csv(r'data\supplier_data.csv')
    
    df['Status'] = df['Status'].astype(str).str.strip()
    df['Catagory'] = df['Catagory'].astype(str).str.strip()
    df['Product_Name'] = df['Product_Name'].astype(str).str.strip()
    df['Supplier_Name'] = df['Supplier_Name'].astype(str).str.strip()
    
    df['Unit_Price'] = df['Unit_Price'].astype(str).str.replace('$', '', regex=False).str.replace(',', '', regex=False).astype(float)
    df['Date_Received'] = pd.to_datetime(df['Date_Received'], errors='coerce')
    df['Expiration_Date'] = pd.to_datetime(df['Expiration_Date'], errors='coerce')
    
    df['Shelf_Life_Days'] = (df['Expiration_Date'] - df['Date_Received']).dt.days
    df['Turnover_Rate'] = df['Inventory_Turnover_Rate'].astype(float)
    
    return df

df = load_data()

def min_max_benefit(col):
    return (col - col.min()) / (col.max() - col.min()) if col.max() != col.min() else 1.0

def min_max_cost(col):
    return (col.max() - col) / (col.max() - col.min()) if col.max() != col.min() else 1.0

# ==========================================
# 3. SIDEBAR
# ==========================================
st.sidebar.title("Control Panel")
menu = st.sidebar.radio("Pilih Mode Analisis:", 
    ["1. Evaluasi Aktif", "2. Audit Post-Mortem", "3. Eksplorasi Data Mentah"])

st.sidebar.markdown("---")
st.sidebar.subheader("Simulator Bobot Kriteria")

w_price = st.sidebar.number_input("Bobot Harga (Cost) %",0,100,30)
w_turnover = st.sidebar.number_input("Bobot Kecepatan Laku (Benefit) %",0,100,20)
w_shelf = st.sidebar.number_input("Bobot Kesegaran/Umur (Benefit) %",0,100,50)

total_weight = w_price + w_turnover + w_shelf

if total_weight != 100:
    st.sidebar.error(f"Total bobot {total_weight}%. Harus 100%")
    st.stop()

w_price,w_turnover,w_shelf = w_price/100,w_turnover/100,w_shelf/100

# ==========================================
# 4. HALAMAN EVALUASI
# ==========================================
if menu == "1. Evaluasi Aktif":

    st.title("Analisa Pengadaan Barang Aktif")

    df_active = df[df['Status'].isin(['Active','Backordered'])].copy()

    eval_level = st.radio("Level Evaluasi:",
        ["Per Produk Spesifik","Keseluruhan Kategori (Global)"],horizontal=True)

    col1,col2 = st.columns(2)

    with col1:
        selected_cat = st.selectbox("Pilih Kategori",
            df_active['Catagory'].dropna().unique())

    if eval_level == "Per Produk Spesifik":

        with col2:
            products = df_active[df_active['Catagory']==selected_cat]['Product_Name'].unique()
            selected_prod = st.selectbox("Pilih Produk",products)

        df_eval = df_active[
            (df_active['Catagory']==selected_cat) &
            (df_active['Product_Name']==selected_prod)
        ]

        target_name = selected_prod

    else:

        df_eval = df_active[df_active['Catagory']==selected_cat]
        target_name = f"Kategori {selected_cat}"

    if df_eval['Supplier_Name'].nunique() < 2:

        st.warning("Supplier tidak cukup untuk evaluasi")

    else:

        grouped = df_eval.groupby('Supplier_Name').agg({
            'Unit_Price':'mean',
            'Turnover_Rate':'mean',
            'Shelf_Life_Days':'mean'
        }).reset_index()

        # NORMALISASI
        grouped['Norm_Price'] = min_max_cost(grouped['Unit_Price'])
        grouped['Norm_Turnover'] = min_max_benefit(grouped['Turnover_Rate'])
        grouped['Norm_Shelf'] = min_max_benefit(grouped['Shelf_Life_Days'])

        # SAW
        grouped['Skor_SAW'] = (
            grouped['Norm_Price']*w_price +
            grouped['Norm_Turnover']*w_turnover +
            grouped['Norm_Shelf']*w_shelf
        )

        # TOPSIS
        grouped['V_Price'] = grouped['Norm_Price']*w_price
        grouped['V_Turnover'] = grouped['Norm_Turnover']*w_turnover
        grouped['V_Shelf'] = grouped['Norm_Shelf']*w_shelf

        A_plus = np.array([w_price,w_turnover,w_shelf])
        A_minus = np.array([0,0,0])

        def dplus(r):
            return np.sqrt(
                (r['V_Price']-A_plus[0])**2+
                (r['V_Turnover']-A_plus[1])**2+
                (r['V_Shelf']-A_plus[2])**2
            )

        def dminus(r):
            return np.sqrt(
                (r['V_Price']-A_minus[0])**2+
                (r['V_Turnover']-A_minus[1])**2+
                (r['V_Shelf']-A_minus[2])**2
            )

        grouped['D_Plus'] = grouped.apply(dplus,axis=1)
        grouped['D_Minus'] = grouped.apply(dminus,axis=1)

        grouped['Skor_TOPSIS'] = grouped['D_Minus'] / (grouped['D_Plus']+grouped['D_Minus'])

        # MATRIX
        normalized_matrix = grouped[['Supplier_Name','Norm_Price','Norm_Turnover','Norm_Shelf']]
        weighted_matrix = grouped[['Supplier_Name','V_Price','V_Turnover','V_Shelf']]

        saw_results = grouped[['Supplier_Name','Unit_Price','Turnover_Rate','Shelf_Life_Days','Skor_SAW']]
        topsis_results = grouped[['Supplier_Name','Unit_Price','Turnover_Rate','Shelf_Life_Days','D_Plus','D_Minus','Skor_TOPSIS']]

        # DOWNLOAD
        st.markdown("### Download Hasil DSS")

        c1,c2,c3,c4 = st.columns(4)

        with c1:
            st.download_button("Download Normalized Matrix",
                normalized_matrix.to_csv(index=False),
                "normalized_matrix.csv",
                "text/csv")

        with c2:
            st.download_button("Download Weighted Matrix",
                weighted_matrix.to_csv(index=False),
                "weighted_matrix.csv",
                "text/csv")

        with c3:
            st.download_button("Download SAW Results",
                saw_results.to_csv(index=False),
                "saw_results.csv",
                "text/csv")

        with c4:
            st.download_button("Download TOPSIS Results",
                topsis_results.to_csv(index=False),
                "topsis_results.csv",
                "text/csv")

        # VISUALISASI
        selected_method = st.radio("Metode Grafik",
            ["TOPSIS","SAW"],horizontal=True)

        score_col = "Skor_TOPSIS" if selected_method=="TOPSIS" else "Skor_SAW"

        grouped = grouped.sort_values(score_col,ascending=False)

        top_supplier = grouped.iloc[0]

        st.subheader(f"Rekomendasi Supplier: {top_supplier['Supplier_Name']}")

        fig = px.bar(
            grouped,
            x="Supplier_Name",
            y=score_col,
            color=score_col,
            color_continuous_scale="plasma",
            title=f"Peringkat Supplier ({selected_method})"
        )

        st.plotly_chart(fig,use_container_width=True)

        # ==================================
        # TABEL RANKING DI BAWAH CHART
        # ==================================
        st.markdown("### Tabel Ranking Supplier")

        base_cols = ['Supplier_Name','Unit_Price','Turnover_Rate','Shelf_Life_Days']
        display_cols = base_cols + [score_col]

        rename_dict = {
            'Supplier_Name':'Nama Pemasok',
            'Unit_Price':'Harga Satuan',
            'Turnover_Rate':'Kecepatan Laku',
            'Shelf_Life_Days':'Umur Simpan',
            'Skor_SAW':'Skor Akhir (SAW)',
            'Skor_TOPSIS':'Skor Akhir (TOPSIS)'
        }

        df_display = grouped[display_cols].rename(columns=rename_dict)

        score_display = rename_dict[score_col]

        format_dict = {
            'Harga Satuan':'${:.2f}',
            'Kecepatan Laku':'{:.2f}',
            'Umur Simpan':'{:.0f} Hari',
            score_display:'{:.3f}'
        }

        st.dataframe(
            df_display.style.format(format_dict),
            use_container_width=True
        )

# ==========================================
# 5. HALAMAN AUDIT
# ==========================================
elif menu == "2. Audit Post-Mortem":

    st.title("Audit Supplier Discontinued")

    df_disc = df[df['Status']=="Discontinued"]

    df_disc['Red_Flag'] = df_disc['Shelf_Life_Days'] < 0

    st.dataframe(df_disc)

# ==========================================
# 6. RAW DATA
# ==========================================
else:

    st.title("Eksplorasi Data Mentah")

    col1,col2,col3 = st.columns(3)

    col1.metric("Total Transaksi",len(df))
    col2.metric("Total Supplier",df['Supplier_Name'].nunique())
    col3.metric("Total Produk",df['Product_Name'].nunique())

    search = st.text_input("Cari Supplier / Produk")

    if search:
        st.dataframe(
            df[
                df['Supplier_Name'].str.contains(search,case=False) |
                df['Product_Name'].str.contains(search,case=False)
            ]
        )
    else:
        st.dataframe(df)