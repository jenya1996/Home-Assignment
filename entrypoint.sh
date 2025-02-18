#!/bin/bash -i
if [ -z "${LOG_FILE_DIR}" ]; then
    echo "LOG_FILE_DIR is missing from env"
    exit 1
fi
python3 -m uvicorn webapp:app --host 0.0.0.0 --port 8080