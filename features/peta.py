import streamlit as st
import pandas as pd
import numpy as np
import math
from core.dataset import pariwisata
from core.fuzzy import hitung_fuzzy_tsukamoto

def hitung_haversine(lat1, lon1, lat2, lon2):
    """
    Menghitung jarak garis lurus antara dua titik koordinat di permukaan bumi dalam satuan Kilometer.
    """
    R = 6371.0 # Radius rata-rata bumi dalam kilometer

    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    dlon = lon2_rad - lon1_rad
    dlat = lat2_rad - lat1_rad

    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    jarak_km = R * c
    return jarak_km

def render_peta_rekomendasi():
    st.title("Peta Rekomendasi Dinamis (Berbasis Lokasi)")
    st.markdown("Fitur ini menghitung ulang rekomendasi wisata menggunakan logika Fuzzy berdasarkan jarak aktual dari posisi Anda saat ini.")

    try:
        df = pariwisata()
    except Exception as e:
        st.error(f"Gagal memuat dataset: {e}")
        return

    # Memastikan kolom koordinat tersedia
    if 'latitude' not in df.columns or 'longitude' not in df.columns:
        st.warning("Kolom 'latitude' dan/atau 'longitude' tidak ditemukan dalam dataset. Pastikan penamaan kolom sudah benar.")
        return

    # 1. Definisi Lokasi Pengguna
    st.header("1. Tentukan Posisi Anda")
    
    # Preset lokasi acuan di Yogyakarta
    lokasi_preset = {
        "Stasiun Tugu": (-7.7891, 110.3633),
        "Terminal Giwangan": (-7.8344, 110.3925),
        "Bandara YIA": (-7.8967, 110.0526),
        "Kotagede (Jalan Kemasan)": (-7.8286, 110.3995),
        "Custom (Input Manual)": (0.0, 0.0)
    }
    
    pilihan_lokasi = st.selectbox("Pilih Titik Awal (Pusat Baru):", list(lokasi_preset.keys()))
    
    col_lat, col_lon = st.columns(2)
    if pilihan_lokasi == "Custom (Input Manual)":
        user_lat = col_lat.number_input("Latitude", value=-7.7956)
        user_lon = col_lon.number_input("Longitude", value=110.3695)
    else:
        user_lat = col_lat.number_input("Latitude", value=lokasi_preset[pilihan_lokasi][0], disabled=True)
        user_lon = col_lon.number_input("Longitude", value=lokasi_preset[pilihan_lokasi][1], disabled=True)

    tombol_hitung = st.button("Hitung Ulang Rekomendasi dari Lokasi Ini", type="primary")

    if tombol_hitung:
        # 2. Injeksi Jarak Dinamis (Haversine)
        # Menimpa kolom jarak_pusat_km dengan jarak dari lokasi pengguna yang baru
        df['jarak_pusat_km'] = df.apply(
            lambda row: hitung_haversine(user_lat, user_lon, row['latitude'], row['longitude']), axis=1
        )

        # 3. Eksekusi Ulang Fuzzy Tsukamoto
        # Jika ada parameter custom di session state, kita gunakan. Jika tidak, gunakan default.
        if 'custom_params' in st.session_state and st.session_state.custom_params is not None:
            df_hasil = hitung_fuzzy_tsukamoto(df, custom_params=st.session_state.custom_params)
        else:
            df_hasil = hitung_fuzzy_tsukamoto(df)

        # Mengurutkan hasil berdasarkan skor terbaik
        df_sorted = df_hasil.sort_values(by='skor_rekomendasi', ascending=False).reset_index(drop=True)
        
        # Mengambil Top 10 untuk ditampilkan di peta agar tidak terlalu penuh
        top_10 = df_sorted.head(10)

        st.markdown("---")
        st.header("2. Hasil Rekomendasi Terdekat & Terbaik")
        
        # 4. Merender Peta menggunakan st.map bawaan Streamlit
        st.markdown("Titik pada peta di bawah menunjukkan 10 tempat wisata dengan skor rekomendasi tertinggi berdasarkan lokasi yang Anda tentukan.")
        
        # Persiapan data peta (Streamlit map mendeteksi kolom 'latitude' dan 'longitude' secara otomatis)
        peta_data = top_10[['nama', 'latitude', 'longitude']].copy()
        
        st.map(peta_data, zoom=10)

        # 5. Tampilkan Tabel Ringkasan
        st.markdown("#### Detail 10 Rekomendasi Teratas")
        kolom_tampil = ['nama', 'jarak_pusat_km', 'htm_weekday', 'skor_rekomendasi']
        df_tampil = top_10[kolom_tampil].copy()
        df_tampil['jarak_pusat_km'] = df_tampil['jarak_pusat_km'].round(2)
        df_tampil['skor_rekomendasi'] = df_tampil['skor_rekomendasi'].round(2)
        
        # Rename kolom untuk tampilan
        df_tampil.rename(columns={'jarak_pusat_km': 'Jarak dari Anda (KM)'}, inplace=True)
        
        st.dataframe(df_tampil, use_container_width=True, hide_index=True)