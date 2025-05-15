@echo off
echo Creating virtual environment...
python -m venv venv

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Installing dependencies...
pip install -r requirements.txt

echo Creating .env file...
echo RIOT_API_KEY=your_api_key_here > .env

echo Setup complete! To start the application:
echo 1. Activate the virtual environment: venv\Scripts\activate.bat
echo 2. Run the application: uvicorn main:app --reload 