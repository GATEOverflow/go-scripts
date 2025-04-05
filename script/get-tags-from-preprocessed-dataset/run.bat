@echo off
echo "%MLC_PYTHON_BIN_WITH_PATH%" "%MLC_TMP_CURRENT_SCRIPT_PATH%\process.py"
"%MLC_PYTHON_BIN_WITH_PATH%" "%MLC_TMP_CURRENT_SCRIPT_PATH%\process.py"
if %errorlevel% neq 0 exit /b 1
echo MLC_DATASET_TAGS=%CD%\tagList.json > tmp-run-env.out