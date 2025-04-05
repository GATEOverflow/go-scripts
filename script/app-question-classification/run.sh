#!/bin/bash

echo "$MLC_PYTHON_BIN_WITH_PATH" "$MLC_TMP_CURRENT_SCRIPT_PATH/process.py"
"$MLC_PYTHON_BIN_WITH_PATH" "$MLC_TMP_CURRENT_SCRIPT_PATH/process.py"
if [ $? -ne 0 ]; then
    exit 1
fi
echo "MLC_ML_MODEL_ANSWER=$(pwd)/Predicted_answers.csv" > tmp-run-env.out