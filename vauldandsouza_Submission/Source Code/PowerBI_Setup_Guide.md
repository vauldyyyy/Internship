# Power BI Dashboards Setup Guide

## Overview
This project builds 7 Power BI dashboards for financial analysis of Nifty 100 companies.

## Prerequisites
- Power BI Desktop (latest version)
- PostgreSQL client or database connection
- Access to bluestock_dw database

## Connection Setup

### Step 1: Connect to PostgreSQL Database
1. Open Power BI Desktop
2. Click **Get Data** → **PostgreSQL Database**
3. Enter Server: `localhost:5432`
4. Enter Database: `bluestock_dw`
5. Import all `dim_*` and `fact_*` tables

### Step 2: Data Transformation
In Power Query Editor:
- Verify data types for all columns
- Check for null values and handle appropriately
- Create calculated columns for date fields if needed
- Remove duplicates if any

### Step 3: Create Data Model Relationships
Set these relationships in Model View:

| From Table | From Column | To Table | To Column | Cardinality |
|------------|------------|----------|-----------|------------|
| fact_profit_loss | symbol | dim_company | symbol | Many-to-One |
| fact_profit_loss | year_id | dim_year | year_id | Many-to-One |
| fact_balance_sheet | symbol | dim_company | symbol | Many-to-One |
| fact_balance_sheet | year_id | dim_year | year_id | Many-to-One |
| fact_cash_flow | symbol | dim_company | symbol | Many-to-One |
| fact_cash_flow | year_id | dim_year | year_id | Many-to-One |
| dim_company | sector | dim_sector | sector_name | Many-to-One |

## Dashboard Files

### 1. 01_executive_overview.pbix
**Purpose:** High-level market snapshot for fund managers and CXOs
**Pages:** 3
- Market Snapshot
- Sector Performance
- YoY Growth Tracker

### 2. 02_company_deep_dive.pbix
**Purpose:** Detailed analysis for individual company research
**Pages:** 4
- Financial Summary
- Profitability Analysis
- Growth Metrics
- Comparative Analysis

### 3. 03_sector_analysis.pbix
**Purpose:** Sector-level insights and trends
**Pages:** 3
- Sector Overview
- Sector Comparison
- Sector Trends

### 4. 04_valuation_metrics.pbix
**Purpose:** Valuation and relative metrics
**Pages:** 2
- Valuation Multiples
- Peer Comparison

### 5. 05_cash_flow_analysis.pbix
**Purpose:** Cash flow analysis and quality metrics
**Pages:** 2
- Cash Flow Overview
- Cash Quality Metrics

### 6. 06_ml_intelligence.pbix
**Purpose:** ML-based scoring and insights
**Pages:** 2
- Health Scores
- Investment Signal Dashboard

### 7. 07_executive_summary.pbix
**Purpose:** One-page summary for presentations
**Pages:** 1
- Executive Summary

## Key Features

### Slicers
- Company Selector (multi-select)
- Year Selector
- Sector Selector
- Health Label Filter

### Visualizations Used
- Card (KPI metrics)
- Gauge (Health scores)
- Line Chart (Trends)
- Bar Chart (Comparisons)
- Scatter Chart (Correlations)
- Heatmap/Matrix (Multi-dimensional)
- Treemap (Hierarchical data)
- Table/Matrix (Detailed data)

## Security & Performance

### Security
- Use environment variables for database password
- Never hardcode sensitive information
- Use Power BI Row-Level Security (RLS) if needed for different user roles

### Performance Optimization
- Use aggregation tables for large datasets
- Implement incremental refresh if dataset is large
- Minimize use of calculated columns; prefer measures
- Use SELECTEDVALUE() instead of ALLSELECTED() where possible

## Publishing

### To Power BI Service:
1. Click **Publish** in Power BI Desktop
2. Select workspace
3. Configure refresh schedule (daily/weekly)
4. Set up gateway if on-premises database
5. Share dashboard with stakeholders

## Troubleshooting

### Issue: "You don't have permission to access this database"
- Check database credentials
- Verify firewall allows connection to port 5432
- Ensure user has SELECT permissions on all tables

### Issue: Slow dashboard performance
- Check data volume in tables
- Consider using Import mode instead of DirectQuery
- Implement aggregation tables

### Issue: Measures showing blank values
- Verify relationships are correct
- Check filter context
- Use IFERROR() to handle division by zero

## Maintenance

### Monthly Tasks:
- Verify data refresh completed successfully
- Monitor dashboard performance metrics
- Review error logs in Power BI Service

### Quarterly Tasks:
- Update data source if schema changes
- Review and optimize DAX formulas
- Gather feedback from dashboard users

---

**Last Updated:** June 2, 2026
**Created By:** vauldandsouza
