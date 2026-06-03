import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

from components.styles import get_custom_css, get_header_style, get_theme


st.set_page_config(page_title="Supplier Intelligence DSS", layout="wide")


@st.cache_data
def load_data():
    df = pd.read_csv("data/supplier_data.csv")

    for column in ["Status", "Catagory", "Product_Name", "Supplier_Name"]:
        df[column] = df[column].astype(str).str.strip()

    df["Unit_Price"] = (
        df["Unit_Price"]
        .astype(str)
        .str.replace("$", "", regex=False)
        .str.replace(",", "", regex=False)
        .astype(float)
    )
    df["Date_Received"] = pd.to_datetime(df["Date_Received"], errors="coerce")
    df["Expiration_Date"] = pd.to_datetime(df["Expiration_Date"], errors="coerce")
    df["Shelf_Life_Days"] = (df["Expiration_Date"] - df["Date_Received"]).dt.days
    df["Turnover_Rate"] = df["Inventory_Turnover_Rate"].astype(float)

    return df


def min_max_benefit(column):
    return (column - column.min()) / (column.max() - column.min()) if column.max() != column.min() else 1.0


def min_max_cost(column):
    return (column.max() - column) / (column.max() - column.min()) if column.max() != column.min() else 1.0


def apply_plotly_theme(fig, mode):
    theme = get_theme(mode)
    fig.update_layout(
        template="plotly_dark" if mode == "Dark" else "plotly_white",
        paper_bgcolor=theme["surface"],
        plot_bgcolor=theme["surface"],
        font_color=theme["text"],
        title_font_color=theme["text"],
        margin=dict(l=20, r=20, t=60, b=20),
        coloraxis_colorbar=dict(title="Skor"),
    )
    fig.update_xaxes(gridcolor=theme["border"], zerolinecolor=theme["border"])
    fig.update_yaxes(gridcolor=theme["border"], zerolinecolor=theme["border"])
    return fig


