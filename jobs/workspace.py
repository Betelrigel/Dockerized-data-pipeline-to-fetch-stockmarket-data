# jobs/workspace.py
"""
Workspace definition for Dagster.
This file exports all jobs and schedules so Dagit and dagster-daemon can discover them.
"""

import sys
sys.path.insert(0, '/opt/dagster/app')

from dagster import repository
# Import jobs and schedules directly from stock_job
import importlib.util
spec = importlib.util.spec_from_file_location("stock_job", "/opt/dagster/app/jobs/stock_job.py")
stock_job_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(stock_job_module)

stock_data_job = stock_job_module.stock_data_job
daily_stock_schedule = stock_job_module.daily_stock_schedule


@repository
def stock_market_repo():
    """Main repository containing all jobs and schedules."""
    return [stock_data_job, daily_stock_schedule]
