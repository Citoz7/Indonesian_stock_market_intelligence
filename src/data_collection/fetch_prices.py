
from pathlib import Path

import pandas as pd
import yfinance as yf

# 1. Menentukan lokasi folder proyek
PROJECT_DIR = Path(__file__).resolve().parents[2]
CONFIG_FILE = PROJECT_DIR / "config" / "tickers.csv"
RAW_DIR = PROJECT_DIR / "data" / "raw"

RAW_DIR.mkdir(parents=True, exist_ok=True)

# 2. Membaca konfigurasi ticker
if not CONFIG_FILE.exists():
    raise FileNotFoundError(
        f"File konfigurasi tidak ditemukan: {CONFIG_FILE}"
    )

tickers_df = pd.read_csv(CONFIG_FILE)

required_columns = ["ticker", "company", "sector"]
missing_columns = [
    col for col in required_columns if col not in tickers_df.columns
]

if missing_columns:
    raise ValueError(f"Kolom konfigurasi hilang: {missing_columns}")

tickers_df["ticker"] = tickers_df["ticker"].astype(str).str.strip()
tickers_df = tickers_df.dropna(subset=["ticker"])
tickers_df = tickers_df[tickers_df["ticker"] != ""]

if tickers_df["ticker"].duplicated().any():
    raise ValueError("Ada ticker duplikat di tickers.csv.")

print(f"Jumlah ticker yang akan diproses: {len(tickers_df)}")

# 3. Mengunduh data setiap saham
results = []

for ticker in tickers_df["ticker"]:
    print(f"\nMengambil data: {ticker}")

    try:
        df = yf.Ticker(ticker).history(
            period="3y",
            interval="1d",
            auto_adjust=True
        )

        if df.empty:
            print(f"GAGAL: Tidak ada data untuk {ticker}.")
            results.append({
                "ticker": ticker,
                "status": "FAILED",
                "rows": 0,
                "message": "Data kosong"
            })
            continue

        # 4. Merapikan kolom
        df = df.reset_index()
        df.columns = [
            str(col).lower().replace(" ", "_")
            for col in df.columns
        ]

        df["ticker"] = ticker

        # 5. Menyimpan CSV hanya setelah data berhasil diperoleh
        output_file = RAW_DIR / (
            ticker.replace(".", "_").replace("/", "_") + "_raw.csv"
        )
        df.to_csv(output_file, index=False)

        print(f"Berhasil: {len(df)} baris")
        print(f"File: {output_file}")

        results.append({
            "ticker": ticker,
            "status": "SUCCESS",
            "rows": len(df),
            "message": ""
        })

    except Exception as exc:
        print(f"GAGAL mengambil {ticker}: {exc}")
        results.append({
            "ticker": ticker,
            "status": "FAILED",
            "rows": 0,
            "message": str(exc)
        })

# 6. Menyimpan ringkasan hasil pengambilan data
summary = pd.DataFrame(results)
summary_file = RAW_DIR / "collection_summary.csv"
summary.to_csv(summary_file, index=False)

print("\n" + "=" * 50)
print("RINGKASAN PENGAMBILAN DATA")
print("=" * 50)
print(summary.to_string(index=False))
print(f"\nRingkasan tersimpan di: {summary_file}")
print(f"Berhasil: {(summary['status'] == 'SUCCESS').sum()}")
print(f"Gagal: {(summary['status'] == 'FAILED').sum()}")
