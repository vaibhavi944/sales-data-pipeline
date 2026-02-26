# Sales Data Pipeline (ETL + SQL + FastAPI)

End-to-end data engineering pipeline that ingests raw retail sales data, cleans and transforms it, stores it in a SQL database, and exposes business insights through REST APIs.

## Architecture
Raw CSV → Python (Pandas) → SQLite → SQL Queries → FastAPI → Swagger API

## Features
- Automated data cleaning & transformation
- ~100,000 transaction dataset simulation
- SQLite database integration
- Business analytics queries:
  - Total revenue
  - Top-selling products
  - Monthly revenue trends
- REST API endpoints using FastAPI

## Tech Stack
- Python
- Pandas
- SQLite
- SQLAlchemy
- FastAPI

## How to Run

### Setup environment
python -m venv venv  
source venv/Scripts/activate  
pip install -r requirements.txt  

### Run pipeline
python pipeline.py  

### Start API server
uvicorn api:app  

Open browser:
http://127.0.0.1:8000/docs

## API Endpoints
- /total-revenue
- /top-products
- /monthly-revenue