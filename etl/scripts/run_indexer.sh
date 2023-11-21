#!/bin/bash

# Indexer ETL Job Script
#
# This script executes the ETL job for processing CSV files and importing data into Redis.
# It sets necessary environment variables,
# activates the required Python environment, and runs the ETL job.
#
# Author: Patryk Golabek
# Company: Translucent Computing Inc.
# Copyright: 2023 Translucent Computing Inc.

# Bash safeties: exit on error, no unset variables, pipelines can't hide errors
set -o errexit
set -o nounset
set -o pipefail

# Define log file
LOGFILE="${LOGS_DIR}/etl_job.log"

# Source the support functions
source ${SCRIPT_DIR}/support_functions.sh

# Set the path to the .env file
export ENV_FILE_PATH="${ETL_DIR}/.env"

# Set environment variables
export DATA_DIR="${DATA_DIR}"

# Navigate to your project directory
log "Navigating to project directory ${PROJECT_ROOT}"
cd "$PROJECT_ROOT" || error "Failed to navigate to project directory."

# Run the Indexer ETL job
log "Starting the Indexer ETL job."
python -m src.jobs.redis_job >> "$LOGFILE" 2>&1 || error "ETL job failed."

log "Indexer ETL job completed successfully!"
