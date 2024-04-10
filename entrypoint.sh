#!/bin/bash

ls -l

# Run the database migration first
echo "Running database migration..."
poetry run poe db-push

# Run the commands in parallel
echo "Starting the tailwind build and the main application in the background..."
parallel --ungroup ::: "poetry run poe dev-tailwind" "poetry run uvicorn app.app:app --host 0.0.0.0 --reload"