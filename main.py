import sqlite3
from fastapi import FastAPI

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
    customers = cur.execute(
    "SELECT CustomerID id, COALESCE(CompanyName, '') name, "
    "COALESCE(Address, '') || ' ' || COALESCE(PostalCode, '') || ' ' || COALESCE(City, '') || ' ' || "
    "COALESCE(Country, '') full_address "
    "FROM Customers c ORDER BY UPPER(CustomerID);"
    ).fetchall()
    return dict(customers=customers)

'''


@app.get("/suppliers/{supplier_id}")
async def single_supplier(supplier_id: int):
    app.db_connection.row_factory = sqlite3.Row
    data = app.db_connection.execute(
        f"SELECT CompanyName, Address FROM Suppliers WHERE SupplierID = {supplier_id}").fetchone()

    return data
    '''