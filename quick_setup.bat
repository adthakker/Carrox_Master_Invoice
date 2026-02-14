@echo off
REM Quick Build Script for Invoice PDF Generator (Windows)

echo ==============================================
echo Invoice PDF Generator - Quick Setup
echo ==============================================
echo.

REM Check Docker
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo X Docker not found. Please install Docker Desktop:
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
    echo X Docker is not running. Please start Docker Desktop.
    pause
    exit /b 1
)

echo [OK] Docker is running
echo.

REM Build image
echo Building Docker image 'invoice-pdf-generator'...
echo This may take 2-3 minutes...
echo.

docker build -t invoice-pdf-generator .

if %errorlevel% equ 0 (
    echo.
    echo [OK] Docker image built successfully!
    echo.
    echo Image info:
    docker images invoice-pdf-generator
    echo.
    echo ==============================================
    echo Setup Complete!
    echo ==============================================
    echo.
    echo You can now generate PDFs:
    echo   python generate_invoice.py
    echo.
    echo Or programmatically:
    echo   from generate_invoice import generate_invoice_html
    echo   generate_invoice_html('data.json', generate_pdf=True)
    echo.
) else (
    echo.
    echo X Docker build failed
    pause
    exit /b 1
)

pause
