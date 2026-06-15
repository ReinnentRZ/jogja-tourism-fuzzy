import streamlit as st
from core.dataset import pariwisata
from core.fuzzy import hitung_fuzzy_tsukamoto, dapatkan_detail_kalkulasi, plot_kurva

def render_laboratorium():
    st.title("Laboratorium Fuzzy")
    st.markdown("Halaman ini memungkinkan Anda untuk mengubah batasan parameter fuzzy secara manual dan melihat jejak perhitungannya secara detail.")
    
    try:
        df_raw = pariwisata()
    except Exception as e:
        st.error(f"Gagal memuat dataset: {e}")
        return

    # 1. Inisialisasi State agar data tidak hilang saat halaman dimuat ulang
    if 'df_result' not in st.session_state:
        st.session_state.df_result = hitung_fuzzy_tsukamoto(df_raw)
    
    if 'custom_params' not in st.session_state:
        st.session_state.custom_params = None

    st.header("1. Pengaturan Parameter")
    st.markdown("Ubah batas parameter melalui form di bawah ini, lalu klik tombol Terapkan untuk menghitung ulang.")
    
    # 2. Menggunakan st.form untuk menghentikan live update
    with st.form(key='form_parameter'):
        col1, col2, col3 = st.columns(3)
        
       # Tarik memori sebelumnya (jika ada) supaya slider tidak reset
        default_htm = (10000, 50000)
        default_jarak = (5, 25)
        default_rating = (3.5, 4.5)

        if st.session_state.custom_params is not None:
            p = st.session_state.custom_params
            default_htm = (int(p['htm_murah'][2]), int(p['htm_murah'][3]))
            default_jarak = (int(p['jarak_dekat'][2]), int(p['jarak_dekat'][3]))
            default_rating = (float(p['vote_avg_rendah'][2]), float(p['vote_avg_rendah'][3]))

        with col1:
            st.subheader("Harga Tiket")
            htm_batas = st.slider("Batas Murah ke Mahal (Rp)", 10000, 100000, default_htm, step=5000)
            
        with col2:
            st.subheader("Jarak")
            jarak_batas = st.slider("Batas Dekat ke Jauh (KM)", 2, 40, default_jarak, step=1)
            
        with col3:
            st.subheader("Rating")
            rating_batas = st.slider("Batas Rendah ke Tinggi", 2.0, 5.0, default_rating, step=0.1)

        # Tombol eksekusi
        submit_button = st.form_submit_button(label='Terapkan Parameter')

    # 3. Logika saat tombol ditekan
    if submit_button:
        custom_params = {
            'htm_murah': [0, 0, htm_batas[0], htm_batas[1]],
            'htm_mahal': [htm_batas[0], htm_batas[1], 500000, 500000],
            'jarak_dekat': [0, 0, jarak_batas[0], jarak_batas[1]],
            'jarak_jauh': [jarak_batas[0], jarak_batas[1], 60, 60],
            'vote_avg_rendah': [1.0, 1.0, rating_batas[0], rating_batas[1]],
            'vote_avg_tinggi': [rating_batas[0], rating_batas[1], 5.0, 5.0],
            
            # Nilai statis untuk mempermudah form
            'vote_cnt_sedikit': [0, 0, 100, 1000],
            'vote_cnt_banyak': [100, 1000, 82000, 82000],
            'hotel_sedikit': [0, 0, 5, 50],
            'hotel_banyak': [5, 50, 524, 524]
        }
        
        # Simpan parameter ke session state
        st.session_state.custom_params = custom_params
        
        # Hitung ulang dan simpan hasilnya ke session state
        st.session_state.df_result = hitung_fuzzy_tsukamoto(df_raw, custom_params=custom_params)
        st.success("Parameter berhasil diterapkan! Data di bawah telah diperbarui.")

    # 4. Mengambil parameter aktif untuk menggambar grafik
    aktif_params = st.session_state.custom_params
    if aktif_params is None:
        # Nilai default jika tombol belum pernah ditekan
        aktif_params = {
            'htm_murah': [0, 0, 10000, 50000],
            'htm_mahal': [10000, 50000, 500000, 500000],
            'jarak_dekat': [0, 0, 5, 25],
            'jarak_jauh': [5, 25, 60, 60],
            'vote_avg_rendah': [1.0, 1.0, 3.5, 4.5],
            'vote_avg_tinggi': [3.5, 4.5, 5.0, 5.0]
        }

    st.markdown("---")
    st.header("2. Visualisasi Kurva Keanggotaan")
    
    tab1, tab2, tab3 = st.tabs(["Kurva Harga Tiket", "Kurva Jarak", "Kurva Rating"])
    
    with tab1:
        fig_htm = plot_kurva("Harga Tiket", 150000, aktif_params['htm_murah'], aktif_params['htm_mahal'], "Murah", "Mahal")
        st.pyplot(fig_htm)
        
    with tab2:
        fig_jarak = plot_kurva("Jarak dari Pusat", 60, aktif_params['jarak_dekat'], aktif_params['jarak_jauh'], "Dekat", "Jauh")
        st.pyplot(fig_jarak)
        
    with tab3:
        fig_rating = plot_kurva("Rating Tempat", 5.0, aktif_params['vote_avg_rendah'], aktif_params['vote_avg_tinggi'], "Rendah", "Tinggi")
        st.pyplot(fig_rating)

    st.markdown("---")
    st.header("3. Bedah Kalkulasi Spesifik")
    
    # Memanggil dataframe dari session state agar datanya konsisten
    df_sekarang = st.session_state.df_result
    
    daftar_wisata = df_sekarang['nama'].tolist()
    pilihan_wisata = st.selectbox("Pilih Tempat Wisata untuk dibedah:", daftar_wisata)
    
    if pilihan_wisata:
        detail = dapatkan_detail_kalkulasi(df_sekarang, pilihan_wisata)
        
        if detail:
            st.markdown(f"### Skor Rekomendasi: {detail['skor_final']:.2f} / 100")
            st.markdown("---")
            
            st.markdown("#### 1. Nilai Fakta di Lapangan")
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("HTM Weekday", f"Rp {int(detail['nilai_riil']['htm_weekday']):,}")
            c2.metric("Jarak Pusat", f"{detail['nilai_riil']['jarak_pusat_km']} KM")
            c3.metric("Rating", detail['nilai_riil']['vote_average'])
            c4.metric("Jumlah Hotel", detail['nilai_riil']['jumlah_hotel_terdekat'])
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            st.markdown("#### 2. Derajat Keanggotaan (Fuzzifikasi)")
            
            def batasi_nilai(val):
                return min(max(float(val), 0.0), 1.0)
            
            f1, f2, f3 = st.columns(3)
            with f1:
                st.caption(f"Harga Murah: {detail['fuzzifikasi']['htm_wd_murah'] * 100:.1f}%")
                st.progress(batasi_nilai(detail['fuzzifikasi']['htm_wd_murah']))
                st.caption(f"Harga Mahal: {detail['fuzzifikasi']['htm_wd_mahal'] * 100:.1f}%")
                st.progress(batasi_nilai(detail['fuzzifikasi']['htm_wd_mahal']))
                
            with f2:
                st.caption(f"Jarak Dekat: {detail['fuzzifikasi']['jarak_dekat'] * 100:.1f}%")
                st.progress(batasi_nilai(detail['fuzzifikasi']['jarak_dekat']))
                st.caption(f"Jarak Jauh: {detail['fuzzifikasi']['jarak_jauh'] * 100:.1f}%")
                st.progress(batasi_nilai(detail['fuzzifikasi']['jarak_jauh']))

            with f3:
                st.caption(f"Rating Tinggi: {detail['fuzzifikasi']['vote_avg_tinggi'] * 100:.1f}%")
                st.progress(batasi_nilai(detail['fuzzifikasi']['vote_avg_tinggi']))
                st.caption(f"Rating Rendah: {detail['fuzzifikasi']['vote_avg_rendah'] * 100:.1f}%")
                st.progress(batasi_nilai(detail['fuzzifikasi']['vote_avg_rendah']))

            st.markdown("<br>", unsafe_allow_html=True)

            st.markdown("#### 3. Evaluasi Aturan (Bobot Alpha dan Nilai Z)")
            data_aturan = []
            for rule_name, rule_data in detail['rules'].items():
                data_aturan.append({
                    "Aturan": rule_name,
                    "Kesimpulan": rule_data['type'],
                    "Kekuatan (Alpha)": f"{rule_data['alpha']:.5f}",
                    "Nilai Z": f"{rule_data['z']:.2f}"
                })
            st.table(data_aturan)