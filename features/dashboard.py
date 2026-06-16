import streamlit as st
import pandas as pd
import folium # <-- Tambahan baru
from streamlit_folium import st_folium
from core.dataset import pariwisata, hotel
from core.haversine import hitung_haversine
from core.fuzzy import hitung_fuzzy_tsukamoto
from features.peta import buat_peta_rekomendasi

def render_dashboard():
    st.title("Dashboard Rekomendasi Wisata Interaktif")
    st.markdown("Temukan destinasi wisata terbaik di Yogyakarta berdasarkan jarak dari lokasi Anda dan perhitungan cerdas logika Fuzzy.")

    # 1. Memuat Dataset
    try:
        df_wisata = pariwisata()
        df_hotel = hotel()
    except Exception as e:
        st.error(f"Gagal memuat dataset: {e}. Pastikan file CSV tersedia di folder dataset/clean/.")
        return

    # 2. Antarmuka Pemilihan Titik Pusat
    st.header("1. Tentukan Titik Awal Anda")
    st.markdown("Jarak ke seluruh tempat wisata akan dihitung ulang otomatis berdasarkan titik yang Anda pilih.")
    
    metode_pusat = st.radio(
        "Pilih metode penentuan lokasi:",
        ["Landmark / Titik Umum", "Pilih Hotel / Penginapan", "Klik Titik di Peta"],
        horizontal=True
    )

    # Variabel penampung titik pusat
    user_lat, user_lon = 0.0, 0.0
    nama_pusat = "Titik Pusat"

    if metode_pusat == "Landmark / Titik Umum":
        lokasi_preset = {
            "Jalan Kemasan (Kotagede)": (-7.8286, 110.3995),
            "Stasiun Tugu": (-7.7891, 110.3633),
            "Terminal Giwangan": (-7.8344, 110.3925),
            "Bandara YIA": (-7.8967, 110.0526),
            "Titik Nol Kilometer (Malioboro)": (-7.8005, 110.3650)
        }
        pilihan_lokasi = st.selectbox("Pilih Landmark:", list(lokasi_preset.keys()))
        user_lat, user_lon = lokasi_preset[pilihan_lokasi]
        nama_pusat = pilihan_lokasi

    elif metode_pusat == "Pilih Hotel / Penginapan":
        pilihan_hotel = st.selectbox("Ketik atau pilih tempat Anda menginap:", df_hotel['NAMA PENGINAPAN'].unique())
        info_hotel = df_hotel[df_hotel['NAMA PENGINAPAN'] == pilihan_hotel].iloc[0]
        user_lat = info_hotel['Latitude']
        user_lon = info_hotel['Longitude']
        nama_pusat = pilihan_hotel

    else: # Klik Titik di Peta
        st.markdown("**Silakan klik lokasi mana saja pada peta di bawah ini untuk mendapatkan koordinatnya:**")
        # Membuat peta kosong khusus untuk nge-klik
        peta_pemilih = folium.Map(location=[-7.7956, 110.3695], zoom_start=12)
        
        # Menampilkan peta pemilih dan menangkap event klik
        peta_diklik = st_folium(peta_pemilih, width=800, height=350, key="peta_pemilih", returned_objects=["last_clicked"])
        
        if peta_diklik and peta_diklik.get("last_clicked"):
            user_lat = peta_diklik["last_clicked"]["lat"]
            user_lon = peta_diklik["last_clicked"]["lng"]
            nama_pusat = "Titik Kustom (Klik Peta)"
            st.success(f"Titik berhasil dikunci pada Latitude: {user_lat:.5f}, Longitude: {user_lon:.5f}")
        else:
            # Titik default kalau user belum ngeklik apa-apa
            user_lat, user_lon = -7.7956, 110.3695
            nama_pusat = "Titik Default (Pusat Jogja)"
            st.info("Menunggu Anda mengklik peta... (Saat ini menggunakan titik pusat Jogja)")

    st.markdown("---")

    # --- EKSEKUSI OTOMATIS ---
    with st.spinner("Mensinkronisasi data spasial dan Fuzzy..."):
        
        df_wisata['jarak_pusat_km'] = df_wisata.apply(
            lambda row: hitung_haversine(user_lat, user_lon, row['latitude'], row['longitude']), 
            axis=1
        )

        if 'custom_params' in st.session_state and st.session_state.custom_params is not None:
            df_hasil = hitung_fuzzy_tsukamoto(df_wisata, custom_params=st.session_state.custom_params)
        else:
            df_hasil = hitung_fuzzy_tsukamoto(df_wisata)
            st.caption("ℹ Menggunakan parameter Fuzzy bawaan (default).")

        df_top10 = df_hasil.sort_values(by='skor_rekomendasi', ascending=False).head(10).reset_index(drop=True)

        st.header("2. Peta & Hasil Rekomendasi Teratas")
        
        peta_folium = buat_peta_rekomendasi(df_top10, user_lat, user_lon, nama_pusat)
        st_folium(peta_folium, width=800, height=500, returned_objects=[], key="peta_hasil")

        st.subheader("Detail Top 10 Wisata")
        
        kolom_tampil = ['nama', 'jarak_pusat_km', 'htm_weekday', 'vote_average', 'jumlah_hotel_terdekat', 'skor_rekomendasi']
        df_tabel = df_top10[kolom_tampil].copy()
        
        df_tabel['jarak_pusat_km'] = df_tabel['jarak_pusat_km'].round(2)
        df_tabel['skor_rekomendasi'] = df_tabel['skor_rekomendasi'].round(2)
        
        df_tabel.rename(columns={
            'nama': 'Nama Tempat',
            'jarak_pusat_km': 'Jarak (KM)',
            'htm_weekday': 'Harga Tiket (Rp)',
            'vote_average': 'Rating',
            'jumlah_hotel_terdekat': 'Fasilitas Hotel',
            'skor_rekomendasi': 'Skor Fuzzy'
        }, inplace=True)
        
        st.dataframe(df_tabel, use_container_width=True, hide_index=True)