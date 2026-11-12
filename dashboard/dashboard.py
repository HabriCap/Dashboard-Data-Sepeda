import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from pathlib import Path

# Konfigurasi Halaman Streamlit
st.set_page_config(page_title="Bike Sharing Dashboard", page_icon="🚲", layout="wide")
sns.set_theme(style="whitegrid")

# Fungsi untuk memuat data 
@st.cache_data
def load_data():
    # Mengambil path relatif agar bisa berjalan di lokal maupun cloud
    data_path = Path(__file__).parent / "main_data.csv"
    df = pd.read_csv(data_path)
    df["dteday"] = pd.to_datetime(df["dteday"])
    return df

df = load_data()

st.sidebar.header("Filter Data")
min_date = df["dteday"].min().date()
max_date = df["dteday"].max().date()

date_range = st.sidebar.date_input(
    "Rentang Waktu",
    value=[min_date, max_date],
    min_value=min_date,
    max_value=max_date
)

if len(date_range) < 2:
    st.info("Silakan pilih satu hari lagi sebagai tanggal akhir rentang.")
    st.stop()

start_date, end_date = date_range

selected_season = st.sidebar.multiselect(
    "Musim",
    options=df["season_label"].unique(),
    default=df["season_label"].unique()
)

# Filter dataset berdasarkan input sidebar
main_df = df[(df["dteday"].dt.date >= start_date) & 
             (df["dteday"].dt.date <= end_date) & 
             (df["season_label"].isin(selected_season))]

# KONTEN UTAMA 
st.title(" Bike Sharing Analytics Dashboard")
st.markdown("Dashboard ini menampilkan performa penyewaan sepeda (2011-2012) berdasarkan jam operasional, cuaca, dan profil pengguna.")

# Metrik Utama (Baris 1)
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Penyewaan (Semua Pengguna)", f"{main_df['cnt'].sum():,}")
with col2:
    st.metric("Total Pengguna Terdaftar (Registered)", f"{main_df['registered'].sum():,}")
with col3:
    st.metric("Total Pengguna Kasual (Casual)", f"{main_df['casual'].sum():,}")

st.divider()

# Visualisasi 1: Jam Sibuk Fall
st.subheader("1. Kenaikan Rata-Rata Penyewaan di Jam Sibuk Musim Gugur (2011 vs 2012)")
q1_df = df[(df["workingday"] == 1) & (df["hr"].isin([8, 17])) & (df["season_label"] == "Fall")]
q1_summary = q1_df.groupby(["year", "hr"])["cnt"].mean().reset_index()

fig1, ax1 = plt.subplots(figsize=(10, 5))
sns.barplot(data=q1_summary, x="hr", y="cnt", hue="year", palette=["#7FB3D5", "#1F618D"], ax=ax1)
for container in ax1.containers:
    ax1.bar_label(container, fmt="%.1f", padding=3, fontweight="bold")
ax1.set_xlabel("Jam Operasional (08:00 & 17:00)")
ax1.set_ylabel("Rata-Rata Penyewaan")
ax1.set_ylim(0, 950)
sns.despine(ax=ax1)
st.pyplot(fig1)

st.divider()

# Visualisasi 2: Dampak Cuaca pada Akhir Pekan
st.subheader("2. Dampak Kelembaban Udara terhadap Pengguna Kasual di Akhir Pekan")
q2_df = main_df[main_df["workingday"] == 0]

if not q2_df.empty:
    fig2, ax2 = plt.subplots(figsize=(10, 5))
    sns.regplot(data=q2_df, x="hum_pct", y="casual", scatter_kws={"alpha": 0.3}, line_kws={"color": "red"}, ax=ax2)
    ax2.set_xlabel("Kelembaban Udara (%)")
    ax2.set_ylabel("Jumlah Pengguna Kasual")
    sns.despine(ax=ax2)
    st.pyplot(fig2)
else:
    st.warning("Tidak ada data untuk rentang waktu/musim yang dipilih.")

st.divider()

# Visualisasi 3: Analisis Lanjutan (Clustering Waktu)
st.subheader("3. Analisis Lanjutan: Pola Penyewaan Berdasarkan Klaster Waktu")
def categorize_time(hr):
    if 0 <= hr <= 5: return "1. Dini Hari (00-05)"
    elif 6 <= hr <= 9: return "2. Jam Sibuk Pagi (06-09)"
    elif 10 <= hr <= 15: return "3. Siang Hari (10-15)"
    elif 16 <= hr <= 19: return "4. Jam Sibuk Sore (16-19)"
    else: return "5. Malam Hari (20-23)"

if not main_df.empty:
    cluster_df = main_df.copy()
    cluster_df["time_cluster"] = cluster_df["hr"].apply(categorize_time)
    cluster_df["day_type"] = cluster_df["workingday"].map({0: "Akhir Pekan/Libur", 1: "Hari Kerja"})
    
    cluster_agg = cluster_df.groupby(["time_cluster", "day_type"])[["casual", "registered"]].mean().reset_index()
    cluster_melt = cluster_agg.melt(id_vars=["time_cluster", "day_type"], value_vars=["casual", "registered"], var_name="Tipe Pengguna", value_name="Rata-Rata")
    
    fig3 = sns.catplot(data=cluster_melt, x="time_cluster", y="Rata-Rata", hue="Tipe Pengguna", col="day_type", kind="bar", height=5, aspect=1.2, palette=["#F39C12", "#2C3E50"])
    fig3.set_titles("{col_name}", fontweight="bold")
    fig3.set_axis_labels("Klaster Waktu", "Rata-Rata Penyewaan")
    fig3.tick_params(axis="x", rotation=20)
    st.pyplot(fig3.fig)