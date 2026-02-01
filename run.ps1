# PowerShell script to run the Command Chat Assistant

Write-Host "Command Chat Assistant - Setup and Run" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

# Check if virtual environment exists
if (-not (Test-Path "venv")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Error creating virtual environment" -ForegroundColor Red
        exit 1
    }
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1

# Install/update dependencies
Write-Host "Installing dependencies..." -ForegroundColor Yellow
pip install -q -r requirements.txt
if ($LASTEXITCODE -ne 0) {
    Write-Host "Error installing dependencies" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Starting Command Chat Assistant..." -ForegroundColor Green
Write-Host ""

# Run the application
python command_chat_app.py
