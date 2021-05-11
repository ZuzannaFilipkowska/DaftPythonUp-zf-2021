import sqlite3
from fastapi import FastAPI, HTTPException

app = FastAPI()


@app.on_event("startup")
async def startup():
    app.db_connection = sqlite3.connect("northwind.db")
    app.db_connection.text_factory = lambda b: b.decode(errors="ignore")  # northwind specific


@app.on_event("shutdown")
async def shutdown():
    app.db_connection.close()


@app.get("/categories")
async def get_cat():
    cur = app.db_connection.cursor()
    cat = cur.execute("SELECT CategoryID, CategoryName FROM Categories ORDER BY CategoryID").fetchall()
    return dict(categories=[dict(id=category[0], name=category[1]) for category in cat])


@app.get("/customers")
async def get_customers():
    cur = app.db_connection.cursor()
    cur.row_factory = sqlite3.Row
    customers = cur.execute(
    "SELECT CustomerID id, COALESCE(CompanyName, '') name, "
    "COALESCE(Address, '') || ' ' || COALESCE(PostalCode, '') || ' ' || COALESCE(City, '') || ' ' || "
    "COALESCE(Country, '') full_address "
    "FROM Customers c ORDER BY UPPER(CustomerID);"
    ).fetchall()
    return dict(customers=customers)


@app.get("/products/{id}")
async def single_product(id: int):
    cur = app.db_connection.cursor()
    cur.row_factory = sqlite3.Row
    product = cur.execute(
        "SELECT ProductID id, ProductName name FROM Products WHERE ProductID = ?",
        (id, )).fetchone()
    if product:
        return product
    raise HTTPException(status_code=404)
