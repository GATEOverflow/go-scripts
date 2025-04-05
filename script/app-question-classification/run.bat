@echo off
"%MLC_PYTHON_BIN_WITH_PATH%" "%MLC_TMP_CURRENT_SCRIPT_PATH%\process.py"
echo MLC_ML_MODEL_ANSWER=%CD%\Predicted_answers.csv > tmp-run-env.out
if %errorlevel% neq 0 exit /b 1