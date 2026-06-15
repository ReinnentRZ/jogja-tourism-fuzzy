import numpy as np
import pandas as pd
import skfuzzy as fuzz
import matplotlib.pyplot as plt

#[R1] IF htm_weekday is Murah AND htm_weekend is Murah AND jarak_pusat_km is Dekat AND vote_average is Tinggi AND vote_count is Banyak AND jumlah_hotel_terdekat is Banyak THEN Rekomendasi is Tinggi
#[R2] IF htm_weekday is Murah AND htm_weekend is Murah AND jarak_pusat_km is Jauh AND vote_average is Tinggi AND vote_count is Sedikit AND jumlah_hotel_terdekat is Sedikit THEN Rekomendasi is Tinggi
#[R3] IF htm_weekday is Mahal AND htm_weekend is Mahal AND jarak_pusat_km is Dekat AND vote_average is Tinggi AND vote_count is Banyak AND jumlah_hotel_terdekat is Banyak THEN Rekomendasi is Tinggi
#[R4] IF htm_weekday is Mahal AND htm_weekend is Mahal AND jarak_pusat_km is Dekat AND vote_average is Rendah AND vote_count is Banyak AND jumlah_hotel_terdekat is Banyak THEN Rekomendasi is Rendah
#[R5] IF htm_weekday is Mahal AND htm_weekend is Mahal AND jarak_pusat_km is Jauh AND vote_average is Rendah AND vote_count is Sedikit AND jumlah_hotel_terdekat is Sedikit THEN Rekomendasi is Rendah
#[R6] IF htm_weekday is Murah AND htm_weekend is Mahal AND jarak_pusat_km is Dekat AND vote_average is Rendah AND vote_count is Banyak AND jumlah_hotel_terdekat is Banyak THEN Rekomendasi is Rendah

