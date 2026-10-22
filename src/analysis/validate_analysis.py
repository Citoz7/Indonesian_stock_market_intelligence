from pathlib import Path
import pandas as pd
import numpy as np

PROJECT_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_DIR / "data" / "processed"

prices = pd.read_csv(DATA_DIR / "stocks_combined.csv", parse_dates=["date"])
returns = pd.read_csv(DATA_DIR / "daily_returns.csv", parse_dates=["date"])
metrics = pd.read_csv(DATA_DIR / "stock_metrics.csv")

print("=== 1. VALIDASI HARGA ===")

price_columns = ["open", "high", "low", "close"]
print("Harga kosong:")
print(prices[price_columns].isna().sum())

print("\nHarga nol atau negatif:")
print((prices[price_columns] <= 0).sum())

print("\nTanggal terakhir setiap saham:")
print(prices.groupby("ticker")["date"].max().sort_values().to_string())

print("\n=== 2. VALIDASI RETURN ===")

daily_return = returns["daily_return"]

print("Daily return kosong:", daily_return.isna().sum())
print("Daily return tak hingga:", np.isinf(daily_return.dropna()).sum())
print("Daily return valid:", np.isfinite(daily_return.dropna()).sum())

print("\n=== 3. VALIDASI METRIK ===")

print("Jumlah saham:", metrics["ticker"].nunique())
print("Metrik kosong:")
print(metrics[["total_return", "annualized_volatility", "max_drawdown"]].isna().sum())

print("\n=== 4. HASIL ===")
print("Saham pada dataset:", sorted(prices["ticker"].unique()))
print("Saham pada metrik:", sorted(metrics["ticker"].unique()))
