import folium
import pandas as pd

def buat_peta_rekomendasi(df_wisata, pusat_lat, pusat_lon, nama_pusat="Titik Pencarian"):
    """
    Membuat objek peta Folium dengan titik pusat (hotel/user) dan sebaran lokasi wisata.
    
    Parameter:
    - df_wisata: Dataframe berisi top 10 wisata yang sudah dihitung skornya.
    - pusat_lat, pusat_lon: Koordinat titik acuan (Pusat baru).
    - nama_pusat: Nama label untuk penanda titik pusat.
    """
    # 1. Inisialisasi peta, difokuskan pada titik pusat pencarian
    peta = folium.Map(location=[pusat_lat, pusat_lon], zoom_start=12)

    # 2. Tambahkan Penanda (Marker) untuk Titik Pusat
    # Diberi warna biru dengan ikon informasi agar beda dari tempat wisata
    folium.Marker(
        location=[pusat_lat, pusat_lon],
        popup=f"<b>{nama_pusat}</b><br>Titik Acuan Pencarian",
        tooltip="Lokasi Pusat",
        icon=folium.Icon(color="blue", icon="info-sign")
    ).add_to(peta)

    # 3. Tambahkan Penanda untuk Top 10 Tempat Wisata
    for index, row in df_wisata.iterrows():
        # Validasi sederhana agar tidak error jika ada data kosong
        if pd.notna(row['latitude']) and pd.notna(row['longitude']):
            
            # Format teks yang muncul saat pin diklik
            teks_popup = f"""
            <b>{row['nama']}</b><br>
            Jarak: {row['jarak_pusat_km']:.2f} KM<br>
            Skor Rekomendasi: {row['skor_rekomendasi']:.2f}
            """
            
            # Marker wisata diberi warna merah
            folium.Marker(
                location=[row['latitude'], row['longitude']],
                popup=folium.Popup(teks_popup, max_width=300),
                tooltip=row['nama'], # Teks yang muncul saat kursor diarahkan (hover)
                icon=folium.Icon(color="red", icon="map-marker")
            ).add_to(peta)

    return peta