def hitung_fuzzy_tsukamoto(df, custom_params=None):
    """
    Fungsi untuk menghitung skor rekomendasi wisata menggunakan metode Fuzzy Tsukamoto.
    Menerima DataFrame pariwisata dan mengembalikan DataFrame dengan tambahan kolom skor.
    """
    # Salin dataframe agar tidak merubah data asli
    df_fuzzy = df.copy()

    # 1. Definisikan Semesta Pembicaraan (Universe) Minimal
    x_htm = np.array([0, 500000])
    x_jarak = np.array([0, 60])
    x_vote_avg = np.array([1.0, 5.0])
    x_vote_cnt = np.array([0, 82000])
    x_hotel = np.array([0, 524])

    # 2. Definisikan Parameter Trapesium [a, b, c, d]
    if custom_params is None:
        # Jika tidak ada input dari slider Streamlit, gunakan nilai default ini
        p_htm_murah = [0, 0, 10000, 50000]
        p_htm_mahal = [10000, 50000, 500000, 500000]
        p_jarak_dekat = [0, 0, 5, 25]
        p_jarak_jauh = [5, 25, 60, 60]
        p_vote_avg_rendah = [1.0, 1.0, 3.5, 4.5]
        p_vote_avg_tinggi = [3.5, 4.5, 5.0, 5.0]
        p_vote_cnt_sedikit = [0, 0, 100, 1000]
        p_vote_cnt_banyak = [100, 1000, 82000, 82000]
        p_hotel_sedikit = [0, 0, 5, 50]
        p_hotel_banyak = [5, 50, 524, 524]
    else:
        # Jika dari slider dipasok nilai baru, gunakan nilai kustom tersebut
        p_htm_murah = custom_params['htm_murah']
        p_htm_mahal = custom_params['htm_mahal']
        p_jarak_dekat = custom_params['jarak_dekat']
        p_jarak_jauh = custom_params['jarak_jauh']
        p_vote_avg_rendah = custom_params['vote_avg_rendah']
        p_vote_avg_tinggi = custom_params['vote_avg_tinggi']
        p_vote_cnt_sedikit = custom_params['vote_cnt_sedikit']
        p_vote_cnt_banyak = custom_params['vote_cnt_banyak']
        p_hotel_sedikit = custom_params['hotel_sedikit']
        p_hotel_banyak = custom_params['hotel_banyak']

    # 3. Proses Fuzzifikasi
    df_fuzzy['mu_htm_wd_murah'] = fuzz.interp_membership(x_htm, fuzz.trapmf(x_htm, p_htm_murah), df_fuzzy['htm_weekday'])
    df_fuzzy['mu_htm_wd_mahal'] = fuzz.interp_membership(x_htm, fuzz.trapmf(x_htm, p_htm_mahal), df_fuzzy['htm_weekday'])
    df_fuzzy['mu_htm_we_murah'] = fuzz.interp_membership(x_htm, fuzz.trapmf(x_htm, p_htm_murah), df_fuzzy['htm_weekend'])
    df_fuzzy['mu_htm_we_mahal'] = fuzz.interp_membership(x_htm, fuzz.trapmf(x_htm, p_htm_mahal), df_fuzzy['htm_weekend'])
    df_fuzzy['mu_jarak_dekat'] = fuzz.interp_membership(x_jarak, fuzz.trapmf(x_jarak, p_jarak_dekat), df_fuzzy['jarak_pusat_km'])
    df_fuzzy['mu_jarak_jauh'] = fuzz.interp_membership(x_jarak, fuzz.trapmf(x_jarak, p_jarak_jauh), df_fuzzy['jarak_pusat_km'])
    df_fuzzy['mu_vote_avg_rendah'] = fuzz.interp_membership(x_vote_avg, fuzz.trapmf(x_vote_avg, p_vote_avg_rendah), df_fuzzy['vote_average'])
    df_fuzzy['mu_vote_avg_tinggi'] = fuzz.interp_membership(x_vote_avg, fuzz.trapmf(x_vote_avg, p_vote_avg_tinggi), df_fuzzy['vote_average'])
    df_fuzzy['mu_vote_cnt_sedikit'] = fuzz.interp_membership(x_vote_cnt, fuzz.trapmf(x_vote_cnt, p_vote_cnt_sedikit), df_fuzzy['vote_count'])
    df_fuzzy['mu_vote_cnt_banyak'] = fuzz.interp_membership(x_vote_cnt, fuzz.trapmf(x_vote_cnt, p_vote_cnt_banyak), df_fuzzy['vote_count'])
    df_fuzzy['mu_hotel_sedikit'] = fuzz.interp_membership(x_hotel, fuzz.trapmf(x_hotel, p_hotel_sedikit), df_fuzzy['jumlah_hotel_terdekat'])
    df_fuzzy['mu_hotel_banyak'] = fuzz.interp_membership(x_hotel, fuzz.trapmf(x_hotel, p_hotel_banyak), df_fuzzy['jumlah_hotel_terdekat'])

    # 4. Evaluasi Rule & Inferensi Tsukamoto
    # [R1] Rekomendasi is Tinggi
    df_fuzzy['alpha_R1'] = np.minimum(df_fuzzy['mu_htm_wd_murah'], np.minimum(df_fuzzy['mu_htm_we_murah'], np.minimum(df_fuzzy['mu_jarak_dekat'], np.minimum(df_fuzzy['mu_vote_avg_tinggi'], np.minimum(df_fuzzy['mu_vote_cnt_banyak'], df_fuzzy['mu_hotel_banyak'])))))
    df_fuzzy['z_R1'] = df_fuzzy['alpha_R1'] * 100

    # [R2] Rekomendasi is Tinggi
    df_fuzzy['alpha_R2'] = np.minimum(df_fuzzy['mu_htm_wd_murah'], np.minimum(df_fuzzy['mu_htm_we_murah'], np.minimum(df_fuzzy['mu_jarak_jauh'], np.minimum(df_fuzzy['mu_vote_avg_tinggi'], np.minimum(df_fuzzy['mu_vote_cnt_sedikit'], df_fuzzy['mu_hotel_sedikit'])))))
    df_fuzzy['z_R2'] = df_fuzzy['alpha_R2'] * 100

    # [R3] Rekomendasi is Tinggi
    df_fuzzy['alpha_R3'] = np.minimum(df_fuzzy['mu_htm_wd_mahal'], np.minimum(df_fuzzy['mu_htm_we_mahal'], np.minimum(df_fuzzy['mu_jarak_dekat'], np.minimum(df_fuzzy['mu_vote_avg_tinggi'], np.minimum(df_fuzzy['mu_vote_cnt_banyak'], df_fuzzy['mu_hotel_banyak'])))))
    df_fuzzy['z_R3'] = df_fuzzy['alpha_R3'] * 100

    # [R4] Rekomendasi is Rendah
    df_fuzzy['alpha_R4'] = np.minimum(df_fuzzy['mu_htm_wd_mahal'], np.minimum(df_fuzzy['mu_htm_we_mahal'], np.minimum(df_fuzzy['mu_jarak_dekat'], np.minimum(df_fuzzy['mu_vote_avg_rendah'], np.minimum(df_fuzzy['mu_vote_cnt_banyak'], df_fuzzy['mu_hotel_banyak'])))))
    df_fuzzy['z_R4'] = 100 - (df_fuzzy['alpha_R4'] * 100)

    # [R5] Rekomendasi is Rendah
    df_fuzzy['alpha_R5'] = np.minimum(df_fuzzy['mu_htm_wd_mahal'], np.minimum(df_fuzzy['mu_htm_we_mahal'], np.minimum(df_fuzzy['mu_jarak_jauh'], np.minimum(df_fuzzy['mu_vote_avg_rendah'], np.minimum(df_fuzzy['mu_vote_cnt_sedikit'], df_fuzzy['mu_hotel_sedikit'])))))
    df_fuzzy['z_R5'] = 100 - (df_fuzzy['alpha_R5'] * 100)

    # [R6] Rekomendasi is Rendah
    df_fuzzy['alpha_R6'] = np.minimum(df_fuzzy['mu_htm_wd_murah'], np.minimum(df_fuzzy['mu_htm_we_mahal'], np.minimum(df_fuzzy['mu_jarak_dekat'], np.minimum(df_fuzzy['mu_vote_avg_rendah'], np.minimum(df_fuzzy['mu_vote_cnt_banyak'], df_fuzzy['mu_hotel_banyak'])))))
    df_fuzzy['z_R6'] = 100 - (df_fuzzy['alpha_R6'] * 100)

    # 5. Defuzzifikasi (Weighted Average)
    total_alpha_z = (
        (df_fuzzy['alpha_R1'] * df_fuzzy['z_R1']) +
        (df_fuzzy['alpha_R2'] * df_fuzzy['z_R2']) +
        (df_fuzzy['alpha_R3'] * df_fuzzy['z_R3']) +
        (df_fuzzy['alpha_R4'] * df_fuzzy['z_R4']) +
        (df_fuzzy['alpha_R5'] * df_fuzzy['z_R5']) +
        (df_fuzzy['alpha_R6'] * df_fuzzy['z_R6'])
    )

    total_alpha = (
        df_fuzzy['alpha_R1'] + df_fuzzy['alpha_R2'] + df_fuzzy['alpha_R3'] + 
        df_fuzzy['alpha_R4'] + df_fuzzy['alpha_R5'] + df_fuzzy['alpha_R6']
    )

    # Menghitung skor final rekomendasi
    df_fuzzy['skor_rekomendasi'] = np.where(total_alpha > 0, total_alpha_z / total_alpha, 0)

    return df_fuzzy

