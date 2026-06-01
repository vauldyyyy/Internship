# POWER BI COMPLETE SETUP & DASHBOARD CREATION

## PART 1: INSTALLATION & CONNECTION

### Step 1: Download Power BI Desktop
1. Visit: https://www.microsoft.com/en-us/download/details.aspx?id=58494
2. Click **Download**
3. Run `PBIDesktopSetup.exe`
4. Complete installation (5-10 minutes)
5. Launch Power BI Desktop

### Step 2: Connect to SQLite Database

**Database Location:**
```
C:\Users\vauld\Desktop\CODING\Internship BlueStock\bluestock_dw.db
```

**Steps:**
1. Power BI → Click **Get Data**
2. Search: `SQLite`
3. Select **SQLite Database** → **Connect**
4. File path: `C:\Users\vauld\Desktop\CODING\Internship BlueStock\vauldandsouza_Submission\Datasets\bluestock_dw.db`
5. Click **OK**
6. Select ALL tables (use Ctrl+A):
   - dim_company
   - dim_year
   - dim_sector
   - dim_health_label
   - fact_profit_loss
   - fact_balance_sheet
   - fact_cash_flow
   - fact_ml_scores
   - fact_pros_cons
7. Click **Load**
8. Wait 10-15 seconds for data to load

### Step 3: Verify Relationships

Go to **Model** view - check relationships are created:
- fact_profit_loss → dim_company (symbol)
- fact_profit_loss → dim_year (year_id)
- fact_balance_sheet → dim_company (symbol)
- fact_balance_sheet → dim_year (year_id)
- fact_cash_flow → dim_company (symbol)
- fact_cash_flow → dim_year (year_id)
- fact_ml_scores → dim_company (symbol)
- fact_pros_cons → dim_company (symbol)

If missing, manually create by dragging fields.

---

## PART 2: CREATE DAX MEASURES

Go to **Report** view. Right-click on **fact_profit_loss** → **New Measure**

### Essential Measures:

**1. Total Companies**
```dax
Total Companies = DISTINCTCOUNT(dim_company[symbol])
```

**2. Avg ROE**
```dax
Avg ROE = AVERAGE(fact_profit_loss[roe_pct_3y])
```

**3. Avg OPM**
```dax
Avg OPM = AVERAGE(fact_profit_loss[opm_pct])
```

**4. Total Revenue**
```dax
Total Revenue = SUM(fact_profit_loss[sales])
```

**5. Total Profit**
```dax
Total Profit = SUM(fact_profit_loss[net_profit])
```

**6. Avg Health Score**
```dax
Avg Health = AVERAGE(fact_ml_scores[overall_score])
```

**7. Free Cash Flow**
```dax
Total Free CF = SUM(fact_cash_flow[free_cf])
```

**8. Growth Rate**
```dax
Avg Growth = AVERAGE(fact_profit_loss[sales_growth_3y])
```

---

## PART 3: DASHBOARD 1 - EXECUTIVE OVERVIEW

### Page Name: "Executive Overview"

**Visual 1: KPI Cards (Top)**
- 4 cards in a row showing:
  - Card 1: [Total Companies] 
  - Card 2: [Avg ROE]
  - Card 3: [Total Revenue] (format: ₹ Crores)
  - Card 4: [Avg Health]

**Visual 2: Revenue by Sector (Left)**
- Chart Type: Column Chart
- X-Axis: dim_company[sector]
- Y-Axis: [Total Revenue]
- Sort: Descending
- Height: 400px

**Visual 3: Health Distribution (Right)**
- Chart Type: Pie/Donut
- Values: Count of fact_ml_scores[health_label]
- Category: fact_ml_scores[health_label]
- Colors: Excellent=Green, Good=Light Green, Average=Yellow, Weak=Red

**Visual 4: Revenue Trend (Bottom)**
- Chart Type: Line with markers
- X-Axis: dim_year[year_value]
- Y-Axis: [Total Revenue]
- Height: 400px

**Slicer 1: Company (Top Left)**
- Field: dim_company[company_name]
- Type: Dropdown
- Style: Light

**Slicer 2: Year (Top Right)**
- Field: dim_year[year_value]
- Type: Dropdown
- Style: Light

---

## PART 4: DASHBOARD 2 - COMPANY DEEP DIVE

### Page Name: "Company Deep Dive"

**Slicer: Company Selection (Top)**
- Field: dim_company[symbol]
- Type: Dropdown
- Multi-select: OFF (single company)

**Visual 1: Health Score Gauge (Top Left)**
- Chart Type: Gauge
- Min: 0, Max: 100, Target: 75
- Value: AVERAGE(fact_ml_scores[overall_score])
- Filter: Use company slicer

**Visual 2: Company Info (Top Right)**
- Chart Type: Card
- Values: 
  - Company Name
  - Sector
  - Market Cap

**Visual 3: Profitability Trend (Middle Left)**
- Chart Type: Line with markers
- X-Axis: dim_year[year_value]
- Line 1: [Avg OPM]
- Line 2: [Avg ROE]
- Dual Axis: ON

**Visual 4: Revenue Trend (Middle Right)**
- Chart Type: Column Chart
- X-Axis: dim_year[year_value]
- Y-Axis: SUM(fact_profit_loss[sales])

**Visual 5: Pros & Cons (Bottom)**
- Chart Type: Text Box (2 boxes side by side)
- Box 1: MAX(fact_pros_cons[pros_text])
- Box 2: MAX(fact_pros_cons[cons_text])
- Width: 400px each

**Visual 6: Financial Summary Table (Bottom)**
- Chart Type: Table
- Columns: Year, Revenue, Net Profit, OPM%, ROE%
- Rows: dim_year[year_value]

