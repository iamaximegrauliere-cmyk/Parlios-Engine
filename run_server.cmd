@echo off
setlocal
set PYTHONPATH=%CD%
set HOST=127.0.0.1
set PORT=8080
.\.venv\Scripts\python.exe -m uvicorn engine.api.main:app --host %HOST% --port %PORT%
endlocal