def plot_kurva(judul, max_val, param_rendah, param_tinggi, label_rendah="Rendah/Murah/Dekat", label_tinggi="Tinggi/Mahal/Jauh"):
    """
    Fungsi untuk membuat objek plot grafik fungsi keanggotaan trapesium.
    """
    # Buat linspace yang rapi untuk rendering visual grafik kurva
    x_plot = np.linspace(0, max_val, 1000)
    
    # Ambil nilai fuzzy array untuk grafik
    x_universe = np.array([0, max_val])
    y_rendah = fuzz.interp_membership(x_universe, fuzz.trapmf(x_universe, param_rendah), x_plot)
    y_tinggi = fuzz.interp_membership(x_universe, fuzz.trapmf(x_universe, param_tinggi), x_plot)
    
    fig, ax = plt.subplots(figsize=(6, 2.5))
    ax.plot(x_plot, y_rendah, label=label_rendah, color='blue', linewidth=2)
    ax.plot(x_plot, y_tinggi, label=label_tinggi, color='red', linewidth=2)
    ax.set_title(f"Fungsi Keanggotaan: {judul}", fontsize=10)
    ax.set_ylabel("Derajat Keanggotaan (\u03bc)", fontsize=8)
    ax.set_ylim(-0.05, 1.05)
    ax.legend(fontsize=8, loc='center right')
    ax.grid(True, linestyle='--', alpha=0.5)
    
    plt.tight_layout()
    return fig

