
# Start from a standard, clean Python image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /opt/dagster/app

# Install all the Python libraries we need in one go
# This ensures all their versions are compatible with each other
RUN pip install dagster dagit dagster-postgres psycopg2-binary requests

# Copy our application code into the image
COPY ./jobs /opt/dagster/app/jobs
COPY ./scripts /opt/dagster/app/scripts