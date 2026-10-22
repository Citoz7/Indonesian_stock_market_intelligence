
from pathlib import Path

import pandas as pd

# Menentukan lokasi proyek dan file data
PROJECT_DIR = Path(__file__).resolve().parents[2]
DATA_FILE = PROJECT_DIR / "data" / "raw" / "bbca_raw.csv"

# Memastikan file tersedia
if not DATA_FILE.exists():
    raise FileNotFoundError(f"File tidak ditemukan: {DATA_FILE}")

# Membaca CSV
df = pd.read_csv(DATA_FILE)

print("=" * 50)
print("1. UKURAN DATA")
print("=" * 50)
print(f"Jumlah baris: {df.shape[0]}")
print(f"Jumlah kolom: {df.shape[1]}")

print("\n2. NAMA KOLOM")
print(df.columns.tolist())

print("\n3. LIMA BARIS PERTAMA")
print(df.head().to_string(index=False))

print("\n4. INFORMASI TIPE DATA")
df.info()

print("\n5. NILAI KOSONG PER KOLOM")
print(df.isnull().sum())

print("\n6. JUMLAH BARIS DUPLIKAT")
print(df.duplicated().sum())

print("\n7. RENTANG TANGGAL")
if "date" in df.columns:
    dates = pd.to_datetime(df["date"], errors="coerce")
    print(f"Tanggal paling awal: {dates.min()}")
    print(f"Tanggal paling akhir: {dates.max()}")
    print(f"Tanggal yang gagal dibaca: {dates.isna().sum()}")
else:
    print("Kolom 'date' tidak ditemukan. Periksa nama kolom.")

print("\n8. RINGKASAN HARGA")
price_columns = [
    col for col in ["open", "high", "low", "close", "volume"]
    if col in df.columns
]
if price_columns:
    print(df[price_columns].describe().round(2).to_string())
else:
    print("Kolom harga yang diharapkan tidak ditemukan.")
