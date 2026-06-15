import streamlit as st
from core.dataset import pariwisata
from core.fuzzy import hitung_fuzzy_tsukamoto

def render_dashboard():
    st.title("Dashboard Rekomendasi Utama")
    st.markdown("Berikut adalah daftar rekomendasi tempat wisata di Yogyakarta berdasarkan perhitungan Fuzzy Tsukamoto.")
    
    # 1. Memuat data dari dataset clean
    try:
        df_raw = pariwisata()
    except Exception as e:
        st.error(f"Gagal memuat dataset: {e}")
        return

    # 2. Menjalankan perhitungan Tsukamoto dengan parameter bawaan
    if 'custom_params' in st.session_state and st.session_state.custom_params is not None:
        st.success("Menggunakan parameter Fuzzy yang telah Anda sesuaikan dari Laboratorium.")
        df_result = hitung_fuzzy_tsukamoto(df_raw, custom_params=st.session_state.custom_params)
    else:
        st.info("Menggunakan parameter Fuzzy bawaan (Default).")
        df_result = hitung_fuzzy_tsukamoto(df_raw)
    
    # 3. Memproses hasil untuk tampilan tabel
    st.subheader("Top Rekomendasi")
    
    # Mengurutkan data berdasarkan skor rekomendasi dari yang terbesar ke terkecil
    df_sorted = df_result.sort_values(by='skor_rekomendasi', ascending=False).reset_index(drop=True)
    
    # Menentukan kolom yang ingin ditampilkan agar tabel tidak terlalu panjang
    kolom_tampil = [
        'nama', 
        'jarak_pusat_km', 
        'htm_weekday', 
        'htm_weekend', 
        'vote_average', 
        'skor_rekomendasi'
    ]
    
    # Memastikan kolom yang diminta ada di dalam dataframe
    kolom_ada = [col for col in kolom_tampil if col in df_sorted.columns]
    df_display = df_sorted[kolom_ada].copy()
    
    # Membulatkan skor rekomendasi agar lebih rapi dilihat
    if 'skor_rekomendasi' in df_display.columns:
        df_display['skor_rekomendasi'] = df_display['skor_rekomendasi'].round(2)
        
    # 4. Menampilkan tabel ke layar
    st.dataframe(
        df_display,
        use_container_width=True,
        hide_index=True
    )
    
    st.caption("Data di atas menggunakan batas parameter bawaan. Anda dapat membedah kalkulasinya di menu Laboratorium Fuzzy.")