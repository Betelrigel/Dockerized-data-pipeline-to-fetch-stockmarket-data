import os
import requests
import psycopg2
from psycopg2 import sql

def fetch_and_store_stock_data(symbol):
    """
    Fetches daily stock data for a given symbol from Alpha Vantage
    and stores it in a PostgreSQL database.
    """
    api_key = os.getenv('ALPHA_VANTAGE_API_KEY')
    db_name = os.getenv('POSTGRES_DB')
    db_user = os.getenv('POSTGRES_USER')
    db_password = os.getenv('POSTGRES_PASSWORD')
    db_host = os.getenv('POSTGRES_HOST', 'postgres') # Default to 'postgres' if not set

    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}'

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes
        data = response.json()

        if "Time Series (Daily)" not in data:
            print(f"Could not find time series data for {symbol}")
            return

        time_series = data["Time Series (Daily)"]

        conn = psycopg2.connect(
            dbname=db_name,
            user=db_user,
            password=db_password,
            host=db_host
        )
        cur = conn.cursor()

        # Create table if it doesn't exist
        cur.execute("""
            CREATE TABLE IF NOT EXISTS stock_data (
                symbol VARCHAR(10),
                date DATE,
                open NUMERIC,
                high NUMERIC,
                low NUMERIC,
                close NUMERIC,
                volume BIGINT,
                PRIMARY KEY (symbol, date)
            );
        """)
        conn.commit()

        for date_str, values in time_series.items():
            try:
                cur.execute(
                    sql.SQL("""
                        INSERT INTO stock_data (symbol, date, open, high, low, close, volume)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                        ON CONFLICT (symbol, date) DO NOTHING;
                    """),
                    (
                        symbol,
                        date_str,
                        float(values['1. open']),
                        float(values['2. high']),
                        float(values['3. low']),
                        float(values['4. close']),
                        int(values['5. volume'])
                    )
                )
            except psycopg2.Error as e:
                print(f"Database error on {date_str} for {symbol}: {e}")
                conn.rollback()

        conn.commit()
        cur.close()
        conn.close()
        print(f"Successfully fetched and stored data for {symbol}")

    except requests.exceptions.RequestException as e:
        print(f"HTTP Request failed: {e}")
    except psycopg2.Error as e:
        print(f"Database connection failed: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    # Example usage, you can pass any stock symbol
    fetch_and_store_stock_data('IBM')