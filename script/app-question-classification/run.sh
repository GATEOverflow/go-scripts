#!/bin/bash

echo "$CM_PYTHON_BIN_WITH_PATH" "$CM_TMP_CURRENT_SCRIPT_PATH/process.py"
"$CM_PYTHON_BIN_WITH_PATH" "$CM_TMP_CURRENT_SCRIPT_PATH/process.py"
if [ $? -ne 0 ]; then
    exit 1
fi
