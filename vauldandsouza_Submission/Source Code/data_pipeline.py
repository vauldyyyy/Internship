#!/usr/bin/env python3
"""
Data Pipeline for Nifty 100 Financial Intelligence System
Transforms raw stock market data and loads into PostgreSQL data warehouse

Author: vauldandsouza
Date: June 2, 2026
"""

import pandas as pd
import psycopg2
from psycopg2 import sql
import logging
from datetime import datetime

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class DataPipeline:
    """Main pipeline class for data extraction, transformation, and loading"""
    
    def __init__(self, db_host, db_name, db_user, db_password):
        """Initialize database connection"""
        try:
            self.conn = psycopg2.connect(
                host=db_host,
                database=db_name,
                user=db_user,
                password=db_password
            )
            self.cursor = self.conn.cursor()
            logger.info("Database connection established")
        except Exception as e:
            logger.error(f"Database connection failed: {e}")
            raise
    
    def create_dimension_tables(self):
        """Create dimension tables in data warehouse"""
        
        # Create dim_company table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS dim_company (
                symbol VARCHAR(20) PRIMARY KEY,
                company_name VARCHAR(255),
                sector VARCHAR(100),
                market_cap NUMERIC,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create dim_year table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS dim_year (
                year_id INT PRIMARY KEY,
                year_value INT,
                quarter INT
            )
        """)
        
        # Create dim_sector table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS dim_sector (
                sector_id SERIAL PRIMARY KEY,
                sector_name VARCHAR(100),
                description TEXT
            )
        """)
        
        # Create dim_health_label table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS dim_health_label (
                label_id SERIAL PRIMARY KEY,
                label_name VARCHAR(50),
                score_min INT,
                score_max INT
            )
        """)
        
        self.conn.commit()
        logger.info("Dimension tables created successfully")
    
    def create_fact_tables(self):
        """Create fact tables in data warehouse"""
        
        # Create fact_profit_loss table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS fact_profit_loss (
                id SERIAL PRIMARY KEY,
                symbol VARCHAR(20),
                year_id INT,
                sales NUMERIC,
                net_profit NUMERIC,
                opm_pct NUMERIC,
                roe_pct_3y NUMERIC,
                sales_growth_3y NUMERIC,
                FOREIGN KEY (symbol) REFERENCES dim_company(symbol),
                FOREIGN KEY (year_id) REFERENCES dim_year(year_id)
            )
        """)
        
        # Create fact_balance_sheet table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS fact_balance_sheet (
                id SERIAL PRIMARY KEY,
                symbol VARCHAR(20),
                year_id INT,
                total_assets NUMERIC,
                total_debt NUMERIC,
                equity NUMERIC,
                FOREIGN KEY (symbol) REFERENCES dim_company(symbol),
                FOREIGN KEY (year_id) REFERENCES dim_year(year_id)
            )
        """)
        
        # Create fact_cash_flow table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS fact_cash_flow (
                id SERIAL PRIMARY KEY,
                symbol VARCHAR(20),
                year_id INT,
                operating_cf NUMERIC,
                investing_cf NUMERIC,
                financing_cf NUMERIC,
                free_cf NUMERIC,
                FOREIGN KEY (symbol) REFERENCES dim_company(symbol),
                FOREIGN KEY (year_id) REFERENCES dim_year(year_id)
            )
        """)
        
        # Create fact_ml_scores table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS fact_ml_scores (
                id SERIAL PRIMARY KEY,
                symbol VARCHAR(20),
                overall_score NUMERIC,
                health_label VARCHAR(50),
                FOREIGN KEY (symbol) REFERENCES dim_company(symbol)
            )
        """)
        
        # Create fact_pros_cons table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS fact_pros_cons (
                id SERIAL PRIMARY KEY,
                symbol VARCHAR(20),
                pros_text TEXT,
                cons_text TEXT,
                FOREIGN KEY (symbol) REFERENCES dim_company(symbol)
            )
        """)
        
        # Create fact_analysis table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS fact_analysis (
                id SERIAL PRIMARY KEY,
                symbol VARCHAR(20),
                year_id INT,
                rating VARCHAR(10),
                recommendation TEXT,
                FOREIGN KEY (symbol) REFERENCES dim_company(symbol),
                FOREIGN KEY (year_id) REFERENCES dim_year(year_id)
            )
        """)
        
        self.conn.commit()
        logger.info("Fact tables created successfully")
    
    def load_sample_data(self):
        """Load sample data for demonstration"""
        
        # Sample companies
        companies = [
            ('TCS', 'Tata Consultancy Services', 'IT', 1500000),
            ('INFY', 'Infosys Limited', 'IT', 1400000),
            ('HDFC', 'HDFC Bank Limited', 'Finance', 1200000),
            ('RELIANCE', 'Reliance Industries', 'Energy', 2000000),
            ('ITC', 'ITC Limited', 'Diversified', 500000),
        ]
        
        for company in companies:
            try:
                self.cursor.execute("""
                    INSERT INTO dim_company (symbol, company_name, sector, market_cap)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (symbol) DO NOTHING
                """, company)
            except Exception as e:
                logger.warning(f"Error loading company {company[0]}: {e}")
        
        self.conn.commit()
        logger.info("Sample data loaded successfully")
    
    def calculate_metrics(self):
        """Calculate financial metrics from raw data"""
        logger.info("Calculating financial metrics...")
        # Implementation for metric calculation
        pass
    
    def validate_data(self):
        """Validate data quality and completeness"""
        
        # Check for null values
        self.cursor.execute("""
            SELECT COUNT(*) FROM fact_profit_loss WHERE sales IS NULL
        """)
        null_count = self.cursor.fetchone()[0]
        
        if null_count > 0:
            logger.warning(f"Found {null_count} null values in fact_profit_loss[sales]")
        
        logger.info("Data validation completed")
    
    def close(self):
        """Close database connection"""
        self.cursor.close()
        self.conn.close()
        logger.info("Database connection closed")


def main():
    """Main execution function"""
    
    # Database configuration
    DB_HOST = "localhost"
    DB_NAME = "bluestock_dw"
    DB_USER = "postgres"
    DB_PASSWORD = "your_password"  # Change this!
    
    try:
        # Initialize pipeline
        pipeline = DataPipeline(DB_HOST, DB_NAME, DB_USER, DB_PASSWORD)
        
        # Execute pipeline steps
        logger.info("Starting data pipeline...")
        pipeline.create_dimension_tables()
        pipeline.create_fact_tables()
        pipeline.load_sample_data()
        pipeline.calculate_metrics()
        pipeline.validate_data()
        
        logger.info("Data pipeline completed successfully!")
        
    except Exception as e:
        logger.error(f"Pipeline execution failed: {e}")
        raise
    
    finally:
        pipeline.close()


if __name__ == "__main__":
    main()
