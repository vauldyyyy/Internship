# Nifty 100 Financial Intelligence System - README

## Project Overview

A comprehensive financial intelligence platform for analyzing and visualizing the Nifty 100 index. This system provides fund managers, research analysts, and investors with deep insights into company financials, health scores, and investment signals.

**Created by:** vauldandsouza  
**Date:** June 2, 2026  
**Duration:** 8 weeks (May - June 2026)

---

## Project Structure

```
nifty100-intelligence/
├── powerbi/                    # Power BI dashboard files
│   ├── 01_executive_overview.pbix
│   ├── 02_company_deep_dive.pbix
│   ├── 03_sector_analysis.pbix
│   ├── 04_valuation_metrics.pbix
│   ├── 05_cash_flow_analysis.pbix
│   ├── 06_ml_intelligence.pbix
│   └── 07_executive_summary.pbix
├── data/                       # Data and ETL scripts
│   ├── raw/                    # Raw data files
│   ├── processed/              # Processed data
│   └── pipeline.py             # ETL pipeline script
├── docs/                       # Documentation
│   ├── schema.md               # Database schema
│   ├── api_docs.md             # API documentation
│   └── user_guide.md           # User guide
└── README.md
```

---

## Key Features

### 1. **7 Interactive Power BI Dashboards**

#### Executive Overview
- High-level market snapshot
- Sector performance analysis
- YoY growth tracking
- Audience: Fund managers, CXOs

#### Company Deep Dive
- Detailed company financial metrics
- Profitability & growth analysis
- Health score visualization
- Audience: Research analysts, individual investors

#### Sector Analysis
- Cross-company sector comparison
- Sector trends and performance
- Peer benchmarking
- Audience: Sector specialists

#### Valuation Metrics
- P/E, P/B, ROE comparisons
- Valuation multiples
- Fair value estimation
- Audience: Value investors

#### Cash Flow Analysis
- Operating, investing, financing cash flows
- Free cash flow analysis
- Cash quality metrics
- Audience: Credit analysts

#### ML Intelligence Dashboard
- AI-based health scores (0-100)
- Investment signal recommendations
- Risk scoring
- Audience: Quant teams

#### Executive Summary
- One-page view for presentations
- KPI highlights
- Quick decision-making view
- Audience: C-Suite executives

### 2. **Comprehensive Data Model**

**Dimension Tables:**
- `dim_company` - 100 Nifty companies metadata
- `dim_year` - Time dimensions (2013-2023)
- `dim_sector` - Industry sectors
- `dim_health_label` - Health classifications

**Fact Tables:**
- `fact_profit_loss` - P&L data
- `fact_balance_sheet` - Balance sheet data
- `fact_cash_flow` - Cash flow statements
- `fact_ml_scores` - ML-based health scores
- `fact_pros_cons` - Investment pros/cons
- `fact_analysis` - Analyst recommendations

### 3. **DAX Measures Library**

25+ DAX measures for financial calculations:
- ROE, OPM%, CAGR calculations
- Health score aggregations
- Sector benchmarking
- Ranking and comparisons

---

## Technologies Used

- **Data Warehouse:** PostgreSQL
- **BI Tool:** Power BI Desktop
- **ETL:** Python (pandas, psycopg2)
- **Languages:** DAX, M Query, Python
- **Database Design:** Star schema

---

## Getting Started

### Prerequisites

1. Power BI Desktop (Version 2.115 or higher)
2. PostgreSQL 12+
3. Python 3.8+
4. Required Python packages: `pandas`, `psycopg2`

### Installation

1. **Clone or download** the project files
2. **Set up PostgreSQL database:**
   ```bash
   createdb bluestock_dw
   python data/pipeline.py
   ```
3. **Open Power BI files:**
   - Open each .pbix file in Power BI Desktop
   - Update data source connection if needed

### Database Connection

1. In Power BI: **Get Data** → **PostgreSQL Database**
2. Server: `localhost:5432`
3. Database: `bluestock_dw`
4. Authentication: Username/Password

---

## Key Metrics Explained

### Financial Metrics

| Metric | Definition | Usage |
|--------|-----------|-------|
| **ROE (Return on Equity)** | Net Profit / Equity % | Profitability measure |
| **OPM (Operating Profit Margin)** | Operating Profit / Sales % | Operational efficiency |
| **CAGR** | Compound Annual Growth Rate | Growth trajectory (3-year) |
| **D/E Ratio** | Total Debt / Equity | Leverage and risk |
| **Free Cash Flow** | Operating CF - Capital Expenditure | Cash generation ability |

### Health Score Components

- **Profitability (30%)** - ROE, OPM, Margins
- **Growth (25%)** - Revenue CAGR, Profit growth
- **Leverage (20%)** - Debt-to-equity, Interest coverage
- **Liquidity (15%)** - Current ratio, Quick ratio
- **Quality (10%)** - Earnings quality, Cash conversion

---

## Data Sources

- National Stock Exchange (NSE) - Public data
- Company Annual Reports (2013-2023)
- Financial databases - Balance sheet, P&L, Cash flow
- ML model outputs - Health scores, signals

---

## Usage Guidelines

### For Fund Managers
1. Use **Executive Overview** for market snapshot
2. Filter by sector to identify opportunities
3. Check health scores in **ML Intelligence** dashboard

### For Analysts
1. Deep dive into **Company Deep Dive** dashboard
2. Analyze 5-year trends
3. Compare with sector averages
4. Review pros/cons in ML Intelligence

### For Individual Investors
1. Start with **Executive Summary**
2. Shortlist 5-10 companies
3. Compare valuations in **Valuation Metrics** dashboard
4. Review cash flow health

---

## Performance Notes

- Dashboards optimized for 100 companies × 10 years data
- Average load time: < 3 seconds
- Recommended: Refresh data weekly (Saturday evening)
- Mobile view: Responsive design for tablets

---

## Maintenance

### Weekly Tasks
- Monitor data refresh success
- Check for connection errors

### Monthly Tasks
- Review new earnings reports
- Update ML model with latest data
- Analyze dashboard usage metrics

### Quarterly Tasks
- Rebalance health score weights
- Review currency impacts
- Update sector classifications if needed

---

## Troubleshooting

### Dashboard not loading?
- Check PostgreSQL connection
- Verify firewall allows port 5432
- Ensure all tables exist in database

### Measures showing blank?
- Verify relationships in Data Model
- Check filter context
- Use IFERROR() in problematic measures

### Slow performance?
- Reduce date range in visuals
- Use Import mode instead of DirectQuery
- Check data volume in tables

---

## Future Enhancements

1. **Real-time data streaming** from NSE API
2. **Advanced ML models** for price prediction
3. **Portfolio optimization** engine
4. **Mobile app** for on-the-go access
5. **Integrated risk modeling**
6. **Sentiment analysis** from news/earnings calls

---

## Support & Documentation

- **Technical Issues:** Check troubleshooting section
- **Data Questions:** See schema.md
- **API Integration:** See api_docs.md
- **User Guide:** See user_guide.md

---

## License & Attribution

**Created as part of Bluestock Internship Program**  
All data sourced from public financial databases.

**Author:** vauldandsouza  
**Contact:** vauldandsouza@gmail.com  
**Last Updated:** June 2, 2026
