# FastAPI
Learning to build a full-fledged API in Python using FastAPI

## Setting Virtual Enviromnent
    Creating:
    $ py -3 -m venv venv

    Activating:
    $ .\venv\Scripts\Activate.ps1 or $ .\venv\Scripts\activate.bat

## Set the Virtual Enviromnent as a default interpreter on VS CODE
    1. ctrl + p
    2. Python: Select Interpreter
    3. Select python.exe (venv\Scripts\python.exe) as main interpreter

## Install FastAPI
    Installing:
    $ pip install fastapi[all]
    
    Checking packages:
    $ pip freeze

## Starting API
    $ unicorn FILENAME:INSTANCE_NAME --reload

    Example:
    $ unicorn main:app --reload

