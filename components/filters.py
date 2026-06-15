import streamlit as st

def render_parameter_expander():
    with st.expander("⚙️ Sesuaikan Parameter Fuzzy (Opsional)", expanded=False):
        st.markdown("Geser slider di bawah ini jika kamu ingin mengubah definisi 'Murah', 'Dekat', atau 'Tinggi'.")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("** Harga Tiket (Rp)**")
            htm_batas = st.slider("Batas Murah - Mahal", 10000, 100000, (10000, 50000), step=5000)
            
        with col2:
            st.markdown("** Jarak dari Pusat (KM)**")
            jarak_batas = st.slider("Batas Dekat - Jauh", 2, 40, (5, 25), step=1)
            
        with col3:
            st.markdown("** Rating (Vote Average)**")
            rating_batas = st.slider("Batas Rendah - Tinggi", 2.0, 5.0, (3.5, 4.5), step=0.1)

        # Mapping nilai slider ke format trapesium [a, b, c, d]
        custom_params = {
            'htm_murah': [0, 0, htm_batas[0], htm_batas[1]],
            'htm_mahal': [htm_batas[0], htm_batas[1], 500000, 500000],
            
            'jarak_dekat': [0, 0, jarak_batas[0], jarak_batas[1]],
            'jarak_jauh': [jarak_batas[0], jarak_batas[1], 60, 60],
            
            'vote_avg_rendah': [1.0, 1.0, rating_batas[0], rating_batas[1]],
            'vote_avg_tinggi': [rating_batas[0], rating_batas[1], 5.0, 5.0],
            
            # Default untuk vote count dan hotel agar UI tidak terlalu penuh
            'vote_cnt_sedikit': [0, 0, 100, 1000],
            'vote_cnt_banyak': [100, 1000, 82000, 82000],
            'hotel_sedikit': [0, 0, 5, 50],
            'hotel_banyak': [5, 50, 524, 524]
        }
        
        return custom_params