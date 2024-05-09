#!/bin/bash
${CM_PYTHON_BIN_WITH_PATH} ${CM_TMP_CURRENT_SCRIPT_PATH}/process.py
test $? -eq 0 || exit 1
echo "CM_PREPROCESSED_DATASET_PATH=$PWD/questions.csv" > tmp-run-env.out
