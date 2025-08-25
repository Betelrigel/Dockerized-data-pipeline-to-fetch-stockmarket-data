# Dockerized Stock Market Data Pipeline

This project is a Dockerized data pipeline that fetches daily stock market data from the Alpha Vantage API and stores it in a PostgreSQL database. The pipeline is orchestrated using [Airflow/Dagster].

## Prerequisites

- Docker
- Docker Compose

## Setup

1.  **Clone the repository:**
    ```bash
    git clone <your-repository-url>
    cd data_pipeline
    ```

2.  **Create a `.env` file:**
    Create a file named `.env` in the root of the project and add the following, replacing the placeholder values with your credentials:
    ```
    ALPHA_VANTAGE_API_KEY=YOUR_API_KEY
    POSTGRES_USER=your_username
    POSTGRES_PASSWORD=your_password
    POSTGRES_DB=stock_market
    ```

## Running the Pipeline

To build and run the entire pipeline, use the following command:

```bash
docker-compose up -d