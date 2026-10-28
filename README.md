# Indonesian Stock Market Intelligence

## Overview

Indonesian Stock Market Intelligence is an end-to-end data analytics project that examines the historical performance and risk characteristics of 10 Indonesian stocks.

The project uses Python for data collection, data cleaning, preprocessing, statistical analysis, and visualization. Power BI is used to build an interactive dashboard that helps users explore stock performance, returns, volatility, and maximum drawdown.

This project is intended for educational and portfolio purposes and does not provide investment advice.

## Business Questions

This project aims to answer the following questions:

- How did the selected Indonesian stocks perform over the observation period?
- Which stocks recorded the highest and lowest total returns?
- How does annualized volatility vary across stocks?
- Which stocks experienced the deepest maximum drawdowns?
- How can stock performance and risk be compared through an interactive dashboard?

## Tools and Technologies

- **Python** — data collection, transformation, analysis, and visualization
- **Pandas** — data cleaning and manipulation
- **NumPy** — numerical calculations
- **Matplotlib** — data visualization
- **Power BI Desktop** — interactive dashboard development
- **Git and GitHub** — version control and project documentation

## Project Structure

```text
Indonesian_stock_market_intelligence/
├── config/
│   └── tickers.csv
├── data/
│   ├── raw/
│   ├── processed/
│   └── external/
├── image/
├── notebook/
├── powerbi/
├── reports/
│   ├── analysis_insights.md
│   ├── data_sources.md
│   └── project_scope.md
├── src/
│   ├── data_collection/
│   ├── data_validation/
│   ├── preprocessing/
│   └── analysis/
├── .gitignore
└── README.md
```

## Data and Methodology

The project analyzes historical price data for 10 selected Indonesian stocks over approximately three years.

The workflow includes:

1. Collect historical stock price data.
2. Validate the downloaded data and check for data quality issues.
3. Clean and preprocess the data.
4. Calculate daily returns and cumulative returns.
5. Calculate total return, annualized volatility, and maximum drawdown.
6. Compare stock performance and risk across the selected stocks.
7. Build an interactive Power BI dashboard.

Refer to `reports/data_sources.md` for data source information and `reports/project_scope.md` for the project scope.

## Key Findings

The initial dashboard analysis produced the following findings:

- **Average total return:** -8.32% across the 10 selected stocks.
- **Average annualized volatility:** 34.78%.
- **Average maximum drawdown:** -61.45%.
- **Highest total return:** ANTM.JK at 84.21%.
- **Lowest total return:** KLBF.JK at -58.74%.

These findings apply only to the selected stocks and observation period. Price-based returns may not include dividends, transaction fees, or taxes. See `reports/analysis_insights.md` for additional interpretation and limitations.

## Power BI Dashboard

The dashboard is organized into three pages:

### 1. Market Overview
Provides an overview of stock closing prices, the number of analyzed stocks, average total return, and average annualized volatility.
![Market Overview](image/1.Market_Overview.png)

### 2. Risk vs Return
Compares total returns, annualized volatility, and maximum drawdown across the selected stocks.
![Risk & Return](image/2.%20Risk%26Return.png)

### 3. Stock Comparison
Provides a stock-by-stock comparison using total return, cumulative return trends, and a summary table.
![Stock Comparison](image/3.%20Stock_Comparison.png)

## How to Run

1. Clone this repository.
2. Create and activate a Python virtual environment.
3. Install the required Python packages.
4. Run the data collection, validation, preprocessing, and analysis scripts in the appropriate order.
5. Open the Power BI report in Power BI Desktop.

Example setup commands for Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install pandas numpy matplotlib yfinance
```

Run scripts from the project root directory. For example:

```bash
python src/data_collection/fetch_prices.py
python src/data_validation/check_data.py
python src/data_validation/validate_data.py
python src/preprocessing/prepare_data.py
python src/analysis/analyze_stocks.py
python src/analysis/validate_analysis.py
python src/analysis/visualize_stocks.py
```

The commands above reflect the current project workflow. If the scripts require additional packages or specific execution conditions, consult their source code before running them.

## Limitations

- The analysis covers only 10 selected stocks.
- Historical results do not predict future performance.
- Price-based returns may exclude dividends and transaction costs.
- Annualized volatility is a measure of variability, not a guarantee of future risk.
- This project is for educational purposes and is not investment advice.

## Future Improvements

- Add sector-level comparisons and analysis.
- Include dividend-adjusted returns where reliable data is available.
- Improve data quality checks and automated data refresh.
- Add more stocks and extend the observation period.
- Publish dashboard screenshots and expand the analytical findings.

## Author

Created as a data analytics portfolio project.