# Bike Sharing Analytics Dashboard

Dashboard interaktif untuk mengeksplorasi data penyewaan sepeda selama 2011-2012. Proyek ini dibuat menggunakan Streamlit dan dilengkapi notebook analisis data.

## Isi Dashboard

- Ringkasan total penyewaan, pengguna terdaftar, dan pengguna kasual.
- Perbandingan rata-rata penyewaan pada jam sibuk (08.00 dan 17.00) di musim gugur antara 2011 dan 2012.
- Hubungan kelembapan udara dengan jumlah pengguna kasual pada akhir pekan atau hari libur.
- Pola penyewaan berdasarkan kelompok waktu, tipe pengguna, dan jenis hari.
- Filter interaktif berdasarkan rentang tanggal dan musim.

## Struktur Proyek

```text
.
|-- Proyek_Analisis_Data.ipynb
|-- README.md
|-- requirements.txt
`-- dashboard
    |-- dashboard.py
    `-- main_data.csv
```

## Setup Environment - Anaconda

Buka Anaconda Prompt atau terminal, lalu jalankan:

```bash
conda create --name bike-sharing-dashboard python=3.11
conda activate bike-sharing-dashboard
python -m pip install -r requirements.txt
```

Jalankan perintah dari folder utama proyek, yaitu folder yang berisi `requirements.txt`.

## Setup Environment - Windows PowerShell

```powershell
cd "D:\Proyek Analisis Data Asah"
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Jika PowerShell menolak aktivasi environment karena kebijakan eksekusi, gunakan Command Prompt:

```bat
cd /d "D:\Proyek Analisis Data Asah"
py -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
```

## Menjalankan Dashboard

Dari folder utama proyek dengan environment aktif, jalankan:

```bash
python -m streamlit run dashboard/dashboard.py
```

Di Windows PowerShell, pemisah path berikut juga dapat digunakan:

```powershell
py -m streamlit run dashboard\dashboard.py
```

Streamlit akan menampilkan alamat lokal di terminal, biasanya `http://localhost:8501`. Buka alamat tersebut di browser.


