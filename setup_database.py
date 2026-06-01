#!/usr/bin/env python3
"""
Setup SQLite Database for Nifty 100 Financial Intelligence System
Creates complete schema and loads sample data

Run: python setup_database.py
"""

import sqlite3
import pandas as pd
from datetime import datetime
import os

# Database path
DB_PATH = "bluestock_dw.db"

def create_connection():
    """Create SQLite database connection"""
    conn = sqlite3.connect(DB_PATH)
    return conn

def create_dimension_tables(conn):
    """Create dimension tables"""
    cursor = conn.cursor()
    
    # dim_company
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS dim_company (
            symbol TEXT PRIMARY KEY,
            company_name TEXT NOT NULL,
            sector TEXT NOT NULL,
            market_cap_billions REAL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # dim_year
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS dim_year (
            year_id INTEGER PRIMARY KEY,
            year_value INTEGER NOT NULL
        )
    """)
    
    # dim_sector
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS dim_sector (
            sector_id INTEGER PRIMARY KEY AUTOINCREMENT,
            sector_name TEXT NOT NULL,
            description TEXT
        )
    """)
    
    # dim_health_label
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS dim_health_label (
            label_id INTEGER PRIMARY KEY AUTOINCREMENT,
            label_name TEXT NOT NULL,
            score_min INTEGER,
            score_max INTEGER
        )
    """)
    
    conn.commit()
    print("✓ Dimension tables created")

def create_fact_tables(conn):
    """Create fact tables"""
    cursor = conn.cursor()
    
    # fact_profit_loss
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS fact_profit_loss (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT NOT NULL,
            year_id INTEGER NOT NULL,
            sales REAL,
            net_profit REAL,
            opm_pct REAL,
            roe_pct_3y REAL,
            sales_growth_3y REAL,
            FOREIGN KEY (symbol) REFERENCES dim_company(symbol),
            FOREIGN KEY (year_id) REFERENCES dim_year(year_id)
        )
    """)
    
    # fact_balance_sheet
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS fact_balance_sheet (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT NOT NULL,
            year_id INTEGER NOT NULL,
            total_assets REAL,
            total_debt REAL,
            equity REAL,
            FOREIGN KEY (symbol) REFERENCES dim_company(symbol),
            FOREIGN KEY (year_id) REFERENCES dim_year(year_id)
        )
    """)
    
    # fact_cash_flow
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS fact_cash_flow (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT NOT NULL,
            year_id INTEGER NOT NULL,
            operating_cf REAL,
            investing_cf REAL,
            financing_cf REAL,
            free_cf REAL,
            FOREIGN KEY (symbol) REFERENCES dim_company(symbol),
            FOREIGN KEY (year_id) REFERENCES dim_year(year_id)
        )
    """)
    
    # fact_ml_scores
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS fact_ml_scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT NOT NULL,
            overall_score REAL,
            health_label TEXT,
            FOREIGN KEY (symbol) REFERENCES dim_company(symbol)
        )
    """)
    
    # fact_pros_cons
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS fact_pros_cons (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT NOT NULL,
            pros_text TEXT,
            cons_text TEXT,
            FOREIGN KEY (symbol) REFERENCES dim_company(symbol)
        )
    """)
    
    conn.commit()
    print("✓ Fact tables created")

def load_dimensions(conn):
    """Load dimension data"""
    cursor = conn.cursor()
    
    # Load years
    years = [(year, year) for year in range(2019, 2024)]
    cursor.executemany("INSERT OR IGNORE INTO dim_year (year_id, year_value) VALUES (?, ?)", years)
    
    # Load companies
    companies = [
        ('TCS', 'Tata Consultancy Services', 'IT', 1500),
        ('INFY', 'Infosys Limited', 'IT', 1400),
        ('HDFC', 'HDFC Bank Limited', 'Finance', 1200),
        ('RELIANCE', 'Reliance Industries Limited', 'Energy', 2000),
        ('ITC', 'ITC Limited', 'Diversified', 500),
        ('HCLTECH', 'HCL Technologies Limited', 'IT', 450),
        ('WIPRO', 'Wipro Limited', 'IT', 850),
        ('BAJAJFINSV', 'Bajaj Finserv Limited', 'Finance', 280),
        ('MARUTI', 'Maruti Suzuki India Limited', 'Automotive', 350),
        ('SUNPHARMA', 'Sun Pharmaceutical Industries', 'Pharma', 400),
        ('AXISBANK', 'Axis Bank Limited', 'Finance', 900),
        ('ICICIBANK', 'ICICI Bank Limited', 'Finance', 850),
        ('KOTAKBANK', 'Kotak Mahindra Bank Limited', 'Finance', 650),
        ('BAJAJFINSV2', 'Bajaj Finance Limited', 'Finance', 500),
        ('SBIN', 'State Bank of India', 'Finance', 750),
        ('ADANIPOWER', 'Adani Power Limited', 'Energy', 300),
        ('BHARTIARTL', 'Bharti Airtel Limited', 'Telecom', 380),
        ('TITAN', 'Titan Company Limited', 'Consumer', 450),
        ('NESTLEIND', 'Nestle India Limited', 'Consumer', 850),
        ('HINDUSTAN', 'Hindustan Unilever Limited', 'Consumer', 520),
    ]
    cursor.executemany("""
        INSERT OR IGNORE INTO dim_company (symbol, company_name, sector, market_cap_billions) 
        VALUES (?, ?, ?, ?)
    """, companies)
    
    # Load sectors
    sectors = [
        ('IT', 'Information Technology'),
        ('Finance', 'Banking & Financial Services'),
        ('Energy', 'Oil & Gas and Power'),
        ('Diversified', 'Diversified Conglomerates'),
        ('Automotive', 'Automotive & Components'),
        ('Pharma', 'Pharmaceuticals'),
        ('Telecom', 'Telecommunications'),
        ('Consumer', 'Consumer Goods & Services'),
    ]
    cursor.executemany("""
        INSERT OR IGNORE INTO dim_sector (sector_name, description) 
        VALUES (?, ?)
    """, sectors)
    
    # Load health labels
    health_labels = [
        ('Excellent', 85, 100),
        ('Good', 70, 84),
        ('Average', 50, 69),
        ('Weak', 0, 49),
    ]
    cursor.executemany("""
        INSERT OR IGNORE INTO dim_health_label (label_name, score_min, score_max) 
        VALUES (?, ?, ?)
    """, health_labels)
    
    conn.commit()
    print("✓ Dimension data loaded")

