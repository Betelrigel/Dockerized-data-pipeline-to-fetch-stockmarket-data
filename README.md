# Dockerized Stock Market Data Pipeline with Dagster

This project is a complete, containerized data pipeline that automatically fetches daily stock market data from the Alpha Vantage API and stores it in a PostgreSQL database. The pipeline is orchestrated using Dagster and is deployed with a single command via Docker Compose, making it secure and reproducible.

---

## Technical Specifications and Features

The pipeline is built to meet all assignment requirements:

*   **Containerized Deployment:** The entire application stack (PostgreSQL, Dagster UI, Dagster Daemon) is defined in a `docker-compose.yml` file for easy deployment.
*   **Data Orchestration:** Dagster is used to schedule and manage the execution of the data fetching job.
*   **API Interaction and Logic:** A Python script uses the `requests` library to fetch JSON data, parses the response, and inserts the extracted information into a PostgreSQL table.
*   **Error Handling:** The core logic incorporates comprehensive `try-except` blocks to ensure robustness against network, parsing, and database failures.
*   **Security:** Sensitive credentials (API keys and database details) are managed via environment variables defined in the `.env` file.

---

## Prerequisites

Before you begin, ensure you have the following installed on your system:

-   Docker
-   Docker Compose (Included with Docker Desktop)

---

## Getting Started (How to Build and Deploy)

Follow these steps to build and run the entire pipeline stack.

### 1. Clone the Repository

First, clone this repository to your local machine.

```bash
git clone https://github.com/your-username/your-repository-name.git
cd your-repository-name
