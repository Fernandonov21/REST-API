from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(
    title="Product API",
    description="A simple API that manages products and their details.",
    version="1.0.0"
)

# Product model
class Product(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None

# Simulated products database (in-memory)
products_db = [
    Product(id=1, name="T-shirt", description="Cotton T-shirt", price=20.5, tax=2.0),
    Product(id=2, name="Shoes", description="Sport shoes", price=50.0, tax=5.0)
]

@app.get("/", tags=["Root"])
def read_root():
    """
    Root route that shows a welcome message.
    This route can be used to verify that the API is working correctly.
    """
    return {"message": "Welcome to the Product API!"}

@app.get("/products/", tags=["Products"])
def get_products():
    """
    Returns all the available products.
    """
    return products_db

@app.get("/products/{product_id}", tags=["Products"])
def get_product(product_id: int):
    """
    Returns the details of a specific product by its ID.
    
    - **product_id**: The ID of the product you want to retrieve.
    """
    for product in products_db:
        if product.id == product_id:
            return product
    return {"message": "Product not found"}

@app.post("/products/", tags=["Products"])
def create_product(product: Product):
    """
    Creates a new product with the provided data.
    
    - **product**: The `Product` object containing the name, description, price, and optionally the tax.
    """
    products_db.append(product)
    return {"message": "Product created successfully", "product": product}
