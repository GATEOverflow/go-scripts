@echo off
"%MLC_PYTHON_BIN_WITH_PATH%" "%MLC_TMP_CURRENT_SCRIPT_PATH%\process.py"
if %errorlevel% neq 0 exit /b 1
echo MLC_PREPROCESSED_DATASET_PATH=%CD%\questions.csv > tmp-run-env.out
