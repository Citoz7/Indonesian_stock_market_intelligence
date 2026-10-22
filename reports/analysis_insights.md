# Analysis Insights — Indonesian Stock Market Intelligence

## 1. Project Overview

This analysis examines the historical performance and risk characteristics of 10 selected Indonesian stocks listed on the Indonesia Stock Exchange (IDX).

The analysis uses approximately three years of daily stock price data, from October 23, 2023, to October 21, 2026.

The main objectives are to:
- Compare cumulative and total returns across selected stocks.
- Evaluate annualized volatility and maximum drawdown.
- Compare average total returns across selected sectors.
- Identify differences in historical risk and return.

## 2. Key Findings

### Finding 1: ANTM.JK recorded the highest total return

ANTM.JK recorded a total return of approximately **+84.21%**, the highest among the 10 selected stocks during the observation period.

This indicates that ANTM.JK had the strongest price performance within this sample over the period analyzed.

### Finding 2: KLBF.JK recorded the lowest total return

KLBF.JK recorded a total return of approximately **-58.74%**, the lowest among the selected stocks.

Its maximum drawdown was approximately **-61.45%**, indicating a substantial decline from a previous peak during the observation period.

### Finding 3: Historical performance differed across selected sectors

The selected Mining stock recorded an average total return of approximately **+84.21%**, while the selected Energy stock recorded approximately **+25.28%**.

The selected Healthcare stock recorded approximately **-58.74%**. The Banking, Telecommunications, and Consumer and Industrial groups also had negative average total returns in this sample.

These results describe only the selected stocks and should not be interpreted as the performance of every company in each sector.

## 3. Risk and Return Considerations

Returns alone do not provide a complete picture of stock performance.

Annualized volatility measures the variability of daily returns, while maximum drawdown measures the largest peak-to-trough decline in the observed price series.

These metrics help compare historical risk characteristics alongside returns. However, they do not predict future performance or guarantee that a stock will behave similarly in the future.

## 4. Limitations

- The analysis includes only 10 selected stocks, not the entire Indonesian stock market.
- Some sectors are represented by only one stock, limiting sector-level comparisons.
- Historical performance does not guarantee future results.
- Annualized volatility is estimated using daily returns and a 252-trading-day convention.
- Prices were retrieved using Yahoo Finance through the `yfinance` Python library. Data availability and adjustments may affect results.
- The analysis is descriptive and is not investment advice.

## 5. Conclusion

The selected stocks exhibited substantial differences in historical returns, volatility, and maximum drawdown. ANTM.JK recorded the highest total return in the sample, while KLBF.JK recorded the lowest total return and the largest maximum drawdown.

The findings demonstrate how Python and Pandas can be used to collect, validate, process, and analyze historical stock market data. The results will support the next stage of the project: building an interactive Power BI dashboard.

*This project is for educational and analytical purposes only and does not constitute investment advice.*