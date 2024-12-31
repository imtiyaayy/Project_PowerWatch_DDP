import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# kelas monitor listrik
class MonitorListrik:
    def __init__(self):
        """Inisialisasi kelas monitoring listrik"""
        self.peralatan = []
        self.penggunaan_harian = []
        self.tarif_listrik = {
            'R-1': 1444,  # Tarif untuk golongan R-1 (per kWh)
            'R-2': 1699,  # Tarif untuk golongan R-2 (per kWh)
            'R-3': 1699,  # Tarif untuk golongan R-3 (per kWh)
        }
        self.tarif_terpilih = 'R-1'  # Golongan R-1 sebagai default

    # 1.Peralatan Elektronik
    def tambah_peralatan(self, nama, unit, watt, golongan, jam_per_hari):
        """Menambahkan peralatan elektronik dan golongan listrik"""
        self.peralatan.append({
            'nama': nama,
            'unit': unit,
            'watt': watt,
            'total_watt': watt * unit,
            'golongan': golongan,
            'jam_per_hari': jam_per_hari,
        })
        self.update_penggunaan_harian_dengan_peralatan_baru()

    def update_penggunaan_harian_dengan_peralatan_baru(self):
        """Mengupdate penggunaan harian dengan peralatan baru"""
        if not self.penggunaan_harian:
            self.generate_sample_data()
        else:
            new_usage = np.random.uniform(1, 5)
            self.penggunaan_harian.append({
                'hari': len(self.penggunaan_harian) + 1,
                'penggunaan': new_usage
            })

    def set_tarif_listrik(self, golongan):
        """Set golongan listrik yang dipilih"""
        self.tarif_terpilih = golongan

    # 2.Penggunaan Listrik
    def hitung_total_penggunaan(self):
        """Menghitung total penggunaan listrik dalam kWh per bulan"""
        total_penggunaan_per_bulan = 0
        for peralatan in self.peralatan:
            total_penggunaan_per_bulan += (peralatan['total_watt'] / 1000) * peralatan['jam_per_hari'] * 30
        return total_penggunaan_per_bulan

    # 3.Estimasi Biaya
    def hitung_estimasi_biaya(self):
        """Menghitung estimasi biaya listrik"""
        total_penggunaan_per_bulan = self.hitung_total_penggunaan()
        tarif = self.tarif_listrik.get(self.tarif_terpilih, 1500)
        return total_penggunaan_per_bulan * tarif

    def generate_sample_data(self, hari=30):
        """Menghasilkan data penggunaan listrik sampel"""
        np.random.seed(42)
        self.penggunaan_harian = []
        for hari in range(1, hari + 1):
            penggunaan = np.random.uniform(5, 15)
            self.penggunaan_harian.append({
                'hari': hari,
                'penggunaan': penggunaan
            })

    def konsumsi_energi_per_peralatan(self):
        """Menghitung konsumsi energi per peralatan"""
        return [
            {'peralatan': peralatan['nama'], 'konsumsi': (peralatan['total_watt'] / 1000) * peralatan['jam_per_hari'] * 30}
            for peralatan in self.peralatan
        ]

# Input data
def main():
    if 'monitor' not in st.session_state:
        monitor = MonitorListrik()

        # Menambahkan peralatan default
        peralatan_default = [
            ('TV 21 inci', 1, 68, 'R-1', 8),
            ('Audio', 1, 50, 'R-1', 14),
            ('AC', 1, 430, 'R-1', 8),
            ('Komputer', 1, 140, 'R-1', 5),
            ('Game Player', 1, 20, 'R-1', 5),
            ('Lampu Bohlam', 3, 60, 'R-1', 8),
            ('Lampu Hemat Listrik', 5, 12, 'R-1', 8),
            ('Kipas Angin', 1, 103, 'R-1', 8),
            ('Microwave', 1, 1270, 'R-1', 1),
            ('Blender', 1, 130, 'R-1', 1.2),
            ('Kompor Listrik', 1, 380, 'R-1', 4),
            ('Magic jar', 1, 465, 'R-1', 9),
            ('Kulkas 120 Liter', 1, 62, 'R-1', 24),
            ('Setrika', 1, 300, 'R-1', 1),
            ('Dispenser', 1, 256, 'R-1', 24),
            ('Pemanggang Roti', 1, 380, 'R-1', 1),
            ('Mesin Cuci', 1, 550, 'R-1', 4),
            ('Pemanas Air', 1, 400, 'R-1', 2),
            ('Pompa Air', 1, 650, 'R-1', 3)
        ]

        for nama, unit, watt, golongan, jam in peralatan_default:
            monitor.tambah_peralatan(nama, unit, watt, golongan, jam)

        st.session_state.monitor = monitor

    monitor = st.session_state.monitor

# Pelajarin masing-masing 
# (yang beda baris 115)  
# elif menu == 'Peralatan Elektronik': ->  if 'Peralatan Elektronik':
# 1. Peralatan Elektronik
    if 'Peralatan Elektronik':
        st.title('Peralatan Elektronik')

        tab1, tab2 = st.tabs(["Daftar Elektronik", "Tambah Elektronik"])

        with tab1:
            if monitor.peralatan:
                data_peralatan = [{
                    'Nama Peralatan': peralatan['nama'],
                    'Golongan Listrik': peralatan['golongan'],
                    'Jumlah Unit': peralatan['unit'],
                    'Daya per Unit (Watt)': peralatan['watt'],
                    'Total Daya (Watt)': peralatan['total_watt'],
                    'Jam Penggunaan per Hari': peralatan['jam_per_hari']
                } for peralatan in monitor.peralatan]

                peralatan_df = pd.DataFrame(data_peralatan)
                st.subheader("Daftar Peralatan Elektronik")
                # Menampilkan grafik terlebih dahulu
                fig_pie = px.pie(
                    peralatan_df,
                    values='Total Daya (Watt)',
                    names='Nama Peralatan',
                    title='Distribusi Daya per Peralatan'
                )
                st.plotly_chart(fig_pie)
                # Kemudian tabel
                st.dataframe(peralatan_df)

        with tab2:
            with st.form('Tambah Peralatan', clear_on_submit=True):
                st.subheader("Formulir Tambah Peralatan Elektronik")

                col1, col2 = st.columns(2)

                with col1:
                    golongan = st.selectbox('Golongan Listrik', ['R-1', 'R-2', 'R-3'])
                    nama = st.text_input('Nama Peralatan')
                    unit = st.number_input('Jumlah Unit', min_value=1, value=1)

                with col2:
                    jam_per_hari = st.number_input('Waktu Penggunaan per Hari (Jam)', min_value=0.1, value=1.0)
                    watt = st.number_input('Daya per Unit (Watt)', min_value=1)

                submit = st.form_submit_button('Tambah')

                if submit:
                    monitor.tambah_peralatan(nama, unit, watt, golongan, jam_per_hari)
                    st.success(f'Peralatan {nama} berhasil ditambahkan!')

if __name__ == '__main__':
    main()
