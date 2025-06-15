#!/bin/bash

# Initialize script path
MLC_TMP_CURRENT_SCRIPT_PATH="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Initialize MLC_PYTHON_BIN_WITH_PATH
MLC_PYTHON_BIN_WITH_PATH=${MLC_PYTHON_BIN_WITH_PATH:-python3}

# Install required Python packages
pip install pdfplumber

# Run the Gemini script
echo "Python path: $MLC_PYTHON_BIN_WITH_PATH"
echo "Script path: $MLC_TMP_CURRENT_SCRIPT_PATH/customize.py"
${MLC_PYTHON_BIN_WITH_PATH} ${MLC_TMP_CURRENT_SCRIPT_PATH}/customize.py
test $? -eq 0 || exit 1