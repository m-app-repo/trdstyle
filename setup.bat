@echo off
:: Batch script to set up a Python virtual environment and install dependencies

:: Check if Python is installed
python --version
if %errorlevel% neq 0 (
    echo Python is not installed. Please install Python before running this script.
    pause
    exit /b 1
)

:: Create a virtual environment called "trading_env"
echo Creating virtual environment...
python -m venv trading_env

:: Activate the virtual environment
echo Activating virtual environment...
 

:: Upgrade pip to the latest version
echo Upgrading pip...
python -m pip install --upgrade pip

:: Install required dependencies
echo Installing dependencies...
pip install PySide6
pip install breeze-connect
pip install pandas
pip install dask
pip install dask[dataframe]

:: Deactivate virtual environment and finish
echo Virtual environment setup complete. You can now activate it using "trading_env\Scripts\activate".
echo To run the application, activate the virtual environment and then execute "python your_script.py".
deactivate

pause
