@echo off
echo "%CM_PYTHON_BIN_WITH_PATH%" "%CM_TMP_CURRENT_SCRIPT_PATH%\process.py"
"%CM_PYTHON_BIN_WITH_PATH%" "%CM_TMP_CURRENT_SCRIPT_PATH%\process.py"
if %errorlevel% neq 0 exit /b 1