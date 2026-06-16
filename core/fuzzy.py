import numpy as np
import pandas as pd
import skfuzzy as fuzz
import matplotlib.pyplot as plt

# [R1] Jika Harga Murah, Jarak Dekat, Rating Tinggi, Ulasan Banyak, dan Hotel Banyak, maka Rekomendasi Tinggi.
# [R2] Jika Harga Murah, Jarak Jauh, Rating Tinggi, Ulasan Sedikit, dan Hotel Sedikit, maka Rekomendasi Tinggi.
# [R3] Jika Harga Mahal, Jarak Dekat, Rating Tinggi, Ulasan Banyak, dan Hotel Banyak, maka Rekomendasi Rendah.
# [R4] Jika Harga Mahal, Jarak Dekat, Rating Rendah, Ulasan Banyak, dan Hotel Banyak, maka Rekomendasi Rendah.
# [R5] Jika Harga Mahal, Jarak Jauh, Rating Rendah, Ulasan Sedikit, dan Hotel Sedikit, maka Rekomendasi Rendah.
# [R6] Jika Harga (Weekday Murah & Weekend Mahal), Jarak Dekat, Rating Rendah, Ulasan Banyak, dan Hotel Banyak, maka Rekomendasi Rendah.
# [R7] Jika Harga Weekend Mahal, Jarak Jauh, Rating Tinggi, dan Ulasan Banyak, maka Rekomendasi Rendah.
# [R8] Jika Harga Murah, Jarak Dekat, Rating Tinggi, Ulasan Banyak, dan Hotel Sedikit, maka Rekomendasi Tinggi.
# [R9] Jika Harga Murah, Jarak Jauh, Rating Tinggi, Ulasan Banyak, dan Hotel Sedikit, maka Rekomendasi Tinggi.

