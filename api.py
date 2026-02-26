from fastapi import FastAPI
from sqlalchemy import create_engine
import pandas as pd

app = FastAPI()

# connect to database
engine = create_engine("sqlite:///database/sales.db")

# endpoint 1: total revenue
@app.get("/total-revenue")
def get_total_revenue():
    query = "SELECT SUM(revenue) as total_revenue FROM sales_data"
    result = pd.read_sql(query, engine)
    return result.to_dict(orient="records")

# endpoint 2: top products
@app.get("/top-products")
def get_top_products():
    query = """
    SELECT product_name, SUM(revenue) as total_sales
    FROM sales_data
    GROUP BY product_name
    ORDER BY total_sales DESC
    LIMIT 5
    """
    result = pd.read_sql(query, engine)
    return result.to_dict(orient="records")

# endpoint 3: monthly revenue
@app.get("/monthly-revenue")
def get_monthly_revenue():
    query = """
    SELECT strftime('%Y-%m', order_date) as month,
    SUM(revenue) as monthly_revenue
    FROM sales_data
    GROUP BY month
    ORDER BY month
    """
    result = pd.read_sql(query, engine)
    return result.to_dict(orient="records")