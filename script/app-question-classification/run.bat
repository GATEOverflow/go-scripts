@echo off
"%CM_PYTHON_BIN_WITH_PATH%" "%CM_TMP_CURRENT_SCRIPT_PATH%\process.py"
echo CM_ML_MODEL_ANSWER=%CD%\Predicted_answers.csv > tmp-run-env.out
if %errorlevel% neq 0 exit /b 1