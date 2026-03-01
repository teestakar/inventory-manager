from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from model import Product
from database import session,engine
import database_model
from sqlalchemy.orm import Session
app=FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"]
)

database_model.Base.metadata.create_all(bind=engine)

@app.get("/")
def greet():
    return "Hi baby I love you"

products=[
    Product(id=1,name="phone",description="phone",price=15000,quantity=5),
    Product(id=2,name="laptop",description="laptop",price=50000,quantity=6),
    Product(id=3,name="t.v",description="t.v",price=100000,quantity=3)
]

def get_db():
    db=session()
    try:
        yield db
    finally:
        db.close()

def init_db():
    db=session()
    count=db.query(database_model.Product).count()
    if count==0:
        for product in products:
            db.add(database_model.Product(**product.model_dump()))
        
    db.commit()


init_db()

@app.get("/products")
def get_all_products(db:Session=Depends(get_db)):
    db_products=db.query(database_model.Product).all()
    return db_products

@app.get("/products/{id}")
def get_product_by_id(id:int,db:Session=Depends(get_db)):
    db_product=db.query(database_model.Product).filter(database_model.Product.id==id).first()
    if db_product:
        return db_product
    return "product not found"

@app.post("/products")
def add_product(product:Product,db:Session=Depends(get_db)):
    db.add(database_model.Product(**product.model_dump()))
    db.commit()
    return product

@app.put("/products/{id}")
def update_product(id:int,pro:Product,db:Session=Depends(get_db)):
    
    db_product=db.query(database_model.Product).filter(database_model.Product.id==id).first()
    if db_product:
        db_product.name=pro.name
        db_product.description=pro.description
        db_product.price=pro.price
        db_product.quantity=pro.quantity
        db.commit()
        return "Product updated"
    else:
        return "product not found"

@app.delete("/products/{id}")
def delete_product(id:int,db:Session=Depends(get_db)):
    db_product=db.query(database_model.Product).filter(database_model.Product.id==id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
        return "Product deleted"
    else:
        return"product not found"

