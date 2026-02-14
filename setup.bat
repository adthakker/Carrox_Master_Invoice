@echo off
REM Invoice PDF Generator - Setup Script (Windows)
REM Version: 1.0 (Final)

echo ==============================================
echo Invoice PDF Generator - Setup
echo ==============================================
echo.

REM Check Docker
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo X Docker not found!
    echo   Please install Docker Desktop:
    echo   https://www.docker.com/products/docker-desktop
    pause
    exit /b 1
)

echo [OK] Docker found
docker --version
echo.

REM Check Docker is running
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo X Docker is not running!
    echo   Please start Docker Desktop
    pause
    exit /b 1
)

echo [OK] Docker is running
echo.

REM Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Warning: Python not found (needed for invoice generation)
    echo    You can still build Docker image
    echo.
)

REM Build Docker image
echo ==============================================
echo Building Docker Image
echo ==============================================
echo.
echo Image name: carrox-invoice-pdf-generator
echo This may take 2-3 minutes...
echo.

docker build -t carrox-invoice-pdf-generator .

if %errorlevel% equ 0 (
    echo.
    echo [OK] Docker image built successfully!
    echo.
    echo Image details:
    docker images carrox-invoice-pdf-generator
    echo.
    echo ==============================================
    echo Setup Complete!
    echo ==============================================
    echo.
    echo Test PDF generation:
    echo   python generate_invoice.py
    echo.
    echo Or manually:
    echo   docker run --rm -v "%cd%":/data carrox-invoice-pdf-generator ^
    echo     /data/sample.html /data/sample.pdf
    echo.
    echo For more information, see README.md
    echo.
) else (
    echo.
    echo X Docker build failed!
    echo   Check error messages above
    pause
    exit /b 1
)

pause
