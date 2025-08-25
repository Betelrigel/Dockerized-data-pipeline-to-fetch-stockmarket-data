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
2. Configure Environment Variables
This project uses an .env file to manage secret credentials. A secure template (.env.example) is provided.
Copy the template file:
code
Bash
cp .env.example .env
Edit the .env file: Open the newly created .env file and input your actual PostgreSQL credentials and your Alpha Vantage API key where indicated by the placeholders.
3. Build and Start Services
Execute the following command from the root of the project directory. This command builds the custom Dagster image and starts all dependent services (PostgreSQL, Dagster Webserver, and Dagster Daemon).
code
Bash
docker-compose up --build
(Note: The --build flag is only required the first time you run the deployment.)
Usage Guide (How to Run the Pipeline)
Once all containers are up and running, you can interact with the system via the Dagster UI.
Accessing the Dagster UI
URL: Open your web browser and navigate to http://localhost:8081
Triggering the Data Fetching Job
In the Dagster UI, click on the Jobs tab.
Select the stock_data_job.
Navigate to the Launchpad tab.
Click the "Launch Run" button to execute the stock data fetching pipeline immediately.
Verifying Stored Data
After a successful run, verify that the data has been inserted into the PostgreSQL database.
Open a new terminal window (keeping the docker-compose up session running).
Execute the following command to connect to the database container:
code
Bash
docker exec -it postgres_db psql -U your_username -d stock_market
(Replace your_username with the user defined in your .env file.)
Enter your database password when prompted.
Run a SQL query to inspect the data:
code
SQL
SELECT * FROM stock_data ORDER BY date DESC LIMIT 10;
Stopping the Pipeline
To gracefully stop all running containers, return to the original terminal session and press Ctrl + C. Then, remove the container instances:
code
Bash
docker-compose down
To remove the containers and the persisted PostgreSQL volume (deleting all stored data), use:
code
Bash
docker-compose down -v```
