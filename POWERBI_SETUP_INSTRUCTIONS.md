# POWER BI SETUP GUIDE - NIFTY 100 DASHBOARD

## Step 1: Download & Install Power BI Desktop

1. Go to: https://www.microsoft.com/en-us/download/details.aspx?id=58494
2. Click **Download**
3. Run the installer (PBIDesktopSetup.exe)
4. Follow installation wizard (takes ~5-10 minutes)
5. Sign in with Microsoft account (create free account if needed)
6. Launch Power BI Desktop

## Step 2: Connect to SQLite Database

### Option A: Direct SQLite Connection (Recommended)

1. In Power BI Desktop, click **Get Data**
2. Search for **SQLite** in the search box
3. Click **SQLite Database** → **Connect**
4. Browse to: `C:\Users\vauld\Desktop\CODING\Internship BlueStock\bluestock_dw.db`
5. Click **OK**
6. A dialog shows all tables - **Select all** tables:
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

**Wait 10-15 seconds for data to load**

### Option B: ODBC Connection (If SQLite connector not available)

1. **Install SQLite ODBC Driver:**
   - Download: http://www.ch-werner.de/sqliteodbc/
   - Run installer
   - Select "Install for current user"

2. **In Power BI:**
   - Click **Get Data** → **ODBC**
   - Set up new DSN:
     - Go to Windows Control Panel → Administrative Tools → ODBC Data Sources
     - Click **Add** (User DSN)
     - Driver: **SQLite3 ODBC Driver**
     - Data Source Name: `bluestock_dw`
     - Database: `C:\Users\vauld\Desktop\CODING\Internship BlueStock\bluestock_dw.db`
     - Click **OK**
   - Back in Power BI: Select `bluestock_dw` DSN → **OK**

## Step 3: Create Data Model Relationships

After loading tables, you'll see the **Model view** with relationships:

**Expected relationships (should auto-detect):**
- fact_profit_loss[symbol] → dim_company[symbol]
- fact_profit_loss[year_id] → dim_year[year_id]
- fact_balance_sheet[symbol] → dim_company[symbol]
- fact_balance_sheet[year_id] → dim_year[year_id]
- fact_cash_flow[symbol] → dim_company[symbol]
- fact_cash_flow[year_id] → dim_year[year_id]
- fact_ml_scores[symbol] → dim_company[symbol]
- fact_pros_cons[symbol] → dim_company[symbol]

**If relationships don't auto-create:**
1. Drag symbol from fact_profit_loss to dim_company[symbol]
2. Set relationship: **Many-to-One**
3. Repeat for other fact tables

## Step 4: Create DAX Measures

Go to **Report** view. Right-click on any Fact table → **New Measure**

**Create these essential measures:**

### 1. Average ROE
```dax
Avg ROE = AVERAGE(fact_profit_loss[roe_pct_3y])
```

### 2. Average OPM
```dax
Avg OPM = AVERAGE(fact_profit_loss[opm_pct])
```

### 3. Total Revenue
```dax
Total Revenue = SUM(fact_profit_loss[sales])
```

### 4. Total Net Profit
```dax
Total Net Profit = SUM(fact_profit_loss[net_profit])
```

### 5. Average Health Score
```dax
Avg Health Score = AVERAGE(fact_ml_scores[overall_score])
```

### 6. Company Count
```dax
Company Count = DISTINCTCOUNT(dim_company[symbol])
```

### 7. Total Cash Flow
```dax
Total Free CF = SUM(fact_cash_flow[free_cf])
```

## Step 5: Create Dashboard Pages

Click **+ Page** to add new pages for each dashboard.

### PAGE 1: Executive Overview

**Visuals to add:**

1. **Card - Total Companies**
   - Value: Company Count
   - Format: Number, no decimals

2. **Card - Avg ROE**
   - Value: Avg ROE
   - Format: Percentage, 1 decimal

3. **Card - Total Revenue**
   - Value: Total Revenue
   - Format: Currency (Crores)

4. **Gauge Chart - Avg Health Score**
   - Value: Avg Health Score
   - Min: 0, Max: 100
   - Target: 75

5. **Column Chart - Revenue by Sector**
   - Axis: dim_company[sector]
   - Value: Total Revenue
   - Sort: Descending

6. **Line Chart - Revenue Trend**
   - Axis: dim_year[year_value]
   - Value: Total Revenue
   - Legend: Add dim_company[sector]

