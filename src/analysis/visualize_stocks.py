from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter

# 1. Lokasi folder
PROJECT_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_DIR / "data" / "processed"
IMAGE_DIR = PROJECT_DIR / "image"

IMAGE_DIR.mkdir(parents=True, exist_ok=True)

# 2. Membaca hasil analisis
cumulative = pd.read_csv(DATA_DIR / "cumulative_returns.csv", parse_dates=["date"])

metrics = pd.read_csv(DATA_DIR / "stock_metrics.csv")
sectors = pd.read_csv(DATA_DIR / "sector_metrics.csv")

# Memastikan urutan tanggal dan saham konsisten
cumulative = cumulative.sort_values(["date", "ticker"])

print("Jumlah saham:", metrics["ticker"].nunique())
print("Jumlah baris cumulative return:", len(cumulative))

# -----------------------------------------
# GRAFIK 1: CUMULATIVE RETURN
# -----------------------------------------
fig, ax = plt.subplots(figsize=(14, 7))

for ticker, group in cumulative.groupby("ticker"):
    ax.plot(group["date"], group["cumulative_return"], label=ticker, linewidth=1.6)

ax.set_title("Cumulative Return of 10 Indonesian Stocks", fontsize=15)
ax.set_xlabel("Date")
ax.set_ylabel("Cumulative Return")
ax.yaxis.set_major_formatter(PercentFormatter(1))
ax.axhline(0, linewidth=0.8, linestyle="--")
ax.legend(title="Ticker", bbox_to_anchor=(1.02, 1), loc="upper left")
ax.grid(True, alpha=0.3)

fig.tight_layout()
fig.savefig(IMAGE_DIR / "cumulative_returns.png", dpi=150, bbox_inches="tight")
plt.close(fig)

# -----------------------------------------
# GRAFIK 2: RISK VS RETURN
# -----------------------------------------
fig, ax = plt.subplots(figsize=(10, 7))

ax.scatter(metrics["annualized_volatility"], metrics["total_return"], s=90)

for _, row in metrics.iterrows():
    ax.annotate(
        row["ticker"],
        (row["annualized_volatility"], row["total_return"]),
        xytext=(5, 5),
        textcoords="offset points",
        fontsize=8,
    )

ax.set_title("Risk vs Return by Stock", fontsize=15)
ax.set_xlabel("Annualized Volatility")
ax.set_ylabel("Total Return")
ax.xaxis.set_major_formatter(PercentFormatter(1))
ax.yaxis.set_major_formatter(PercentFormatter(1))
ax.axhline(0, linewidth=0.8, linestyle="--")
ax.grid(True, alpha=0.3)

fig.tight_layout()
fig.savefig(IMAGE_DIR / "risk_vs_return.png", dpi=150, bbox_inches="tight")
plt.close(fig)

# -----------------------------------------
# GRAFIK 3: MAXIMUM DRAWDOWN
# -----------------------------------------
drawdown_data = metrics.sort_values("max_drawdown")

fig, ax = plt.subplots(figsize=(11, 7))

ax.barh(drawdown_data["ticker"], drawdown_data["max_drawdown"])

ax.set_title("Maximum Drawdown by Stock", fontsize=15)
ax.set_xlabel("Maximum Drawdown")
ax.set_ylabel("Stock")
ax.xaxis.set_major_formatter(PercentFormatter(1))
ax.grid(axis="x", alpha=0.3)

fig.tight_layout()
fig.savefig(IMAGE_DIR / "maximum_drawdown.png", dpi=150, bbox_inches="tight")
plt.close(fig)

# -----------------------------------------
# GRAFIK 4: PERBANDINGAN SEKTOR
# -----------------------------------------
sector_data = sectors.sort_values("average_total_return")

fig, ax = plt.subplots(figsize=(11, 7))

ax.barh(sector_data["sector"], sector_data["average_total_return"])

ax.set_title("Average Total Return by Selected Sector", fontsize=15)
ax.set_xlabel("Average Total Return")
ax.set_ylabel("Sector")
ax.xaxis.set_major_formatter(PercentFormatter(1))
ax.axvline(0, linewidth=0.8, linestyle="--")
ax.grid(axis="x", alpha=0.3)

fig.tight_layout()
fig.savefig(IMAGE_DIR / "sector_comparison.png", dpi=150, bbox_inches="tight")
plt.close(fig)

print("\n=== VISUALISASI SELESAI ===")
print("File gambar tersimpan di:", IMAGE_DIR)

for filename in [
    "cumulative_returns.png",
    "risk_vs_return.png",
    "maximum_drawdown.png",
    "sector_comparison.png",
]:
    path = IMAGE_DIR / filename
    print(f"{filename}: {'OK' if path.exists() else 'GAGAL'}")
