import streamlit as st

def render_recommendation_table(df_result):
    st.subheader("🌟 Top Rekomendasi Wisata")
    
    # Urutkan berdasarkan skor tertinggi
    df_sorted = df_result.sort_values(by='skor_rekomendasi', ascending=False).reset_index(drop=True)
    
    # Pilih kolom yang relevan untuk ditampilkan ke user
    kolom_tampil = ['nama', 'kategori', 'jarak_pusat_km', 'htm_weekday', 'vote_average', 'skor_rekomendasi']
    
    # Jika datasetmu punya kolom-kolom ini, tampilkan. Sesuaikan nama kolomnya jika beda.
    kolom_ada = [col for col in kolom_tampil if col in df_sorted.columns]
    
    df_display = df_sorted[kolom_ada].copy()
    
    # Format skor agar rapi (2 angka di belakang koma)
    df_display['skor_rekomendasi'] = df_display['skor_rekomendasi'].round(2)
    
    st.dataframe(
        df_display, 
        use_container_width=True,
        hide_index=True
    )