def dapatkan_detail_kalkulasi(df_hasil, nama_wisata):
    """
    Mengekstrak seluruh baris data komputasi fuzzy satu tempat wisata spesifik untuk trace visual.
    """
    # Cari baris yang sesuai nama wisata
    row_match = df_hasil[df_hasil['nama'] == nama_wisata]
    if row_match.empty:
        return None
        
    row = row_match.iloc[0]
    
    detail = {
        'nama': row['nama'],
        'nilai_riil': {
            'htm_weekday': row['htm_weekday'],
            'htm_weekend': row['htm_weekend'],
            'jarak_pusat_km': row['jarak_pusat_km'],
            'vote_average': row['vote_average'],
            'vote_count': row['vote_count'],
            'jumlah_hotel_terdekat': row['jumlah_hotel_terdekat']
        },
        'fuzzifikasi': {
            'htm_wd_murah': row['mu_htm_wd_murah'], 'htm_wd_mahal': row['mu_htm_wd_mahal'],
            'htm_we_murah': row['mu_htm_we_murah'], 'htm_we_mahal': row['mu_htm_we_mahal'],
            'jarak_dekat': row['mu_jarak_dekat'], 'jarak_jauh': row['mu_jarak_jauh'],
            'vote_avg_rendah': row['mu_vote_avg_rendah'], 'vote_avg_tinggi': row['mu_vote_avg_tinggi'],
            'vote_cnt_sedikit': row['mu_vote_cnt_sedikit'], 'vote_cnt_banyak': row['mu_vote_cnt_banyak'],
            'hotel_sedikit': row['mu_hotel_sedikit'], 'hotel_banyak': row['mu_hotel_banyak']
        },
        'rules': {
            'R1': {'alpha': row['alpha_R1'], 'z': row['z_R1'], 'type': 'Tinggi'},
            'R2': {'alpha': row['alpha_R2'], 'z': row['z_R2'], 'type': 'Tinggi'},
            'R3': {'alpha': row['alpha_R3'], 'z': row['z_R3'], 'type': 'Tinggi'},
            'R4': {'alpha': row['alpha_R4'], 'z': row['z_R4'], 'type': 'Rendah'},
            'R5': {'alpha': row['alpha_R5'], 'z': row['z_R5'], 'type': 'Rendah'},
            'R6': {'alpha': row['alpha_R6'], 'z': row['z_R6'], 'type': 'Rendah'},
        },
        'skor_final': row['skor_rekomendasi']
    }
    return detail