def render_business_understanding():
    st.markdown("### Business Understanding")
    st.markdown(
        """
        <div class="insight-card">
            <p>
                Analisis ini membantu proses procurement memilih supplier secara objektif.
                Keputusan pengadaan tidak cukup hanya melihat harga, karena supplier juga perlu
                dinilai dari kecepatan perputaran barang dan umur simpan produk agar pembelian
                lebih efisien, stok lebih aman, dan risiko barang tidak layak jual dapat ditekan.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="business-grid">
            <div class="backup-card">
                <div class="rank-label">Problem</div>
                <div class="business-title">Supplier perlu dibandingkan konsisten</div>
                <div class="small-muted">
                    Tanpa pembobotan, keputusan mudah bias ke harga murah tanpa melihat kualitas pasokan.
                </div>
            </div>
            <div class="backup-card">
                <div class="rank-label">Objective</div>
                <div class="business-title">Menentukan supplier terbaik</div>
                <div class="small-muted">
                    SAW dan TOPSIS dipakai untuk memberi ranking berbasis harga, turnover, dan umur simpan.
                </div>
            </div>
            <div class="backup-card">
                <div class="rank-label">Business Value</div>
                <div class="business-title">Pengadaan lebih efisien</div>
                <div class="small-muted">
                    Hasil ranking membantu memilih vendor utama, vendor cadangan, dan evaluasi pasokan.
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


df = load_data()

if "theme_mode" not in st.session_state:
    st.session_state.theme_mode = "Dark"

with st.sidebar:
    st.markdown("## Supplier Intelligence")
    theme_mode = st.radio("Mode tampilan", ["Light", "Dark"], horizontal=True, key="theme_mode")
    st.markdown("---")
    menu = st.radio(
        "Mode Analisis",
        ["Evaluasi Aktif", "Audit Post-Mortem", "Eksplorasi Data Mentah"],
    )
    st.markdown("---")
    st.markdown("### Bobot Kriteria")
    w_price = st.number_input("Harga (Cost) %", 0, 100, 30)
    w_turnover = st.number_input("Kecepatan Laku (Benefit) %", 0, 100, 20)
    w_shelf = st.number_input("Kesegaran / Umur Simpan (Benefit) %", 0, 100, 50)

st.markdown(get_custom_css(theme_mode), unsafe_allow_html=True)

total_weight = w_price + w_turnover + w_shelf
if total_weight != 100:
    st.sidebar.error(f"Total bobot {total_weight}%. Harus tepat 100%.")
    st.stop()

w_price, w_turnover, w_shelf = w_price / 100, w_turnover / 100, w_shelf / 100

if menu == "Evaluasi Aktif":
    st.markdown(
        get_header_style(
            "Analisa Pengadaan Barang Aktif",
            "Evaluasi supplier aktif dan backordered menggunakan SAW serta TOPSIS berdasarkan bobot kriteria yang dapat disimulasikan.",
            theme_mode,
            "Supplier Intelligence DSS",
        ),
        unsafe_allow_html=True,
    )

    df_active = df[df["Status"].isin(["Active", "Backordered"])].copy()
    eval_level = st.radio(
        "Level Evaluasi",
        ["Per Produk Spesifik", "Keseluruhan Kategori"],
        horizontal=True,
    )

    col1, col2 = st.columns(2)
    with col1:
        selected_cat = st.selectbox("Kategori", sorted(df_active["Catagory"].dropna().unique()))

    if eval_level == "Per Produk Spesifik":
        with col2:
            products = sorted(df_active[df_active["Catagory"] == selected_cat]["Product_Name"].dropna().unique())
            selected_prod = st.selectbox("Produk", products)

        df_eval = df_active[
            (df_active["Catagory"] == selected_cat)
            & (df_active["Product_Name"] == selected_prod)
        ]
        target_name = selected_prod
    else:
        df_eval = df_active[df_active["Catagory"] == selected_cat]
        target_name = f"Kategori {selected_cat}"

    if df_eval["Supplier_Name"].nunique() < 2:
        st.warning("Supplier tidak cukup untuk evaluasi pada filter ini.")
    else:
        grouped = (
            df_eval.groupby("Supplier_Name")
            .agg(
                Unit_Price=("Unit_Price", "mean"),
                Turnover_Rate=("Turnover_Rate", "mean"),
                Shelf_Life_Days=("Shelf_Life_Days", "mean"),
            )
            .reset_index()
        )

        grouped["Norm_Price"] = min_max_cost(grouped["Unit_Price"])
        grouped["Norm_Turnover"] = min_max_benefit(grouped["Turnover_Rate"])
        grouped["Norm_Shelf"] = min_max_benefit(grouped["Shelf_Life_Days"])

        grouped["Skor_SAW"] = (
            grouped["Norm_Price"] * w_price
            + grouped["Norm_Turnover"] * w_turnover
            + grouped["Norm_Shelf"] * w_shelf
        )

        grouped["V_Price"] = grouped["Norm_Price"] * w_price
        grouped["V_Turnover"] = grouped["Norm_Turnover"] * w_turnover
        grouped["V_Shelf"] = grouped["Norm_Shelf"] * w_shelf

        a_plus = np.array([w_price, w_turnover, w_shelf])
        a_minus = np.array([0, 0, 0])

        grouped["D_Plus"] = grouped.apply(
            lambda row: np.sqrt(
                (row["V_Price"] - a_plus[0]) ** 2
                + (row["V_Turnover"] - a_plus[1]) ** 2
                + (row["V_Shelf"] - a_plus[2]) ** 2
            ),
            axis=1,
        )
        grouped["D_Minus"] = grouped.apply(
            lambda row: np.sqrt(
                (row["V_Price"] - a_minus[0]) ** 2
                + (row["V_Turnover"] - a_minus[1]) ** 2
                + (row["V_Shelf"] - a_minus[2]) ** 2
            ),
            axis=1,
        )
        grouped["Skor_TOPSIS"] = grouped["D_Minus"] / (grouped["D_Plus"] + grouped["D_Minus"])

        normalized_matrix = grouped[["Supplier_Name", "Norm_Price", "Norm_Turnover", "Norm_Shelf"]]
        weighted_matrix = grouped[["Supplier_Name", "V_Price", "V_Turnover", "V_Shelf"]]
        saw_results = grouped[["Supplier_Name", "Unit_Price", "Turnover_Rate", "Shelf_Life_Days", "Skor_SAW"]]
        topsis_results = grouped[
            ["Supplier_Name", "Unit_Price", "Turnover_Rate", "Shelf_Life_Days", "D_Plus", "D_Minus", "Skor_TOPSIS"]
        ]

        selected_method = st.radio("Metode Grafik", ["TOPSIS", "SAW"], horizontal=True)
        score_col = "Skor_TOPSIS" if selected_method == "TOPSIS" else "Skor_SAW"
        grouped = grouped.sort_values(score_col, ascending=False)
        top_supplier = grouped.iloc[0]

        st.markdown(
            f"""
            <div class="recommendation-card">
                <div class="recommendation-label">Rekomendasi Supplier untuk {target_name}</div>
                <div class="recommendation-name">{top_supplier['Supplier_Name']}</div>
                <div class="recommendation-score">{selected_method} Score: {top_supplier[score_col]:.4f}</div>
                <div class="recommendation-copy">
                    Supplier ini memiliki nilai terbaik berdasarkan bobot kriteria saat ini.
                    Ubah bobot di sidebar untuk mensimulasikan prioritas pengadaan yang berbeda.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        fig = px.bar(
            grouped,
            x="Supplier_Name",
            y=score_col,
            color=score_col,
            color_continuous_scale="Teal",
            title=f"Peringkat Supplier ({selected_method})",
        )
        st.plotly_chart(apply_plotly_theme(fig, theme_mode), use_container_width=True)

        st.markdown("### Tabel Ranking Supplier")
        rename_dict = {
            "Supplier_Name": "Nama Pemasok",
            "Unit_Price": "Harga Satuan",
            "Turnover_Rate": "Kecepatan Laku",
            "Shelf_Life_Days": "Umur Simpan",
            "Skor_SAW": "Skor Akhir (SAW)",
            "Skor_TOPSIS": "Skor Akhir (TOPSIS)",
        }
        display_cols = ["Supplier_Name", "Unit_Price", "Turnover_Rate", "Shelf_Life_Days", score_col]
        df_display = grouped[display_cols].rename(columns=rename_dict)
        score_display = rename_dict[score_col]

        st.dataframe(
            df_display.style.format(
                {
                    "Harga Satuan": "${:.2f}",
                    "Kecepatan Laku": "{:.2f}",
                    "Umur Simpan": "{:.0f} Hari",
                    score_display: "{:.3f}",
                }
            ),
            use_container_width=True,
            hide_index=True,
        )

        st.markdown("### Download Hasil DSS")
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.download_button("Normalized Matrix", normalized_matrix.to_csv(index=False), "normalized_matrix.csv", "text/csv")
        with c2:
            st.download_button("Weighted Matrix", weighted_matrix.to_csv(index=False), "weighted_matrix.csv", "text/csv")
        with c3:
            st.download_button("SAW Results", saw_results.to_csv(index=False), "saw_results.csv", "text/csv")
        with c4:
            st.download_button("TOPSIS Results", topsis_results.to_csv(index=False), "topsis_results.csv", "text/csv")

    render_business_understanding()

elif menu == "Audit Post-Mortem":
    st.markdown(
        get_header_style(
            "Audit Supplier Discontinued",
            "Meninjau supplier yang sudah dihentikan untuk menemukan indikasi risiko seperti umur simpan negatif dan performa pasokan yang tidak sehat.",
            theme_mode,
            "Post-Mortem Analysis",
        ),
        unsafe_allow_html=True,
    )

    df_disc = df[df["Status"] == "Discontinued"].copy()
    df_disc["Red_Flag"] = df_disc["Shelf_Life_Days"] < 0

    m1, m2, m3 = st.columns(3)
    m1.metric("Total Discontinued", f"{len(df_disc):,}")
    m2.metric("Red Flag", f"{int(df_disc['Red_Flag'].sum()):,}")
    m3.metric("Supplier Terdampak", f"{df_disc['Supplier_Name'].nunique():,}")

    st.dataframe(df_disc, use_container_width=True, hide_index=True)
    render_business_understanding()

else:
    st.markdown(
        get_header_style(
            "Eksplorasi Data Mentah",
            "Melihat keseluruhan data supplier, produk, status transaksi, harga, stok, dan performa operasional sebagai dasar analisis keputusan.",
            theme_mode,
            "Data Exploration",
        ),
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Transaksi", f"{len(df):,}")
    col2.metric("Total Supplier", f"{df['Supplier_Name'].nunique():,}")
    col3.metric("Total Produk", f"{df['Product_Name'].nunique():,}")

    search = st.text_input("Cari Supplier / Produk")
    if search:
        mask = df["Supplier_Name"].str.contains(search, case=False, na=False) | df["Product_Name"].str.contains(
            search, case=False, na=False
        )
        st.dataframe(df[mask], use_container_width=True, hide_index=True)
    else:
        st.dataframe(df, use_container_width=True, hide_index=True)

    render_business_understanding()
