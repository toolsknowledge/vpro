@echo off
REM One-command setup and launch for the VPRO Skills Adaptive RAG Assistant (Windows).
REM
REM   start.bat                full setup, tests, build, then start both servers
REM   start.bat --skip-checks  skip backend tests and the frontend build
REM
REM The backend and frontend open in two separate windows. Close those windows
REM (or press Ctrl+C in each) to stop them.

setlocal EnableExtensions EnableDelayedExpansion
set "ROOT=%~dp0"
set "ROOT=%ROOT:~0,-1%"
set "BACKEND=%ROOT%\backend"
set "FRONTEND=%ROOT%\frontend"
set "VENV=%ROOT%\.venv"
set "PY=%VENV%\Scripts\python.exe"
set "SKIP_CHECKS=0"
if /I "%~1"=="--skip-checks" set "SKIP_CHECKS=1"

echo.
echo ==^> Checking Python and Node.js
set "PYTHON_BIN="
for %%P in ("py -3.11" "py -3.12" "py -3.13" "python") do (
  if not defined PYTHON_BIN (
    %%~P -c "import sys; sys.exit(0 if (3, 10) <= sys.version_info[:2] < (3, 14) else 1)" >nul 2>&1 && set "PYTHON_BIN=%%~P"
  )
)
if not defined PYTHON_BIN (
  echo ERROR: Python 3.10-3.13 was not found.
  echo Fix: Install Python 3.11 from https://www.python.org/downloads/ ^(tick "Add to PATH"^) and re-run.
  exit /b 1
)
%PYTHON_BIN% --version
where node >nul 2>&1 || (
  echo ERROR: Node.js was not found.
  echo Fix: Install Node.js 20.19+ or 22+ from https://nodejs.org/ and re-run.
  exit /b 1
)
node -e "const [a,b]=process.versions.node.split('.').map(Number); process.exit(a>22||(a===22&&b>=12)||(a===20&&b>=19)?0:1)" || (
  echo ERROR: Your Node.js version is too old for Vite.
  echo Fix: Install Node.js 20.19+ or 22.12+ and re-run.
  exit /b 1
)
for /f "delims=" %%V in ('node --version') do echo Node.js %%V

echo.
echo ==^> Preparing Python virtual environment
if not exist "%PY%" (
  %PYTHON_BIN% -m venv "%VENV%" || (
    echo ERROR: Could not create the virtual environment.
    exit /b 1
  )
)
set "REQ_HASH="
for /f "delims=" %%H in ('"%PY%" -c "import hashlib,sys; print(hashlib.sha256(open(sys.argv[1],'rb').read()).hexdigest())" "%ROOT%\requirements.txt"') do set "REQ_HASH=%%H"
set "OLD_HASH="
if exist "%VENV%\.deps-installed" set /p OLD_HASH=<"%VENV%\.deps-installed"
if not "%OLD_HASH%"=="%REQ_HASH%" (
  "%PY%" -m pip install --upgrade pip >nul
  "%PY%" -m pip install -r "%ROOT%\requirements.txt" || (
    echo ERROR: Installing Python dependencies failed ^(see output above^).
    echo Fix: Check your network, then run: "%PY%" -m pip install -r requirements.txt
    exit /b 1
  )
  >"%VENV%\.deps-installed" echo %REQ_HASH%
) else (
  echo Python dependencies already up to date
)

echo.
echo ==^> Generating missing sample documents
"%PY%" "%BACKEND%\scripts\create_sample_files.py" || (
  echo ERROR: Sample document generation failed.
  exit /b 1
)

echo.
echo ==^> Installing frontend dependencies
if not exist "%FRONTEND%\node_modules" (
  pushd "%FRONTEND%"
  call npm ci || (
    popd
    echo ERROR: npm ci failed ^(see output above^).
    echo Fix: cd frontend ^&^& npm ci
    exit /b 1
  )
  popd
) else (
  echo Frontend dependencies already installed ^(delete frontend\node_modules to force a reinstall^)
)

echo.
echo ==^> Checking configuration
if not exist "%BACKEND%\.env" (
  copy "%BACKEND%\.env.example" "%BACKEND%\.env" >nul
  echo Created backend\.env from .env.example
) else (
  echo backend\.env exists ^(left unchanged^)
)
if not exist "%FRONTEND%\.env" copy "%FRONTEND%\.env.example" "%FRONTEND%\.env" >nul
findstr /R /C:"^OPENAI_API_KEY=..*" "%BACKEND%\.env" >nul || echo WARNING: OPENAI_API_KEY is empty in backend\.env - the UI starts, but chat and indexing need a key.

set "API_HOST=127.0.0.1"
set "API_PORT=8000"
for /f "tokens=1,* delims==" %%A in ('findstr /R "^API_HOST= ^API_PORT=" "%BACKEND%\.env"') do (
  if not "%%B"=="" set "%%A=%%B"
)

if "%SKIP_CHECKS%"=="0" (
  echo.
  echo ==^> Running backend tests
  pushd "%BACKEND%"
  "%PY%" -m pytest || (
    popd
    echo ERROR: Backend tests failed ^(see output above^).
    echo Fix: Fix the failing tests, or run "start.bat --skip-checks" to start anyway.
    exit /b 1
  )
  popd
  echo.
  echo ==^> Building frontend ^(production check^)
  pushd "%FRONTEND%"
  call npm run build || (
    popd
    echo ERROR: Frontend build failed ^(see output above^).
    exit /b 1
  )
  popd
)

echo.
echo ==^> Starting servers in separate windows
start "Adaptive RAG Backend" cmd /k ""%PY%" -m uvicorn main:app --app-dir "%BACKEND%" --host %API_HOST% --port %API_PORT%"
start "Adaptive RAG Frontend" /D "%FRONTEND%" cmd /k "npm run dev"

echo.
echo   Frontend : http://localhost:5173
echo   Backend  : http://%API_HOST%:%API_PORT%   (API docs: http://%API_HOST%:%API_PORT%/docs)
echo.
echo   To stop: close the "Adaptive RAG Backend" and "Adaptive RAG Frontend" windows (or press Ctrl+C in each).
endlocal
