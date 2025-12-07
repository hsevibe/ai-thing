# Online River

A FastAPI application for online machine learning using the River library.

## What to download
- Python 3.14 or higher
- [Poetry](https://python-poetry.org/) for dependency management

## How to run
1. Install dependencies: `poetry install`
2. Run the app: `poetry run python main.py`

The app will start on http://0.0.0.0:8000

## What every file is for
- `main.py`: Entry point that starts the FastAPI server using uvicorn.
- `router.py`: Defines the FastAPI app with `/learn` and `/predict` endpoints for online learning and prediction.
- `model.py`: Contains the online learning model pipeline using the River library, including preprocessing and AMFClassifier.
- `dto.py`: Pydantic models for API requests/responses (Features, Data, etc.) and ModelState class for thread-safe model management.
