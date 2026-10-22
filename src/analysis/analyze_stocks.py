from pathlib import Path

import numpy as np
import pandas as pd

# 1. Lokasi proyek
PROJECT_DIR = Path(__file__).resolve().parents[2]
INPUT_FILE = PROJECT_DIR / "data" / "processed" / "stocks_combined.csv"
OUTPUT_DIR = PROJECT_DIR / "data" / "processed"

# 2. Baca data
df = pd.read_csv(INPUT_FILE, parse_dates=["date"])

df = df.sort_values(["ticker", "date"]).reset_index(drop=True)

print("=== PEMERIKSAAN DATA ===")
print("Jumlah saham:", df["ticker"].nunique())
print("Jumlah baris:", len(df))
print("Rentang tanggal:", df["date"].min(), "hingga", df["date"].max())

# 3. Hitung daily return per saham
df["daily_return"] = df.groupby("ticker")["close"].pct_change()

# 4. Hitung cumulative return
# Return kumulatif berbasis perubahan close yang telah disesuaikan
df["cumulative_return"] = df.groupby("ticker")["close"].transform(
    lambda s: s / s.iloc[0] - 1
)

# 5. Hitung metrik setiap saham
metrics = []

for ticker, group in df.groupby("ticker"):
    group = group.sort_values("date").copy()

    prices = group["close"].dropna()
    returns = group["daily_return"].dropna()

    if prices.empty:
        continue

    # Nilai puncak berjalan dan drawdown
    running_peak = prices.cummax()
    drawdown = prices / running_peak - 1

    # Statistik risiko dan kinerja
    total_return = prices.iloc[-1] / prices.iloc[0] - 1

    annualized_volatility = (
        returns.std(ddof=1) * np.sqrt(252) if len(returns) > 1 else np.nan
    )

    max_drawdown = drawdown.min()

    metrics.append(
        {
            "ticker": ticker,
            "company": group["company"].iloc[0],
            "sector": group["sector"].iloc[0],
            "start_date": group["date"].min(),
            "end_date": group["date"].max(),
            "trading_days": len(prices),
            "start_close": prices.iloc[0],
            "end_close": prices.iloc[-1],
            "total_return": total_return,
            "annualized_volatility": annualized_volatility,
            "max_drawdown": max_drawdown,
            "average_daily_return": returns.mean(),
            "best_daily_return": returns.max(),
            "worst_daily_return": returns.min(),
        }
    )

metrics_df = pd.DataFrame(metrics)

# 6. Ringkasan sektor
sector_df = metrics_df.groupby("sector", as_index=False).agg(
    stock_count=("ticker", "nunique"),
    average_total_return=("total_return", "mean"),
    average_annualized_volatility=("annualized_volatility", "mean"),
    average_max_drawdown=("max_drawdown", "mean"),
)

# 7. Simpan hasil
df.to_csv(OUTPUT_DIR / "daily_returns.csv", index=False)

metrics_df.to_csv(OUTPUT_DIR / "stock_metrics.csv", index=False)

df[["date", "ticker", "company", "sector", "close", "cumulative_return"]].to_csv(
    OUTPUT_DIR / "cumulative_returns.csv", index=False
)

sector_df.to_csv(OUTPUT_DIR / "sector_metrics.csv", index=False)

# 8. Tampilkan hasil
pd.set_option("display.max_columns", None)
pd.set_option("display.width", 180)

print("\n=== METRIK PER SAHAM ===")
print(
    metrics_df[
        [
            "ticker",
            "total_return",
            "annualized_volatility",
            "max_drawdown",
            "trading_days",
        ]
    ].to_string(index=False, float_format=lambda x: f"{x:.4f}")
)

print("\n=== RINGKASAN SEKTOR ===")
print(sector_df.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

print("\nFile hasil analisis tersimpan di:", OUTPUT_DIR)
