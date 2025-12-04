# Dockerized Stock Market Data Pipeline with Dagster

This project is a complete, containerized data pipeline that automatically fetches daily stock market data from the Alpha Vantage API and stores it in a PostgreSQL database. The pipeline is orchestrated using Dagster and is deployed with a single command via Docker Compose, making it secure and reproducible.

**Architecture (simple flow)**

```
API (Alpha Vantage)  --->  Dagster (job/schedule)  --->  PostgreSQL (stock_data table)
	|                         |                            /
	|-- requests.get() ------>|-- job/op invokes script --|-- SQL upserts
```

The Dagster web UI (`dagit`) is used to inspect and trigger jobs; `dagster-daemon` picks up schedules.

## Technical Specifications and Features

The pipeline is built to meet all assignment requirements:

- **Containerized Deployment**: The entire application stack (PostgreSQL, Dagster UI, Dagster Daemon) is defined in a `docker-compose.yml` file for easy deployment.
- **Data Orchestration**: Dagster is used to schedule and manage the execution of the data fetching job. Jobs and schedules are discovered via `jobs/workspace.py`, which exports a repository containing `stock_data_job` and `daily_stock_schedule`.
- **API Interaction and Logic**: A Python script uses the `requests` library to fetch JSON data, parses the response, and inserts the extracted information into a PostgreSQL table.
- **Error Handling**: The core logic incorporates comprehensive `try-except` blocks, retries with backoff, and defensive parsing to ensure robustness against network, API rate limits, database failures, and missing data.
- **Logging**: Structured logging (via Python `logging` module) for auditing and troubleshooting.
- **Security**: Sensitive credentials (API keys and database details) are managed via environment variables defined in the `.env` file, which is never committed to version control.

## Prerequisites

Before you begin, ensure you have the following installed on your system:

- Docker
- Docker Compose (Included with Docker Desktop)

## Getting Started (How to Build and Deploy)

Follow these steps to build and run the entire pipeline stack.

### 1. Clone the Repository

First, clone this repository to your local machine.

```bash
git clone https://github.com/Betelrigel/Dockerized-data-pipeline-to-fetch-stockmarket-data.git
cd Dockerized-data-pipeline-to-fetch-stockmarket-data
```

### 2. Configure Environment Variables

This project uses an `.env` file to manage secret credentials.

Copy the template file:

```bash
cp .env.example .env
```

Edit the `.env` file and set the following:

- `POSTGRES_USER=postgres` (default Postgres superuser)
- `POSTGRES_PASSWORD=<your_secure_password>`
- `POSTGRES_DB=stock_market` (or your chosen database name)
- `ALPHA_VANTAGE_API_KEY=<your_alpha_vantage_api_key>` (obtain from https://www.alphavantage.co)

**Note**: The `.env` file is in `.gitignore` and should never be committed to version control.

### 3. Build and Start Services

Execute the following command from the root of the project directory. This command builds the custom Dagster image and starts all dependent services (PostgreSQL, Dagster Webserver, and Dagster Daemon).

```bash
docker-compose up --build
```

**Note**: The `--build` flag is only required the first time you run the deployment.

## Usage Guide (How to Run the Pipeline)

Once all containers are up and running, you can interact with the system via the Dagster UI.

### Accessing the Dagster UI

- **URL**: Open your web browser and navigate to `http://localhost:8081`

### Triggering the Data Fetching Job

1. In the Dagster UI, click on the **Jobs** tab.
2. Select the `stock_data_job`.
3. Navigate to the **Launchpad** tab.
4. Click the **"Launch Run"** button to execute the stock data fetching pipeline immediately.

### Automatic Scheduling

This project includes a Dagster schedule so the job can run automatically every day.

- **Schedule definition**: `jobs/stock_job.py` contains `daily_stock_schedule` with `cron_schedule='0 0 * * *'` (daily at midnight UTC).
- **Repository**: The schedule and job are exported by `jobs/workspace.py`, which defines the `stock_market_repo` repository that Dagster discovers.
- **How it runs**: The `dagster-daemon` process picks up schedules from the repository and launches runs according to their cron schedules.

#### To verify schedules are discovered:

```powershell
# List all registered schedules
docker exec dagster_daemon dagster schedule list -f /opt/dagster/app/jobs/workspace.py

# Expected output: Schedule: daily_stock_schedule [STOPPED] Cron Schedule: 0 0 * * *
```

#### To enable/disable schedules in the UI:

1. Open Dagit at http://localhost:8081
2. Click the **Automation** tab (left sidebar)
3. Find `daily_stock_schedule` and toggle to enable it (status will change from STOPPED to RUNNING)
4. Once enabled, the schedule will trigger `stock_data_job` at the specified cron time

#### To view schedule activity:

```powershell
# Watch daemon logs for schedule ticks and run launches
docker-compose logs -f dagster-daemon

# In Dagit, open the Runs tab to see execution history and logs
```

### Verifying Stored Data

After a successful run, verify that the data has been inserted into the PostgreSQL database.

1. Open a new terminal window (keeping the `docker-compose up` session running).
2. Execute the following command to connect to the database container and query the data:

```bash
# Replace 'postgres' with your POSTGRES_USER if different
docker exec postgres_db psql -U postgres -d stock_market -c "SELECT symbol, date, close FROM stock_data ORDER BY date DESC LIMIT 10;"
```

3. Or connect interactively:

```bash
docker exec -it postgres_db psql -U postgres -d stock_market
```

Then run:

```sql
SELECT count(*) FROM stock_data;
SELECT symbol, date, open, high, low, close, volume FROM stock_data ORDER BY date DESC LIMIT 10;
```

### Stopping the Pipeline

To gracefully stop all running containers, return to the original terminal session and press `Ctrl + C`. Then, remove the container instances:

```bash
docker-compose down
```

To remove the containers and the persisted PostgreSQL volume (deleting all stored data), use:

```bash
docker-compose down -v
```
