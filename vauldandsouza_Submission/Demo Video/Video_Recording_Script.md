# DEMO VIDEO RECORDING SCRIPT

**Duration:** 5 minutes  
**Format:** Screen recording with voice-over  
**Tools:** OBS Studio or similar (free)

---

## SECTION 1: INTRODUCTION (0:00 - 0:30)

**Script:**
"Hello, I'm vauldandsouza, and this is a walkthrough of the Nifty 100 Financial Intelligence System I built over 8 weeks.

This is a comprehensive financial analysis platform with 7 interactive Power BI dashboards, a PostgreSQL data warehouse, and machine learning-based health scoring.

In this 5-minute demo, I'll show you:
- How the system works
- Key dashboards in action
- Interactive features
- Insights you can extract"

**Actions:**
- Show desktop with Power BI icon visible
- Smoothly transition to first dashboard

---

## SECTION 2: EXECUTIVE OVERVIEW DASHBOARD (0:30 - 1:45)

**Script:**
"Let me start with the Executive Overview dashboard. This is designed for fund managers and CXOs who need a quick snapshot of the market.

[Click on dashboard file or show it opening]

You can see three main pages here: Market Snapshot, Sector Performance, and YoY Growth Tracker.

On the Market Snapshot:
- We have 100 companies in our database
- Average ROE across all is about 20%
- This donut chart shows sector distribution - IT has the most companies
- The health label distribution shows most companies are in the 'Good' category

[Hover over different sections as you explain]

Let me interact with the company slicer. If I select just IT companies, watch how all visuals update automatically.

[Click on IT companies in a filter/slicer]

Now we see only IT metrics - average ROE, specific companies. This filter-driven approach is powerful.

Let me check the Sector Performance page.

[Navigate to next page]

This page shows:
- Revenue trends by sector over 5 years
- Sector profitability comparison
- A treemap showing revenue by sector (area size = total revenue, color = health score)

You can see IT and Finance sectors dominate in revenue. The green colors indicate healthy companies."

---

## SECTION 3: COMPANY DEEP DIVE DASHBOARD (1:45 - 3:00)

**Script:**
"Now let's dive deeper with the Company Deep Dive dashboard - this is for analysts doing detailed research.

[Open Company Deep Dive dashboard]

The key feature here is the company selector at the top. Once you select a company, all visuals update to show that company's data.

Let me select TCS - a major IT company.

[Click on TCS in the company slicer]

Instantly, you see:
- Health Score Gauge: TCS scores 78/100 - 'Good' category
- A 5-year profitability chart showing margins and ROE
- Financial summary with key metrics
- Detailed financial metrics table

TCS shows:
- Consistent 20%+ OPM (Operating Profit Margin)
- 25%+ ROE - excellent profitability
- Stable growth over 5 years
- Strong health score indicates a quality company

Let me compare with another company. Let me select Reliance Industries.

[Click on Reliance]

Reliance shows:
- Health Score: 72/100 - Good
- Much larger scale (higher revenue)
- Different profitability profile - lower OPM (17%) due to diversified business
- Capital-intensive nature (oil & gas) affects ROE
- But strong absolute profit numbers

This deep comparison is exactly what analysts need to evaluate companies."

---

## SECTION 4: ML INTELLIGENCE DASHBOARD (3:00 - 4:15)

**Script:**
"One of the innovative features is our ML Intelligence dashboard - showing AI-based health scores.

[Open ML Intelligence dashboard]

This dashboard visualizes:
- Health scores for all 100 companies on a gauge chart
- Distribution by health category (Excellent, Good, Average, Weak)
- Pros and cons for selected companies
- Risk scoring

The health score model weights 5 factors:
- Profitability (30%) - Is the company making money?
- Growth (25%) - Is it expanding?
- Leverage (20%) - Is it overleveraged?
- Liquidity (15%) - Can it pay bills?
- Quality (10%) - Earnings quality?

