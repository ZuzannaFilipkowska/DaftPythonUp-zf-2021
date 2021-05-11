import sqlite3
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


app = FastAPI()


class NewCategory(BaseModel):
    name: str


class Category(BaseModel):
    name: str
    id: int



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


@app.get("/employees")
async def all_employees(limit: int = -1, offset: int = 0, order: str = "EmployeeID"):
    order = order.strip()
    categories = {'last_name': 'LastName',
                 'first_name': 'FirstName',
                 'city': 'City',
                 'EmployeeID': 'EmployeeID',
                 '': "EmployeeID"}
    if order not in categories.keys():
        raise HTTPException(status_code=400)

    cur = app.db_connection.cursor()
    cur.row_factory = sqlite3.Row

    workers = cur.execute(
        f"SELECT EmployeeID id, LastName last_name, FirstName first_name, City city FROM Employees ORDER BY {categories[order]} LIMIT :lim OFFSET :off"
        , {"lim": limit, "off": offset}
    ).fetchall()
    return dict(employees=workers)


@app.get("/products_extended")
async def get_product_extended():
    cur = app.db_connection.cursor()
    cur.row_factory = sqlite3.Row
    product = cur.execute('''
        SELECT Products.ProductID id, Products.ProductName name, Categories.CategoryName category, Suppliers.CompanyName supplier
        FROM Products LEFT JOIN Categories ON Products.CategoryID = Categories.CategoryID
        LEFT JOIN Suppliers ON Products.SupplierID = Suppliers.SupplierID ORDER BY Products.ProductID
    ''').fetchall()
    return dict(products_extended=product)


@app.get("/products/{id}/orders", status_code=201)
async def get_specific_order(id: int):
    cur = app.db_connection.cursor()
    cur.row_factory = sqlite3.Row
    product = cur.execute(
        "SELECT p.ProductID FROM Products p where p.ProductID = ?", (id,)
    ).fetchone()
    if not product:
        raise HTTPException(status_code=404)
    orders = cur.execute(
        "SELECT o.OrderID id, c.CompanyName customer, od.Quantity quantity, "
        "ROUND((od.UnitPrice * od.Quantity) - (od.Discount * od.UnitPrice * od.Quantity), 2) total_price "
        "FROM Orders o INNER JOIN 'Order Details' od on o.OrderID = od.OrderID "
        "INNER JOIN Products p on od.ProductID = p.ProductID LEFT JOIN Customers c on o.CustomerID = c.CustomerID "
        "WHERE p.ProductID = ? ORDER BY o.OrderID", (id,)
    ).fetchall()
    return dict(orders=orders)


@app.post("/categories", status_code=201, response_model=Category)
async def add_caegory(cat: NewCategory):
    cur = app.db_connection.cursor()
    cur.execute(
        "INSERT INTO Categories (CategoryName) VALUES (?);", (cat.name,)
    )
    added_cat = Category(name=cat.name, id=cur.lastrowid) # last inserted row id
    app.db_connection.commit()
    return added_cat


@app.put("/categories/{id}")
async def modyfy_cat(id: int):
    cur = app.db_connection.cursor()
    # TO DO


@app.delete("/categories/{id}")
async def delete_cat(id: int):
    cur = app.db_connection.cursor()
    # TO DO
