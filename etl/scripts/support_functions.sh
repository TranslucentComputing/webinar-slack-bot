#!/bin/bash

# Function to print and log messages
log() {
    echo "$(date +"%Y-%m-%d %H:%M:%S") - $1" | tee -a "$LOGFILE"
}

# Function to print and log error messages
error() {
    log "ERROR: $1"
    exit 1
}

# Function to check if a file exists
file_exists() {
    if [ ! -f "$1" ]; then
        error "File $1 does not exist."
    fi
}