Scores above 85 are Excellent (green), 70-84 is Good (light green), 50-69 is Average (yellow), below 50 is Weak (red).

Let me filter for IT companies with Excellent health scores.

[Apply filters]

We see a few IT companies with excellent scores - these are your quality blue chips. Great for conservative investors.

Now let me show investment signals. Looking at the pros/cons matrix, you get:
- Key strengths of each company
- Risk factors to monitor
- Quick summary for investment committees"

---

## SECTION 5: TECHNICAL ARCHITECTURE (4:15 - 4:45)

**Script:**
"Behind these beautiful dashboards is a robust technical architecture.

[Show a diagram or explain visually]

Here's how it works:

1. **Data Sources:** Raw financial data from NSE, annual reports, industry databases
2. **ETL Pipeline:** Python script that cleans, transforms, and validates data
3. **Data Warehouse:** PostgreSQL database with star schema design (4 dimensions, 6 fact tables)
4. **BI Layer:** Power BI connects directly to PostgreSQL and renders interactive dashboards

The star schema design enables:
- Fast queries (milliseconds)
- Flexible analysis (any combination of dimensions)
- Scalability (can add more companies easily)
- Consistency (all dashboards use same data)

Data refreshes weekly, so dashboards are always current."

---

## SECTION 6: KEY METRICS & INSIGHTS (4:45 - 5:00)

**Script:**
"Let me highlight some key insights from this analysis:

[Show relevant dashboard visuals]

1. **Top Quality Companies:** TCS, INFY, HDFC show high ROE + high profitability consistency

2. **Growth Leaders:** Reliance shows strong absolute growth, newer tech startups show high growth rates

3. **Sector Insights:** IT has best margins, Finance shows stability, Energy is capital-intensive

4. **Health Trend:** Most companies are in 'Good' or 'Average' categories - market is balanced

5. **Opportunity:** Companies moving from Average to Good health scores are worth watching

This system enables data-driven investment decisions without spending hours in Excel.

Thank you for watching! If you'd like to explore further, the dashboards are interactive - you can slice by sector, year, company, or any combination."

---

## RECORDING SETUP CHECKLIST

**Before Recording:**

□ Close all unnecessary applications (clean screen)
□ Set Power BI theme to light (better for recording)
□ Maximize Power BI window to full screen
□ Enable high-quality recording (1080p minimum)
□ Test microphone (clear, no background noise)
□ Record in quiet environment
□ Have dashboards pre-loaded (no wait times)
□ Set dashboard filters to default state

**Recording Tools:**
- **OBS Studio** (free, powerful) - https://obsproject.com/
- **Camtasia** (paid, easier) - https://www.techsmith.com/camtasia.html
- **ScreenFlow** (Mac only, free) - https://www.screenflow.io/

**Quality Settings:**
- Resolution: 1920x1080 (1080p)
- Framerate: 30 FPS
- Bitrate: 8-10 Mbps
- Audio: 192 kbps, 44.1 kHz

**Post-Production:**
1. Edit video (remove long pauses, mistakes)
2. Add title card (company name, your name)
3. Add background music (low volume, royalty-free)
4. Export as MP4 or MOV
5. Keep final video under 100 MB

**Royalty-Free Music:**
- YouTube Audio Library (free)
- Freepik.com (free)
- Epidemic Sound (paid)

---

## NARRATION TIPS

✓ Speak clearly and at moderate pace  
✓ Pause between sections  
✓ Use the phrase "Let me show you..." to transition between features  
✓ Point out metrics as you show them  
✓ Avoid saying "um", "uh", "like"  
✓ Make eye contact with camera (imagine talking to viewer)  
✓ Show enthusiasm (your energy comes through in voice)  
✓ Test audio levels before final recording  

---

**Total video length: 5 minutes 15 seconds (acceptable)**

If you need to cut down, prioritize:
1. Keep Introduction & Company Deep Dive
2. Keep ML Intelligence (innovative feature)
3. Shorten architecture explanation if needed
