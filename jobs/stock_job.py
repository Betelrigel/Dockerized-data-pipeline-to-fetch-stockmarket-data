# jobs/stock_job.py

from dagster import job, op
import sys

# This line tells Python to look for modules in the /opt/dagster/app directory,
# which is where our 'scripts' folder is located inside the container.
sys.path.append('/opt/dagster/app')

from scripts.fetch_stock_data import fetch_and_store_stock_data

@op
def fetch_ibm_stock_op():
    """
    A Dagster op that fetches stock data for the symbol 'IBM'.
    """
    fetch_and_store_stock_data('IBM')

@job
def stock_data_job():
    """
    The main Dagster job that orchestrates the data fetching process.
    """
    fetch_ibm_stock_op()