@echo off
SETLOCAL ENABLEDELAYEDEXPANSION

REM Script de lancement local du backend FastAPI (Windows)
REM Usage: run_local_backend.bat [--install] [--ollama-url URL]

set INSTALL=0
set "OLLAMA_URL=%OLLAMA_BASE_URL%"

:parse
if "%~1"=="" goto afterparse
if "%~1"=="--install" (
  set INSTALL=1
  shift
  goto parse
)
if "%~1"=="--ollama-url" (
  set "OLLAMA_URL=%~2"
  shift
  shift
  goto parse
)
if "%~1"=="-h" goto help
if "%~1"=="--help" goto help

echo Unknown arg: %1
exit /b 1

:help
echo Usage: %~nx0 [--install] [--ollama-url URL]
exit /b 0

:afterparse
if "%OLLAMA_URL%"=="" set "OLLAMA_URL=http://localhost:11434"
set "OLLAMA_BASE_URL=%OLLAMA_URL%"
echo Using OLLAMA_BASE_URL=%OLLAMA_BASE_URL%

if "%INSTALL%"=="1" (
  echo Installing backend dependencies...
  pip install -r backend\requirements.txt || exit /b 1
)

python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
