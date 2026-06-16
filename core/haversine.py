import math

def hitung_haversine(lat1, lon1, lat2, lon2):
    """
    Menghitung jarak garis lurus antara dua titik koordinat di permukaan bumi dalam satuan Kilometer.
    """
    R = 6371.0  # Radius rata-rata bumi dalam kilometer

    # Konversi koordinat dari derajat ke radian
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    # Selisih koordinat
    dlon = lon2_rad - lon1_rad
    dlat = lat2_rad - lat1_rad

    # Rumus Haversine
    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    jarak_km = R * c
    return jarak_km