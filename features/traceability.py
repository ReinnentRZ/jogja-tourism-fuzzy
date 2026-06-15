import streamlit as st
from core.fuzzy import dapatkan_detail_kalkulasi, plot_kurva

def render_traceability_section(df_result):
    st.subheader("🔍 Bedah Kalkulasi (Traceability)")
    st.markdown("Pilih satu tempat wisata untuk melihat bagaimana skor Fuzzy Tsukamoto dihitung.")
    
    daftar_wisata = df_result['nama'].tolist()
    pilihan = st.selectbox("Pilih Tempat Wisata:", daftar_wisata)
    
    if pilihan:
        detail = dapatkan_detail_kalkulasi(df_result, pilihan)
        
        if detail:
            st.success(f"Skor Final untuk **{detail['nama']}**: {detail['skor_final']:.2f}")
            
            col1, col2 = st.columns(2)
            with col1:
                st.write("**1. Nilai Riil:**")
                st.json(detail['nilai_riil'])
                
            with col2:
                st.write("**2. Hasil Fuzzifikasi (\u03bc):**")
                st.json(detail['fuzzifikasi'])
                
            st.write("**3. Evaluasi Rules (Alpha & Z):**")
            st.json(detail['rules'])