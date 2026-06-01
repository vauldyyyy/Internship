# Database Schema Documentation

## Overview

**Database Name:** `bluestock_dw`  
**Type:** Star Schema (Fact + Dimensions)  
**Purpose:** Financial data warehouse for Nifty 100 analysis

---

## Dimension Tables

### 1. dim_company
Stores metadata about all Nifty 100 companies.

| Column | Type | Description |
|--------|------|-------------|
| symbol | VARCHAR(20) | **PK** - Stock symbol (e.g., TCS, INFY) |
| company_name | VARCHAR(255) | Full company name |
| sector | VARCHAR(100) | Industry sector |
| market_cap | NUMERIC | Market capitalization in billions |
| created_at | TIMESTAMP | Record creation date |

**Sample Row:**
```
TCS | Tata Consultancy Services | IT | 1500.00 | 2024-01-01
```

---

### 2. dim_year
Time dimension for historical analysis.

| Column | Type | Description |
|--------|------|-------------|
| year_id | INT | **PK** - Year (2013-2023) |
| year_value | INT | Calendar year |
| quarter | INT | Quarter (optional) |

**Sample Rows:**
```
2023 | 2023 | 0
2022 | 2022 | 0
2021 | 2021 | 0
```

---

### 3. dim_sector
Industry sector classification.

| Column | Type | Description |
|--------|------|-------------|
| sector_id | SERIAL | **PK** - Sector ID |
| sector_name | VARCHAR(100) | Sector name (e.g., IT, Finance) |
| description | TEXT | Sector description |

**Sample Rows:**
```
1 | IT | Information Technology
2 | Finance | Banking & Financial Services
3 | Energy | Oil & Gas
4 | Consumer | Consumer Goods & Services
```

---

### 4. dim_health_label
Health score classifications.

| Column | Type | Description |
|--------|------|-------------|
| label_id | SERIAL | **PK** - Label ID |
| label_name | VARCHAR(50) | Label (Excellent, Good, Average, Weak) |
| score_min | INT | Minimum score for label |
| score_max | INT | Maximum score for label |

**Sample Rows:**
```
1 | Excellent | 85 | 100
2 | Good | 70 | 84
3 | Average | 50 | 69
4 | Weak | 0 | 49
```

---

## Fact Tables

### 1. fact_profit_loss
P&L statement data for companies.

| Column | Type | Description |
|--------|------|-------------|
| id | SERIAL | **PK** - Row ID |
| symbol | VARCHAR(20) | **FK** → dim_company |
| year_id | INT | **FK** → dim_year |
| sales | NUMERIC | Total revenue (in crores) |
| net_profit | NUMERIC | Net profit (in crores) |
| opm_pct | NUMERIC | Operating Profit Margin % |
| roe_pct_3y | NUMERIC | Return on Equity % (3-year avg) |
| sales_growth_3y | NUMERIC | Sales growth % (3-year CAGR) |

**Relationships:**
- (symbol, year_id) should be unique
- Links to dim_company and dim_year

---

### 2. fact_balance_sheet
Balance sheet snapshot for each year.

| Column | Type | Description |
|--------|------|-------------|
| id | SERIAL | **PK** - Row ID |
| symbol | VARCHAR(20) | **FK** → dim_company |
| year_id | INT | **FK** → dim_year |
| total_assets | NUMERIC | Total assets (in crores) |
| total_debt | NUMERIC | Total debt (in crores) |
| equity | NUMERIC | Shareholder equity (in crores) |

**Key Calculations:**
- Debt-to-Equity = total_debt / equity
- Asset Turn = sales / total_assets

---

### 3. fact_cash_flow
Cash flow statement data.

| Column | Type | Description |
|--------|------|-------------|
| id | SERIAL | **PK** - Row ID |
| symbol | VARCHAR(20) | **FK** → dim_company |
| year_id | INT | **FK** → dim_year |
| operating_cf | NUMERIC | Operating cash flow (in crores) |
| investing_cf | NUMERIC | Investing cash flow (in crores) |
| financing_cf | NUMERIC | Financing cash flow (in crores) |
| free_cf | NUMERIC | Free cash flow (in crores) |

**Validation Rule:**
- operating_cf + investing_cf + financing_cf ≈ change in cash