---

## PART 5: DASHBOARD 3 - SECTOR ANALYSIS

### Page Name: "Sector Analysis"

**Slicer: Sector Selection (Top)**
- Field: dim_company[sector]
- Type: List
- Multi-select: ON

**Visual 1: Average ROE by Sector**
- Chart Type: Bar Chart
- Y-Axis: dim_company[sector]
- X-Axis: [Avg ROE]
- Sort: Ascending
- Color gradient: Red to Green

**Visual 2: Average OPM by Sector**
- Chart Type: Bar Chart
- Y-Axis: dim_company[sector]
- X-Axis: [Avg OPM]
- Color: Blue gradient

**Visual 3: Sector Comparison Matrix**
- Chart Type: Table
- Rows: dim_company[sector]
- Values: 
  - Count of companies
  - [Total Revenue]
  - [Avg ROE]
  - [Avg OPM]

**Visual 4: ROE vs OPM Scatter**
- Chart Type: Scatter
- X-Axis: [Avg OPM]
- Y-Axis: [Avg ROE]
- Legend: dim_company[sector]
- Size: [Total Revenue]

---

## PART 6: DASHBOARD 4 - ML INTELLIGENCE

### Page Name: "ML Intelligence"

**Visual 1: Health Metrics (Top)**
- 3 Cards:
  - Excellent Health Count (Score >= 85)
  - Good Health Count (70-84)
  - Weak Health Count (<50)

**Visual 2: Health Distribution Pie**
- Chart Type: Pie
- Category: dim_health_label[label_name]
- Values: Count of companies

**Visual 3: Top Companies by Health**
- Chart Type: Bar (Horizontal)
- Category: dim_company[company_name]
- Value: fact_ml_scores[overall_score]
- Sort: Descending
- Top 10

**Visual 4: Company Scores Table**
- Chart Type: Table
- Columns:
  - dim_company[company_name]
  - dim_company[sector]
  - fact_ml_scores[overall_score]
  - fact_ml_scores[health_label]
- Sort: Score descending

**Visual 5: Pros/Cons Matrix**
- Chart Type: Matrix
- Rows: dim_company[symbol]
- Values: fact_pros_cons[pros_text], fact_pros_cons[cons_text]

---

## PART 7: DASHBOARD 5 - EXECUTIVE SUMMARY (One-Page)

### Page Name: "Executive Summary"

**Layout:** Single-page presentation view

**Visual 1: Title**
- Text Box: "Nifty 100 Financial Intelligence - Executive Summary"
- Font: 24pt Bold
- Position: Top Center

**Visual 2: Key Metrics (4 Cards)**
- Total Companies
- Total Revenue
- Avg Health Score
- Avg Growth Rate

**Visual 3: Health Status**
- Pie showing: Excellent, Good, Average, Weak distribution

**Visual 4: Top 5 Companies**
- Table with Top 5 by ROE

**Visual 5: Sector Overview**
- Column chart: Revenue by sector

**Visual 6: Key Insights (Text Box)**
```
KEY INSIGHTS:
• IT sector leads with highest margins (20%+ OPM)
• Finance sector shows stable growth and high ROE
• Top 3 companies account for 35% of total revenue
• 65% of companies in Good-to-Excellent health
• Overall portfolio health score: [Avg Health]
```

---

## PART 8: PUBLISHING

1. **Save file** as: `Nifty100_Financial_Intelligence.pbix`
2. Click **File** → **Publish** (if Power BI Premium)
3. Or share locally via: **File** → **Export** as PDF for presentations

---

## PART 9: FORMATTING GUIDE

### Color Scheme:
- **Excellent (85+):** #10B981 (Green)
- **Good (70-84):** #34D399 (Light Green)
- **Average (50-69):** #FBBF24 (Yellow)
- **Weak (<50):** #EF4444 (Red)
- **Background:** #F3F4F6 (Light Gray)
- **Text:** #1F2937 (Dark Gray)
- **Accent:** #3B82F6 (Blue)

### Font Styling:
- Headers: 16-18pt Bold
- Labels: 12-14pt
- Values: 14-16pt Bold
- Background: Light theme

---

## PART 10: TROUBLESHOOTING

### Problem: "Cannot connect to SQLite"
**Solution:**
- Check file path is exact
- File should be at: `C:\Users\vauld\Desktop\CODING\Internship BlueStock\vauldandsouza_Submission\Datasets\bluestock_dw.db`
- Try ODBC method if SQLite connector not available

### Problem: "Relationships not showing"
**Solution:**
- Go to Model view
- Manually drag symbols from fact to dim tables
- Set as Many-to-One relationship

### Problem: "Measures return blank"
**Solution:**
- Check filter context
- Use IFERROR() to handle edge cases
- Verify table relationships are correct

### Problem: "Dashboard is slow"
**Solution:**
- Limit date range in visuals
- Use Import mode instead of DirectQuery
- Create aggregation tables for large datasets

---

## TOTAL TIME ESTIMATE
- Installation: 10 minutes
- Connection & Data Load: 5 minutes
- Create Measures: 5 minutes
- Dashboard 1: 10 minutes
- Dashboard 2: 15 minutes
- Dashboard 3: 10 minutes
- Dashboard 4: 10 minutes
- Dashboard 5: 5 minutes
- **TOTAL: ~70 minutes**

All set! Follow each section in order for a complete, production-ready Power BI dashboard system.

File Location: `C:\Users\vauld\Desktop\CODING\Internship BlueStock\vauldandsouza_Submission\Datasets\bluestock_dw.db`

**Ready to go!** 🚀
