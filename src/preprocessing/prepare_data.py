from pathlib import Path
import pandas as pd

PROJECT_DIR = Path(__file__).resolve().parents[2]
RAW_DIR = PROJECT_DIR / "data" / "raw"
PROCESSED_DIR = PROJECT_DIR / "data" / "processed"
CONFIG_FILE = PROJECT_DIR / "config" / "tickers.csv"

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

# 1. Baca konfigurasi
tickers_df = pd.read_csv(CONFIG_FILE)
tickers_df.columns = tickers_df.columns.str.strip().str.lower()

required = ["ticker", "company", "sector"]
missing = [col for col in required if col not in tickers_df.columns]

if missing:
    raise ValueError(
        f"Kolom konfigurasi hilang: {missing}. "
        f"Kolom yang ditemukan: {tickers_df.columns.tolist()}"
    )

print("Jumlah ticker dalam konfigurasi:", len(tickers_df))
print("Folder data mentah:", RAW_DIR)

all_data = []

# 2. Baca data tiap saham
for _, stock in tickers_df.iterrows():
    ticker = str(stock["ticker"]).strip()
    company = stock["company"]
    sector = stock["sector"]

    filename = ticker.replace(".", "_") + "_raw.csv"
    file_path = RAW_DIR / filename

    print(f"\nMemproses {ticker}")
    print("File yang dicari:", filename)

    if not file_path.exists():
        print("GAGAL: File tidak ditemukan.")
        continue

    try:
        df = pd.read_csv(file_path)

        # Seragamkan nama kolom
        df.columns = (
            df.columns.astype(str)
            .str.strip()
            .str.lower()
            .str.replace(" ", "_", regex=False)
        )

        print("Kolom yang ditemukan:", df.columns.tolist())

        # Cari kolom tanggal
        date_column = next(
            (col for col in ["date", "datetime", "timestamp"] if col in df.columns),
            None,
        )

        if date_column is None:
            print("GAGAL: Kolom tanggal tidak ditemukan.")
            continue

        # Ubah tanggal menjadi format datetime
        df["date"] = (
            pd.to_datetime(df[date_column], errors="coerce", utc=True)
            .dt.tz_convert("Asia/Jakarta")
            .dt.tz_localize(None)
        )

        if date_column != "date":
            df = df.drop(columns=[date_column])

        df = df.dropna(subset=["date"])

        if df.empty:
            print("GAGAL: Semua tanggal kosong atau tidak valid.")
            continue

        # Tambahkan informasi saham dari konfigurasi
        df["ticker"] = ticker
        df["company"] = company
        df["sector"] = sector

        all_data.append(df)
        print(f"BERHASIL: {len(df)} baris")

    except Exception as exc:
        print(f"GAGAL membaca {ticker}: {exc}")

# 3. Gabungkan data
if not all_data:
    raise ValueError(
        "Tidak ada data yang berhasil dibaca. "
        "Periksa pesan GAGAL yang muncul di atas."
    )

combined_df = pd.concat(all_data, ignore_index=True)

# 4. Pastikan kolom harga tersedia
price_columns = ["open", "high", "low", "close", "volume"]
missing_prices = [col for col in price_columns if col not in combined_df.columns]

if missing_prices:
    raise ValueError(f"Kolom harga tidak ditemukan: {missing_prices}")

# 5. Bersihkan duplikat dan urutkan
combined_df = combined_df.drop_duplicates(subset=["ticker", "date"])

combined_df = combined_df.sort_values(["ticker", "date"]).reset_index(drop=True)

# 6. Susun kolom utama
preferred = [
    "date",
    "ticker",
    "company",
    "sector",
    "open",
    "high",
    "low",
    "close",
    "volume",
    "dividends",
    "stock_splits",
]

ordered = [col for col in preferred if col in combined_df.columns]
other = [col for col in combined_df.columns if col not in ordered]
combined_df = combined_df[ordered + other]

# 7. Simpan hasil
output_file = PROCESSED_DIR / "stocks_combined.csv"
combined_df.to_csv(output_file, index=False)

# 8. Tampilkan laporan
print("\n========== HASIL PREPROCESSING ==========")
print("Jumlah saham:", combined_df["ticker"].nunique())
print("Jumlah baris:", len(combined_df))
print("Tanggal awal:", combined_df["date"].min())
print("Tanggal akhir:", combined_df["date"].max())
print("Duplikat ticker-date:", combined_df.duplicated(["ticker", "date"]).sum())

print("\nJumlah baris per saham:")
print(combined_df.groupby("ticker").size().to_string())

print("\nData kosong per kolom:")
print(combined_df.isna().sum().to_string())

print("\nFile tersimpan di:", output_file)
