import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from core.dataset import pariwisata

def render_analisis_data():
    """
    Merender halaman Analisis Data (Exploratory Data Analysis).
    Menampilkan metrik statistik, distribusi, dan korelasi dari dataset pariwisata.
    """
    st.title("Analisis Data Pariwisata Yogyakarta")
    st.markdown("Halaman ini menyajikan Exploratory Data Analysis (EDA) untuk memahami karakteristik dataset tempat wisata sebelum diproses oleh sistem rekomendasi.")

    # Memuat dataset
    try:
        df = pariwisata()
    except Exception as e:
        st.error(f"Gagal memuat dataset: {e}")
        return

    # Pengaturan gaya visual grafik
    sns.set_theme(style="whitegrid")

    # Bagian 1: Ringkasan Metrik Utama
    st.header("1. Ringkasan Dataset")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Tempat Wisata", len(df))
    col2.metric("Rata-rata HTM Weekday", f"Rp {int(df['htm_weekday'].mean()):,}")
    col3.metric("Rata-rata Jarak Pusat", f"{df['jarak_pusat_km'].mean():.2f} KM")
    col4.metric("Rata-rata Rating", f"{df['vote_average'].mean():.2f}")

    st.markdown("---")

    # Bagian 2: Distribusi Harga Tiket dan Rating (Unsupervised look)
    st.header("2. Distribusi Data Utama")
    tab1, tab2 = st.tabs(["Distribusi Harga Tiket", "Distribusi Rating"])

    with tab1:
        st.subheader("Sebaran Harga Tiket Masuk (Weekday)")
        fig_htm, ax_htm = plt.subplots(figsize=(10, 5))
        # Membatasi visualisasi outlier agar grafik lebih representatif (misal maks 150rb)
        sns.histplot(df[df['htm_weekday'] <= 150000]['htm_weekday'], bins=30, kde=True, ax=ax_htm, color='royalblue')
        ax_htm.set_xlabel("Harga Tiket (Rp)")
        ax_htm.set_ylabel("Jumlah Tempat Wisata")
        st.pyplot(fig_htm)
        st.caption("Grafik difilter untuk HTM di bawah Rp 150.000 untuk memperjelas sebaran mayoritas data.")

    with tab2:
        st.subheader("Sebaran Rating Tempat Wisata")
        fig_rating, ax_rating = plt.subplots(figsize=(10, 5))
        sns.histplot(df['vote_average'], bins=20, kde=True, ax=ax_rating, color='seagreen')
        ax_rating.set_xlabel("Rating (1.0 - 5.0)")
        ax_rating.set_ylabel("Jumlah Tempat Wisata")
        st.pyplot(fig_rating)

    st.markdown("---")

    # Bagian 3: Analisis Korelasi Bivariat
    st.header("3. Analisis Korelasi")
    st.markdown("Menganalisis hubungan antara dua variabel numerik dalam dataset.")
    
    col_korelasi1, col_korelasi2 = st.columns(2)
    
    with col_korelasi1:
        st.subheader("Jarak vs Jumlah Ulasan")
        fig_scatter1, ax_scatter1 = plt.subplots(figsize=(6, 4))
        sns.scatterplot(data=df, x='jarak_pusat_km', y='vote_count', alpha=0.6, ax=ax_scatter1)
        ax_scatter1.set_xlabel("Jarak dari Pusat (KM)")
        ax_scatter1.set_ylabel("Jumlah Ulasan (Popularitas)")
        st.pyplot(fig_scatter1)
        st.caption("Melihat apakah tempat wisata yang lebih dekat dari pusat kota mendapatkan interaksi lebih banyak.")

    with col_korelasi2:
        st.subheader("Harga Tiket vs Rating")
        fig_scatter2, ax_scatter2 = plt.subplots(figsize=(6, 4))
        # Membatasi tampilan outlier harga
        sns.scatterplot(data=df[df['htm_weekday'] <= 150000], x='htm_weekday', y='vote_average', alpha=0.6, ax=ax_scatter2)
        ax_scatter2.set_xlabel("Harga Tiket (Rp)")
        ax_scatter2.set_ylabel("Rating (Vote Average)")
        st.pyplot(fig_scatter2)
        st.caption("Melihat apakah tempat yang lebih mahal cenderung memiliki rating kepuasan yang lebih tinggi.")

    st.markdown("---")

    # Bagian 4: Top Entitas
    st.header("4. Top 10 Tempat Wisata (Berdasarkan Popularitas Dasar)")
    st.markdown("Peringkat ini diambil murni dari tingginya jumlah ulasan pengunjung, tanpa melibatkan perhitungan sistem rekomendasi Fuzzy.")
    
    top_10_populer = df.sort_values(by='vote_count', ascending=False).head(10)
    
    fig_bar, ax_bar = plt.subplots(figsize=(12, 6))
    sns.barplot(data=top_10_populer, x='vote_count', y='nama', palette='viridis', ax=ax_bar)
    ax_bar.set_xlabel("Jumlah Ulasan (Vote Count)")
    ax_bar.set_ylabel("Nama Tempat Wisata")
    ax_bar.set_title("10 Tempat Wisata Paling Sering Diulas")
    st.pyplot(fig_bar)