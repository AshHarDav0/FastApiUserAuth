# Use an official Python runtime as a parent image
FROM python:3.10

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container to /FastApiUserAuth
WORKDIR /FastApiUserAuth

# Install system dependencies
RUN apt-get update && apt-get install -y gcc postgresql-client

# Install poetry
RUN pip install --no-cache-dir poetry

# Copy only requirements to cache them in docker layer
COPY pyproject.toml poetry.lock* /FastApiUserAuth/

# Project initialization:
RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi

# Copying in our source code
COPY . /FastApiUserAuth

# Copy wait-for-postgres.sh and make it executable
COPY wait-for-postgres.sh /wait-for-postgres.sh
RUN chmod +x /wait-for-postgres.sh

# Run the script to wait for the database to be ready, then run the application
CMD /wait-for-postgres.sh && python app/main.py