def hitung_fuzzy_tsukamoto(df, custom_params=None):
    df_fuzzy = df.copy()

    # [1. Pilihan Batas Parameter]
    if custom_params is None:
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

    # [3. Proses Fuzzifikasi] - LANGSUNG PASS DATA KE TRAPMF
    df_fuzzy['mu_htm_wd_murah'] = fuzz.trapmf(df_fuzzy['htm_weekday'].values, p_htm_murah)
    df_fuzzy['mu_htm_wd_mahal'] = fuzz.trapmf(df_fuzzy['htm_weekday'].values, p_htm_mahal)
    df_fuzzy['mu_htm_we_murah'] = fuzz.trapmf(df_fuzzy['htm_weekend'].values, p_htm_murah)
    df_fuzzy['mu_htm_we_mahal'] = fuzz.trapmf(df_fuzzy['htm_weekend'].values, p_htm_mahal)
    df_fuzzy['mu_jarak_dekat'] = fuzz.trapmf(df_fuzzy['jarak_pusat_km'].values, p_jarak_dekat)
    df_fuzzy['mu_jarak_jauh'] = fuzz.trapmf(df_fuzzy['jarak_pusat_km'].values, p_jarak_jauh)
    df_fuzzy['mu_vote_avg_rendah'] = fuzz.trapmf(df_fuzzy['vote_average'].values, p_vote_avg_rendah)
    df_fuzzy['mu_vote_avg_tinggi'] = fuzz.trapmf(df_fuzzy['vote_average'].values, p_vote_avg_tinggi)
    df_fuzzy['mu_vote_cnt_sedikit'] = fuzz.trapmf(df_fuzzy['vote_count'].values, p_vote_cnt_sedikit)
    df_fuzzy['mu_vote_cnt_banyak'] = fuzz.trapmf(df_fuzzy['vote_count'].values, p_vote_cnt_banyak)
    df_fuzzy['mu_hotel_sedikit'] = fuzz.trapmf(df_fuzzy['jumlah_hotel_terdekat'].values, p_hotel_sedikit)
    df_fuzzy['mu_hotel_banyak'] = fuzz.trapmf(df_fuzzy['jumlah_hotel_terdekat'].values, p_hotel_banyak)
    

    # [4. Evaluasi Rule & Inferensi Tsukamoto]
    df_fuzzy['alpha_R1'] = np.minimum(df_fuzzy['mu_htm_wd_murah'], np.minimum(df_fuzzy['mu_htm_we_murah'], np.minimum(df_fuzzy['mu_jarak_dekat'], np.minimum(df_fuzzy['mu_vote_avg_tinggi'], np.minimum(df_fuzzy['mu_vote_cnt_banyak'], df_fuzzy['mu_hotel_banyak'])))))
    df_fuzzy['z_R1'] = df_fuzzy['alpha_R1'] * 100

    df_fuzzy['alpha_R2'] = np.minimum(df_fuzzy['mu_htm_wd_murah'], np.minimum(df_fuzzy['mu_htm_we_murah'], np.minimum(df_fuzzy['mu_jarak_jauh'], np.minimum(df_fuzzy['mu_vote_avg_tinggi'], np.minimum(df_fuzzy['mu_vote_cnt_sedikit'], df_fuzzy['mu_hotel_sedikit'])))))
    df_fuzzy['z_R2'] = df_fuzzy['alpha_R2'] * 100

    df_fuzzy['alpha_R3'] = np.minimum(df_fuzzy['mu_htm_wd_mahal'], np.minimum(df_fuzzy['mu_htm_we_mahal'], np.minimum(df_fuzzy['mu_jarak_dekat'], np.minimum(df_fuzzy['mu_vote_avg_tinggi'], np.minimum(df_fuzzy['mu_vote_cnt_banyak'], df_fuzzy['mu_hotel_banyak'])))))
    df_fuzzy['z_R3'] = df_fuzzy['alpha_R3'] * 100

    df_fuzzy['alpha_R4'] = np.minimum(df_fuzzy['mu_htm_wd_mahal'], np.minimum(df_fuzzy['mu_htm_we_mahal'], np.minimum(df_fuzzy['mu_jarak_dekat'], np.minimum(df_fuzzy['mu_vote_avg_rendah'], np.minimum(df_fuzzy['mu_vote_cnt_banyak'], df_fuzzy['mu_hotel_banyak'])))))
    df_fuzzy['z_R4'] = 100 - (df_fuzzy['alpha_R4'] * 100)

    df_fuzzy['alpha_R5'] = np.minimum(df_fuzzy['mu_htm_wd_mahal'], np.minimum(df_fuzzy['mu_htm_we_mahal'], np.minimum(df_fuzzy['mu_jarak_jauh'], np.minimum(df_fuzzy['mu_vote_avg_rendah'], np.minimum(df_fuzzy['mu_vote_cnt_sedikit'], df_fuzzy['mu_hotel_sedikit'])))))
    df_fuzzy['z_R5'] = 100 - (df_fuzzy['alpha_R5'] * 100)

    df_fuzzy['alpha_R6'] = np.minimum(df_fuzzy['mu_htm_wd_murah'], np.minimum(df_fuzzy['mu_htm_we_mahal'], np.minimum(df_fuzzy['mu_jarak_dekat'], np.minimum(df_fuzzy['mu_vote_avg_rendah'], np.minimum(df_fuzzy['mu_vote_cnt_banyak'], df_fuzzy['mu_hotel_banyak'])))))
    df_fuzzy['z_R6'] = 100 - (df_fuzzy['alpha_R6'] * 100)

    # [R7] IF htm_weekend is Mahal AND jarak_pusat_km is Jauh AND vote_average is Tinggi AND vote_count is Banyak THEN Rekomendasi is Tinggi
    df_fuzzy['alpha_R7'] = np.minimum(df_fuzzy['mu_htm_we_mahal'], np.minimum(df_fuzzy['mu_jarak_jauh'], np.minimum(df_fuzzy['mu_vote_avg_tinggi'], df_fuzzy['mu_vote_cnt_banyak'])))
    df_fuzzy['z_R7'] = 100 - (df_fuzzy['alpha_R7'] * 100)

    # [R8] IF htm_weekday is Murah AND htm_weekend is Murah AND jarak_pusat_km is Dekat AND vote_average is Tinggi AND vote_count is Banyak AND jumlah_hotel_terdekat is Sedikit THEN Rekomendasi is Tinggi
    df_fuzzy['alpha_R8'] = np.minimum(df_fuzzy['mu_htm_wd_murah'], np.minimum(df_fuzzy['mu_htm_we_murah'], np.minimum(df_fuzzy['mu_jarak_dekat'], np.minimum(df_fuzzy['mu_vote_avg_tinggi'], np.minimum(df_fuzzy['mu_vote_cnt_banyak'], df_fuzzy['mu_hotel_sedikit'])))))
    df_fuzzy['z_R8'] = df_fuzzy['alpha_R8'] * 100

    # [R9] IF htm_weekday is Murah AND htm_weekend is Murah AND jarak_pusat_km is Jauh AND vote_average is Tinggi AND vote_count is Banyak AND jumlah_hotel_terdekat is Sedikit THEN Rekomendasi is Tinggi
    df_fuzzy['alpha_R9'] = np.minimum(df_fuzzy['mu_htm_wd_murah'], np.minimum(df_fuzzy['mu_htm_we_murah'], np.minimum(df_fuzzy['mu_jarak_jauh'], np.minimum(df_fuzzy['mu_vote_avg_tinggi'], np.minimum(df_fuzzy['mu_vote_cnt_banyak'], df_fuzzy['mu_hotel_sedikit'])))))
    df_fuzzy['z_R9'] = 100 - (df_fuzzy['alpha_R9'] * 100)
    
    # [5. Defuzzifikasi]
    total_alpha_z = (
        (df_fuzzy['alpha_R1'] * df_fuzzy['z_R1']) + 
        (df_fuzzy['alpha_R2'] * df_fuzzy['z_R2']) + 
        (df_fuzzy['alpha_R3'] * df_fuzzy['z_R3']) + 
        (df_fuzzy['alpha_R4'] * df_fuzzy['z_R4']) + 
        (df_fuzzy['alpha_R5'] * df_fuzzy['z_R5']) + 
        (df_fuzzy['alpha_R6'] * df_fuzzy['z_R6']) + 
        (df_fuzzy['alpha_R7'] * df_fuzzy['z_R7']) + 
        (df_fuzzy['alpha_R8'] * df_fuzzy['z_R8']) + 
        (df_fuzzy['alpha_R9'] * df_fuzzy['z_R9'])
    )
    
    total_alpha = (
        df_fuzzy['alpha_R1'] + df_fuzzy['alpha_R2'] + 
        df_fuzzy['alpha_R3'] + df_fuzzy['alpha_R4'] + 
        df_fuzzy['alpha_R5'] + df_fuzzy['alpha_R6'] + 
        df_fuzzy['alpha_R7'] + df_fuzzy['alpha_R8'] + df_fuzzy['alpha_R9']
    )
    df_fuzzy['skor_rekomendasi'] = np.where(total_alpha > 0, total_alpha_z / total_alpha, 0)

    return df_fuzzy

def plot_kurva(judul, max_val, param_rendah, param_tinggi, label_rendah="Rendah/Murah/Dekat", label_tinggi="Tinggi/Mahal/Jauh"):
    x_plot = np.linspace(0, max_val, 1000)
    
    # FIX: evaluasi x_plot ke trapmf tanpa interp_membership
    y_rendah = fuzz.trapmf(x_plot, param_rendah)
    y_tinggi = fuzz.trapmf(x_plot, param_tinggi)
    
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
            'R7': {'alpha': row['alpha_R7'], 'z': row['z_R7'], 'type': 'Rendah'}, # <-- UBAH
            'R8': {'alpha': row['alpha_R8'], 'z': row['z_R8'], 'type': 'Tinggi'},
            'R9': {'alpha': row['alpha_R9'], 'z': row['z_R9'], 'type': 'Rendah'} # <-- UBAH 
        },
        'skor_final': row['skor_rekomendasi']
    }
    return detail