---

### 4. fact_ml_scores
ML model outputs for health assessment.

| Column | Type | Description |
|--------|------|-------------|
| id | SERIAL | **PK** - Row ID |
| symbol | VARCHAR(20) | **FK** → dim_company |
| overall_score | NUMERIC | Health score (0-100) |
| health_label | VARCHAR(50) | Label (Excellent, Good, etc.) |

**Score Methodology:**
- Profitability: 30%
- Growth: 25%
- Leverage: 20%
- Liquidity: 15%
- Quality: 10%

---

### 5. fact_pros_cons
Investment reasoning and analysis.

| Column | Type | Description |
|--------|------|-------------|
| id | SERIAL | **PK** - Row ID |
| symbol | VARCHAR(20) | **FK** → dim_company |
| pros_text | TEXT | Positive factors |
| cons_text | TEXT | Risk factors |

---

### 6. fact_analysis
Analyst recommendations and ratings.

| Column | Type | Description |
|--------|------|-------------|
| id | SERIAL | **PK** - Row ID |
| symbol | VARCHAR(20) | **FK** → dim_company |
| year_id | INT | **FK** → dim_year |
| rating | VARCHAR(10) | Buy/Hold/Sell |
| recommendation | TEXT | Detailed recommendation |

---

## Relationships (Star Schema)

```
                    dim_company
                        ↑
                   (symbol, FK)
                        
fact_profit_loss ←← (symbol, year_id) ←→ dim_year
fact_balance_sheet                           ↑
fact_cash_flow                           (year_id, FK)
fact_ml_scores
fact_pros_cons
fact_analysis
```

---

## Key Indexes

```sql
-- Performance optimization
CREATE INDEX idx_fact_pl_symbol ON fact_profit_loss(symbol);
CREATE INDEX idx_fact_pl_year ON fact_profit_loss(year_id);
CREATE INDEX idx_fact_bs_symbol ON fact_balance_sheet(symbol);
CREATE INDEX idx_fact_cf_symbol ON fact_cash_flow(symbol);
CREATE INDEX idx_fact_ml_symbol ON fact_ml_scores(symbol);
```

---

## Data Quality Rules

1. **Referential Integrity:**
   - All symbols must exist in dim_company
   - All year_ids must exist in dim_year

2. **Value Constraints:**
   - Sales, Net Profit, Assets: >= 0
   - Percentages (OPM, ROE): -100 to 100
   - Health Scores: 0-100
   - ML Labels: Must match dim_health_label

3. **Temporal Consistency:**
   - No future years
   - Years in ascending order (2013-2023)

---

## Data Dictionary

### Financial Metrics

| Term | Formula | Unit |
|------|---------|------|
| OPM | Operating Profit / Sales | % |
| ROE | Net Profit / Equity | % |
| CAGR | (Ending Value / Starting Value) ^ (1/years) - 1 | % |
| D/E | Total Debt / Equity | Ratio |
| Free CF | Operating CF - Capex | Crores |

---

## Sample Queries

### Top 10 Companies by ROE
```sql
SELECT 
    c.company_name,
    ROUND(AVG(f.roe_pct_3y), 2) AS avg_roe
FROM fact_profit_loss f
JOIN dim_company c ON f.symbol = c.symbol
WHERE f.year_id = 2023
GROUP BY c.symbol, c.company_name
ORDER BY avg_roe DESC
LIMIT 10;
```

### Sector Performance Summary
```sql
SELECT 
    s.sector_name,
    COUNT(DISTINCT c.symbol) AS company_count,
    ROUND(AVG(f.sales), 0) AS avg_sales,
    ROUND(AVG(f.roe_pct_3y), 2) AS avg_roe
FROM fact_profit_loss f
JOIN dim_company c ON f.symbol = c.symbol
JOIN dim_sector s ON c.sector = s.sector_name
WHERE f.year_id = 2023
GROUP BY s.sector_name
ORDER BY avg_roe DESC;
```

---

## Maintenance

- **Backup Frequency:** Daily
- **Refresh Schedule:** Weekly (Saturdays)
- **Archive Policy:** Keep 10 years of history
- **Storage Size:** ~2-5 GB for 100 companies × 10 years

---

**Last Updated:** June 2, 2026