def load_facts(conn):
    """Load fact table data"""
    cursor = conn.cursor()
    
    # Sample profit/loss data
    pl_data = [
        ('TCS', 2023, 272600, 55800, 20.4, 28.5, 8.2),
        ('TCS', 2022, 248500, 51200, 20.6, 27.8, 7.9),
        ('TCS', 2021, 227100, 46500, 20.2, 26.9, 7.5),
        ('TCS', 2020, 221400, 42300, 19.1, 25.2, 6.8),
        ('TCS', 2019, 203700, 38500, 18.9, 24.8, 6.2),
        ('INFY', 2023, 197620, 42110, 18.7, 25.3, 7.1),
        ('INFY', 2022, 191900, 40156, 18.9, 24.8, 6.9),
        ('INFY', 2021, 163620, 35398, 19.1, 23.4, 6.5),
        ('INFY', 2020, 151128, 31675, 20.9, 22.1, 6.1),
        ('INFY', 2019, 138670, 28270, 20.4, 21.8, 5.8),
        ('HDFC', 2023, 235600, 65400, 27.8, 18.2, 5.3),
        ('HDFC', 2022, 218900, 60200, 28.1, 17.8, 5.0),
        ('HDFC', 2021, 205400, 55100, 27.5, 17.3, 4.8),
        ('HDFC', 2020, 189300, 49200, 26.0, 16.9, 4.5),
        ('HDFC', 2019, 175800, 44600, 25.4, 16.5, 4.2),
        ('RELIANCE', 2023, 885300, 155600, 17.6, 16.5, 6.2),
        ('RELIANCE', 2022, 856900, 148900, 18.2, 16.2, 6.0),
        ('RELIANCE', 2021, 748900, 132100, 17.9, 15.8, 5.7),
        ('RELIANCE', 2020, 688400, 115200, 16.7, 15.1, 5.3),
        ('RELIANCE', 2019, 625200, 98900, 15.8, 14.8, 5.0),
        ('ITC', 2023, 125800, 28900, 23.0, 22.4, 5.2),
        ('ITC', 2022, 118600, 26150, 22.7, 21.9, 4.9),
        ('ITC', 2021, 108900, 23750, 22.1, 21.2, 4.6),
        ('ITC', 2020, 102300, 21200, 20.7, 20.5, 4.2),
        ('ITC', 2019, 98700, 19800, 20.0, 19.8, 4.0),
    ]
    
    cursor.executemany("""
        INSERT INTO fact_profit_loss (symbol, year_id, sales, net_profit, opm_pct, roe_pct_3y, sales_growth_3y) 
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, pl_data)
    
    # Sample balance sheet data
    bs_data = [
        ('TCS', 2023, 485000, 25600, 210000),
        ('TCS', 2022, 445000, 28900, 195000),
        ('TCS', 2021, 405000, 31200, 180000),
        ('TCS', 2020, 365000, 33500, 165000),
        ('TCS', 2019, 325000, 36000, 150000),
        ('INFY', 2023, 425000, 19800, 185000),
        ('INFY', 2022, 395000, 21300, 172000),
        ('INFY', 2021, 365000, 22900, 160000),
        ('INFY', 2020, 335000, 24200, 148000),
        ('INFY', 2019, 305000, 25800, 135000),
        ('HDFC', 2023, 1285000, 145000, 580000),
        ('HDFC', 2022, 1185000, 140000, 550000),
        ('HDFC', 2021, 1085000, 135000, 520000),
        ('HDFC', 2020, 985000, 130000, 490000),
        ('HDFC', 2019, 885000, 125000, 460000),
    ]
    
    cursor.executemany("""
        INSERT INTO fact_balance_sheet (symbol, year_id, total_assets, total_debt, equity) 
        VALUES (?, ?, ?, ?, ?)
    """, bs_data)
    
    # Sample cash flow data
    cf_data = [
        ('TCS', 2023, 45600, -12000, -8900, 35200),
        ('TCS', 2022, 42100, -11000, -8200, 31800),
        ('TCS', 2021, 38900, -10000, -7500, 28900),
        ('INFY', 2023, 35200, -9800, -7200, 25600),
        ('INFY', 2022, 33500, -9200, -6800, 24100),
        ('INFY', 2021, 30200, -8600, -6300, 21900),
        ('HDFC', 2023, 52300, -15000, -12000, 38500),
        ('HDFC', 2022, 48900, -14000, -11000, 35900),
        ('HDFC', 2021, 44600, -13000, -10000, 33200),
    ]
    
    cursor.executemany("""
        INSERT INTO fact_cash_flow (symbol, year_id, operating_cf, investing_cf, financing_cf, free_cf) 
        VALUES (?, ?, ?, ?, ?, ?)
    """, cf_data)
    
    # Sample ML scores
    ml_data = [
        ('TCS', 78, 'Good'),
        ('INFY', 76, 'Good'),
        ('HDFC', 82, 'Good'),
        ('RELIANCE', 72, 'Good'),
        ('ITC', 68, 'Average'),
        ('HCLTECH', 71, 'Good'),
        ('WIPRO', 69, 'Average'),
        ('BAJAJFINSV', 65, 'Average'),
        ('MARUTI', 62, 'Average'),
        ('SUNPHARMA', 58, 'Average'),
        ('AXISBANK', 74, 'Good'),
        ('ICICIBANK', 70, 'Good'),
        ('KOTAKBANK', 75, 'Good'),
        ('SBIN', 68, 'Average'),
        ('ADANIPOWER', 55, 'Average'),
        ('BHARTIARTL', 60, 'Average'),
        ('TITAN', 73, 'Good'),
        ('NESTLEIND', 79, 'Good'),
        ('HINDUSTAN', 77, 'Good'),
    ]
    
    cursor.executemany("""
        INSERT INTO fact_ml_scores (symbol, overall_score, health_label) 
        VALUES (?, ?, ?)
    """, ml_data)
    
    # Sample pros/cons
    pros_cons_data = [
        ('TCS', 'Strong brand, Consistent ROE, Global presence, Strong cash flow', 'Competition in IT services, Employee attrition, Rupee appreciation risk'),
        ('INFY', 'Proven track record, Strong balance sheet, Dividend growth, Digital expertise', 'Large company slowdown risk, Visa policy changes, Talent retention'),
        ('HDFC', 'Market leader in banking, High ROE, Strong deposit growth', 'Interest rate risk, NPA concerns, Regulatory changes'),
        ('RELIANCE', 'Diversified business, Scale advantage, Refining margins', 'Energy price volatility, High debt, Regulatory risk'),
        ('ITC', 'Stable dividend, Diversified revenue, Real estate value', 'Tobacco regulatory risk, Declining margins, Consumer shift'),
    ]
    
    cursor.executemany("""
        INSERT INTO fact_pros_cons (symbol, pros_text, cons_text) 
        VALUES (?, ?, ?)
    """, pros_cons_data)
    
    conn.commit()
    print("✓ Fact data loaded")

def create_indexes(conn):
    """Create indexes for performance"""
    cursor = conn.cursor()
    
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_pl_symbol ON fact_profit_loss(symbol)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_pl_year ON fact_profit_loss(year_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_bs_symbol ON fact_balance_sheet(symbol)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_cf_symbol ON fact_cash_flow(symbol)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_ml_symbol ON fact_ml_scores(symbol)")
    
    conn.commit()
    print("✓ Indexes created")

def main():
    """Main setup function"""
    print("\n" + "="*50)
    print("Nifty 100 Financial Intelligence Database Setup")
    print("="*50 + "\n")
    
    # Delete existing database if it exists
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        print(f"✓ Removed existing database")
    
    # Create connection
    conn = create_connection()
    
    try:
        # Create tables
        create_dimension_tables(conn)
        create_fact_tables(conn)
        
        # Load data
        load_dimensions(conn)
        load_facts(conn)
        
        # Create indexes
        create_indexes(conn)
        
        print(f"\n✓ Database created successfully: {DB_PATH}")
        print(f"✓ Size: {os.path.getsize(DB_PATH) / (1024*1024):.2f} MB")
        print("\nDatabase is ready for Power BI connection!")
        print(f"Location: {os.path.abspath(DB_PATH)}")
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        raise
    finally:
        conn.close()

if __name__ == "__main__":
    main()
