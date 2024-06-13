#!/bin/bash

set -e

# Use the separate environment variables for the host, port, username, password, and database name
host=$TEST_DB_HOST
port=$TEST_DB_PORT
username=$TEST_DB_USER
password=$TEST_DB_PASSWORD
dbname=$TEST_DB_NAME

cmd="pytest tests"

>&2 echo "Waiting for Postgres to be available - $host:$port"
until PGPASSWORD=$password psql -h "$host" -p "$port" -U "$username" -d "$dbname" -c '\q'; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

>&2 echo "Postgres is up - executing command"
exec $cmd