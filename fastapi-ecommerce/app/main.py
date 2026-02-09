from fastapi import FastAPI, HTTPException, Query, Path
from service.products import get_all_products
from schema.product import Product



app = FastAPI()

@app.get('/')
def root():
    return {"message": "Welcome to FASTAPI."}

# @app.get('/products/{id}')
# def get_products(id:int):
#     products = ["Brush", "Laptop", "Mouse", "Monitor"]
#     return (
#         products[id] 
#         if products[id] else 
#         HTTPException(status_code=404, detail ="No Product found")
#     )


# @app.get("/products")
# def get_products():
#     return get_all_products()


@app.get("/products")
def list_products(
    name: str = Query(
        default=None,
        min_length=1,
        max_length=50,
        description="Search by product name (Case insensitive)",
        examples="Realme"
    ),
    sort_by_price: bool = Query(
        default=False, 
        description="Sort products by price"
    ),
    order: str = Query(
        default="asc", 
        description="Sort order when sort_by_price=true (asc/desc order)"
    ),
    limit: int = Query(
        default=10,
        ge=1,
        le=100,
        description="Number of items to return",
    ),
    offset: int = Query(
        default=10,
        ge=0,
        description="Pagination offset",
    ),
):  

    products = get_all_products()
    
    if name:
        needle = name.strip().lower()
        products = [p for p in products if needle in p.get("name", "").lower()]
    
    if not products:
        raise HTTPException(
            status_code=404, detail=f"No product found with matching name={name}"
        )
    
    if sort_by_price:
        reverse = order=="desc"
        products = sorted(products, key=lambda p: p.get("price", 0), reverse=reverse)
        
    products = products[offset : offset+limit]
    total = len(products)

    return ({
            "total": total,
            "items": products
        }
    )



@app.get("/products/{product_id}")
def get_product_by_id(
    product_id: str = Path(
        ..., 
        min_length=36, 
        max_length=36, 
        description="UUID of the products",
        examples="0005a4ea-ce3f-4dd7-bee0-f4ccc70fea6a",
    )
):
    products = get_all_products()
    for product in products:
        if product["id"] == product_id:
            return product

    raise HTTPException(status_code=404, detail="Product not found")




@app.post("/products", status_code=201)
def create_product(product: Product):
    return product