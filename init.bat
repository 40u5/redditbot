@echo off
echo ========================================
echo Reddit Bot Initialization Script
echo ========================================
echo.

echo Installing Python requirements...
echo.
set /p "pip_params=Enter additional pip install parameters (e.g., --upgrade --user) or press Enter to continue: "
echo.
if "%pip_params%"=="" (
    echo Running: pip install -r requirements.txt
    pip install -r requirements.txt
) else (
    echo Running: pip install %pip_params% -r requirements.txt
    pip install %pip_params% -r requirements.txt
)
if %errorlevel% neq 0 (
    echo Error: Failed to install requirements
    pause
    exit /b 1
)
echo Requirements installed successfully!
echo.

echo Checking environment file...
if exist .env (
    echo .env file already exists. Checking if it has configuration...
    findstr /C:"CLIENT_ID" .env >nul
    if %errorlevel% equ 0 (
        echo .env file exists and has configuration. Skipping .env creation.
    ) else (
        echo .env file exists but has no CLIENT_ID configuration. Creating new .env file...
        (
        echo # Reddit API Configuration
        echo CLIENT_ID=your_client_id_here
        echo SECRET_KEY=your_secret_key_here
        echo USERNAME=your_reddit_username_here
        echo PASSWORD=your_reddit_password_here
        ) > .env
    )
) else (
    echo Creating .env file with required parameters...
    (
    echo # Reddit API Configuration
    echo CLIENT_ID=your_client_id_here
    echo SECRET_KEY=your_secret_key_here
    echo USERNAME=your_reddit_username_here
    echo PASSWORD=your_reddit_password_here
    ) > .env
)

echo.
echo ========================================
echo Initialization Complete!
echo ========================================
echo.
echo IMPORTANT: Please edit the .env file and replace the placeholder values with your actual Reddit API credentials:
echo - CLIENT_ID: Your Reddit app client ID
echo - SECRET_KEY: Your Reddit app secret key  
echo - USERNAME: Your Reddit username
echo - PASSWORD: Your Reddit password
echo.
echo To get Reddit API credentials:
echo 1. Go to https://www.reddit.com/prefs/apps
echo 2. Click "Create App" or "Create Another App"
echo 3. Choose "script" as the app type
echo 4. Use the generated client ID and secret
echo.
echo After updating .env, you can run: python main.py
echo.
pause
