import streamlit as st
from features.dashboard import render_dashboard
from features.laboratorium import render_laboratorium
from features.analisis import render_analisis_data
from features.peta import render_peta_rekomendasi # Tambahkan baris ini

# Konfigurasi dasar halaman
st.set_page_config(
    page_title="Sistem Rekomendasi Wisata Jogja",
    layout="wide"
)

# Membuat Sidebar untuk Navigasi
st.sidebar.title("Menu Navigasi")
pilihan_menu = st.sidebar.radio(
    "Pilih Halaman:",
    ["Dashboard", "Laboratorium Fuzzy", "Analisis Data", "Peta Rekomendasi"] # Tambahkan menu ini
)

st.sidebar.markdown("---")
st.sidebar.caption("Sistem Rekomendasi Pariwisata Yogyakarta menggunakan Logika Fuzzy Tsukamoto.")

# Routing Halaman berdasarkan pilihan di sidebar
if pilihan_menu == "Dashboard":
    render_dashboard()
    
elif pilihan_menu == "Laboratorium Fuzzy":
    render_laboratorium()
    
elif pilihan_menu == "Analisis Data":
    render_analisis_data()

elif pilihan_menu == "Peta Rekomendasi": # Tambahkan blok logika ini
    render_peta_rekomendasi()