# Makefile for ETL Jobs

# Determine the project root directory
PROJECT_ROOT = $(CURDIR)/..

$(info PROJECT_ROOT is $(PROJECT_ROOT))

# Variables
ETL_DIR = $(PROJECT_ROOT)/etl
DATA_DIR = $(ETL_DIR)/data
SCRIPT_DIR = $(ETL_DIR)/scripts
LOGS_DIR = $(SCRIPT_DIR)/logs

INDEXER_SCRIPT = $(SCRIPT_DIR)/run_indexer.sh

COMMON_VARS = LOGS_DIR=$(LOGS_DIR) ETL_DIR=$(ETL_DIR) DATA_DIR=$(DATA_DIR) PROJECT_ROOT=$(PROJECT_ROOT) SCRIPT_DIR=$(SCRIPT_DIR)

.PHONY: help indexer_job

# Help target to display available commands
help:
	@echo "Available commands:"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

# Target to execute the Indexer Job
indexer_job: ## Redis data indexer job that reads CSV files.
	$(COMMON_VARS) bash $(INDEXER_SCRIPT)
