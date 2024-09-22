from models import Product
from sqlalchemy.orm import Session

def create_product(session: Session, name: str, price: float):
    new_product = Product(name=name, price=price)
    new_product.generate_barcode()
    session.add(new_product)
    session.commit()
    return new_product

def get_all_products(session: Session):
    return session.query(Product).all()

def delete_product(session: Session, product_id: int):
    product = session.query(Product).filter(Product.id == product_id).first()
    if product:
        session.delete(product)
        session.commit()
    else:
        raise ValueError("Product not found")
