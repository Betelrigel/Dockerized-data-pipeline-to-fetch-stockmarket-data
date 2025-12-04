# jobs/stock_job.py

from dagster import job, op, schedule
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


# Schedule definition: run the job daily. The dagster-daemon will pick this up
# when `dagster-daemon` is running and `DAGSTER_HOME` is configured.
@schedule(cron_schedule='0 0 * * *', job=stock_data_job)
def daily_stock_schedule(_context):
    """Daily schedule for `stock_data_job`.

    Returns an empty run config (uses defaults); customize if needed.
    """
    return {}