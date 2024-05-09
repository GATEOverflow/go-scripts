@echo off
"%CM_PYTHON_BIN_WITH_PATH%" "%CM_TMP_CURRENT_SCRIPT_PATH%\process.py"
if %errorlevel% neq 0 exit /b 1
echo CM_PREPROCESSED_DATASET_PATH=%CD%\questions.csv > tmp-run-env.out
