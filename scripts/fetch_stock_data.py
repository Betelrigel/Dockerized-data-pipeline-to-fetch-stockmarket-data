import os
import time
import logging
import requests
import psycopg2
from psycopg2 import sql
from requests.exceptions import RequestException

def fetch_and_store_stock_data(symbol):
    """
    Fetches daily stock data for a given symbol from Alpha Vantage
    and stores it in a PostgreSQL database.
    """
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
    api_key = os.getenv('ALPHA_VANTAGE_API_KEY')
    db_name = os.getenv('POSTGRES_DB')
    db_user = os.getenv('POSTGRES_USER')
    db_password = os.getenv('POSTGRES_PASSWORD')
    db_host = os.getenv('POSTGRES_HOST', 'postgres') # Default to 'postgres' if not set

    if not api_key:
        logging.error('ALPHA_VANTAGE_API_KEY is not set. Aborting fetch for %s', symbol)
        return

    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}'

    # Fetch with simple retry/backoff for transient network issues
    max_http_retries = 3
    for attempt in range(1, max_http_retries + 1):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            break
        except RequestException as e:
            logging.warning('HTTP request attempt %s failed for %s: %s', attempt, symbol, e)
            if attempt == max_http_retries:
                logging.error('Max HTTP retries reached. Aborting fetch for %s', symbol)
                return
            time.sleep(2 ** attempt)

    if "Time Series (Daily)" not in data:
        # Alpha Vantage may return messages in 'Note' or 'Error Message'
        note = data.get('Note') or data.get('Error Message') or 'No time series data in response'
        logging.error('Could not find time series data for %s: %s', symbol, note)
        return

    time_series = data["Time Series (Daily)"]

    # Retry DB connection a few times because the DB container may not be ready yet
    max_db_retries = 5
    conn = None
    for attempt in range(1, max_db_retries + 1):
        try:
            conn = psycopg2.connect(
                dbname=db_name,
                user=db_user,
                password=db_password,
                host=db_host
            )
            break
        except psycopg2.OperationalError as e:
            logging.warning('DB connection attempt %s failed: %s', attempt, e)
            if attempt == max_db_retries:
                logging.error('Max DB connection retries reached. Aborting.')
                return
            time.sleep(2 ** attempt)

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
                    float(values.get('1. open', 0) or 0),
                    float(values.get('2. high', 0) or 0),
                    float(values.get('3. low', 0) or 0),
                    float(values.get('4. close', 0) or 0),
                    int(values.get('5. volume', 0) or 0)
                )
            )
        except psycopg2.Error as e:
            logging.exception('Database error on %s for %s: %s', date_str, symbol, e)
            conn.rollback()

    conn.commit()
    cur.close()
    conn.close()
    logging.info('Successfully fetched and stored data for %s', symbol)

if __name__ == "__main__":
    # Example usage, you can pass any stock symbol
    fetch_and_store_stock_data('IBM')