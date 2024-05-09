#!/bin/bash

echo "$CM_PYTHON_BIN_WITH_PATH" "$CM_TMP_CURRENT_SCRIPT_PATH/process.py"
"$CM_PYTHON_BIN_WITH_PATH" "$CM_TMP_CURRENT_SCRIPT_PATH/process.py"
if [ $? -ne 0 ]; then
    exit 1
fi
echo "CM_ML_MODEL_ANSWER=$(pwd)/Predicted_answers.csv" > tmp-run-env.out