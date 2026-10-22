from pathlib import Path
import pandas as pd

# 1. Menentukan lokasi folder utama proyek
PROJECT_DIR = Path(__file__).resolve().parents[2]

# 2. Menentukan lokasi file CSV
DATA_FILE = PROJECT_DIR / "data" / "raw" / "bbca_raw.csv"

print("=" * 50)
print("VALIDASI DATA SAHAM BBCA.JK")
print("=" * 50)

# 3. Memastikan file CSV tersedia
if not DATA_FILE.exists():
    raise FileNotFoundError(
        f"File data tidak ditemukan: {DATA_FILE}\n"
        "Pastikan bbca_raw.csv berada di folder data/raw/."
    )

# 4. Membaca data
df = pd.read_csv(DATA_FILE)

# 5. Memeriksa kolom wajib
required_columns = ["date", "open", "high", "low", "close", "volume", "ticker"]

missing_columns = [col for col in required_columns if col not in df.columns]

if missing_columns:
    raise ValueError(f"Kolom wajib tidak ditemukan: {missing_columns}")

# 6. Mengubah tanggal menjadi format datetime
df["date"] = pd.to_datetime(df["date"], errors="coerce")

# 7. Memeriksa data kosong
print("\n1. NILAI KOSONG")
print(df.isnull().sum().to_string())

# 8. Memeriksa duplikasi tanggal
print("\n2. JUMLAH TANGGAL DUPLIKAT")
print(df["date"].duplicated().sum())

# 9. Memeriksa urutan tanggal
print("\n3. TANGGAL SUDAH BERURUTAN")
print(df["date"].is_monotonic_increasing)

# 10. Memeriksa harga nol atau negatif
price_columns = ["open", "high", "low", "close"]

print("\n4. HARGA NOL ATAU NEGATIF")
print((df[price_columns] <= 0).sum().to_string())


# Memeriksa konsistensi harga OHLC
# Toleransi untuk mengabaikan perbedaan floating-point yang sangat kecil
tolerance = 1e-8

invalid_prices = (
    (df["high"] < df["low"] - tolerance)
    | (df["high"] < df["open"] - tolerance)
    | (df["high"] < df["close"] - tolerance)
    | (df["low"] > df["open"] + tolerance)
    | (df["low"] > df["close"] + tolerance)
)

print("\n5. BARIS DENGAN HARGA TIDAK KONSISTEN")
print(f"Jumlah baris bermasalah: {int(invalid_prices.sum())}")

if invalid_prices.any():
    print(
        df.loc[
            invalid_prices, ["date", "open", "high", "low", "close", "ticker"]
        ].to_string(index=False)
    )
else:
    print("Tidak ditemukan masalah hubungan harga.")


print("\nPemeriksaan kondisi per baris:")
print(
    df.loc[
        df["date"].dt.strftime("%Y-%m-%d").isin(["2025-10-21", "2025-11-24"]),
        ["date", "open", "high", "low", "close"],
    ]
    .assign(
        high_below_low=lambda x: x["high"] < x["low"],
        high_below_open=lambda x: x["high"] < x["open"],
        high_below_close=lambda x: x["high"] < x["close"],
        low_above_open=lambda x: x["low"] > x["open"],
        low_above_close=lambda x: x["low"] > x["close"],
    )
    .to_string(index=False)
)

# 12. Ringkasan data
print("\n6. RINGKASAN DATA")
print(f"Jumlah baris       : {len(df)}")
print(f"Jumlah kolom       : {len(df.columns)}")
print(f"Tanggal paling awal: {df['date'].min()}")
print(f"Tanggal paling akhir: {df['date'].max()}")

print("\n7. STATUS VALIDASI")

checks_passed = (
    len(df) > 0
    and df["date"].notna().all()
    and not df["date"].duplicated().any()
    and (df[price_columns] > 0).all().all()
    and not invalid_prices.any()
)

if checks_passed:
    print("LOLOS: pemeriksaan utama berhasil.")
    print("Catatan: periksa juga nilai kosong dan kelengkapan tanggal.")
else:
    print("PERLU DIPERIKSA: ditemukan masalah pada data.")

print("\nValidasi selesai.")


# print("\nPemeriksaan presisi harga:")

# for date in ["2025-10-21", "2025-11-24"]:
#     row = df.loc[df["date"].dt.strftime("%Y-%m-%d") == date].iloc[0]

#     print(f"\nTanggal: {date}")
#     print(f"High : {row['high']:.12f}")
#     print(f"Close: {row['close']:.12f}")
#     print(f"Selisih high - close: {row['high'] - row['close']:.12f}")