7. **Donut Chart - Health Label Distribution**
   - Values: COUNTA(fact_ml_scores[health_label])
   - Legend: fact_ml_scores[health_label]

8. **Slicer - Company**
   - Field: dim_company[company_name]
   - Type: List
   - Selection type: Single select

9. **Slicer - Year**
   - Field: dim_year[year_value]
   - Type: List
   - Selection type: Single select

---

### PAGE 2: Company Deep Dive

**Single Company Analysis**

1. **Slicer - Company**
   - Field: dim_company[symbol]
   - Type: Dropdown

2. **Card - Health Score**
   - Value: AVERAGE(fact_ml_scores[overall_score])
   - Format: Number with gauge
   - Conditional formatting based on score

3. **Card - Company Name**
   - Value: MAX(dim_company[company_name])
   - Formatting: Large text

4. **Table - 5Y Financial Summary**
   - Columns: Year, Sales, Net Profit, OPM%, ROE%
   - Rows: Year

5. **Line Chart - Profitability Trend**
   - Axis: Year
   - Line 1: Avg OPM
   - Line 2: Avg ROE
   - Dual axis enabled

6. **Bar Chart - Growth Metrics**
   - Category: Metric (Sales Growth, Profit Growth)
   - Value: Sales Growth % / Net Profit %

7. **Text Box - Pros**
   - Value: MAX(fact_pros_cons[pros_text])

8. **Text Box - Cons**
   - Value: MAX(fact_pros_cons[cons_text])

---

### PAGE 3: Sector Analysis

**Comparative Analysis by Sector**

1. **Slicer - Sector**
   - Field: dim_company[sector]
   - Type: List, Multi-select

2. **Table - Sector Metrics**
   - Group: sector
   - Columns: Company Count, Avg ROE, Avg OPM, Total Revenue

3. **Column Chart - Sector Comparison**
   - Axis: sector
   - Values: Avg ROE, Avg OPM (multi-column)

4. **Scatter Chart - ROE vs OPM**
   - X Axis: Avg OPM
   - Y Axis: Avg ROE
   - Legend: sector
   - Size: Total Revenue

5. **TreeMap - Revenue Distribution**
   - Values: Total Revenue
   - Category: company_name
   - Color saturation: Health Score

---

### PAGE 4: ML Intelligence & Scoring

**Health Scores & Investment Signals**

1. **Table - Company Health Scores**
   - Columns: Company, Health Score, Health Label, Score Status
   - Sort: Health Score DESC

2. **Gauge Charts (Multiple)**
   - One gauge per selected company
   - Values: Health Score

3. **Pie Chart - Health Distribution**
   - Category: Health Label
   - Value: Count of companies

4. **Matrix - Pros/Cons Summary**
   - Rows: Company
   - Values: Pros and Cons text

5. **Card - Companies in Good Health**
   - Value: Count where Health Score >= 70

6. **Card - Companies in Weak Health**
   - Value: Count where Health Score < 50

---

## Step 6: Formatting & Polish

### Colors & Styling
- **Excellent (85+):** Green (#10B981)
- **Good (70-84):** Light Green (#34D399)
- **Average (50-69):** Yellow (#FBBF24)
- **Weak (<50):** Red (#EF4444)

### Theme
- Light background (#F3F4F6)
- Dark text (#1F2937)
- Accent color: Blue (#3B82F6)

### Data Refresh
1. **Queries** → **Refresh** tab
2. Set refresh schedule: **Weekly** (Saturday 10 PM)
3. Or manual refresh via Power BI Service

## Step 7: Publish & Share

1. Click **Publish** in Power BI Desktop
2. Select workspace (create new if needed)
3. Dashboards now available in Power BI Service
4. Share with team via: Service → Share

## Troubleshooting

### "SQLite connector not found"
→ Use ODBC method (Option B above)

### "Connection timeout"
→ Check file path is correct
→ Verify file isn't open in other app

### "Relationships not showing"
→ Go to Model view
→ Manually drag and drop to create relationships
→ Ensure symbols match exactly

### "Slow dashboard performance"
→ Reduce date range in visuals
→ Create aggregation tables for large datasets
→ Use Import mode instead of DirectQuery

## File Location
```
C:\Users\vauld\Desktop\CODING\Internship BlueStock\bluestock_dw.db
```

---

**Total setup time: 30-45 minutes**

Once complete, you'll have a fully functional Power BI dashboard system ready for demo and submission!
