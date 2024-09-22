from models import Sale, Product
from sqlalchemy.orm import Session

def add_sale(session: Session, product_id: int, quantity: int):
    product = session.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise ValueError(f"Product with ID {product_id} not found.")
    
    total_price = product.price * quantity
    sale = Sale(product_id=product_id, quantity=quantity, total_price=total_price)
    session.add(sale)
    session.commit()
    return sale

def get_sales(session: Session):
    return session.query(Sale).all()
