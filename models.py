from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.sql import func
import barcode
from barcode.writer import ImageWriter

Base = declarative_base()

class Product(Base):
    __tablename__ = 'products'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    barcode = Column(String, unique=True)

    def generate_barcode(self):
        code = barcode.get('code128', str(self.id), writer=ImageWriter())
        barcode_path = f"barcodes/{self.id}.png"
        code.save(barcode_path)
        self.barcode = barcode_path

class Sale(Base):
    __tablename__ = 'sales'
    
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    total_price = Column(Float, nullable=False)
    date_created = Column(DateTime(timezone=True), server_default=func.now())
    
    product = relationship('Product')

class Counter(Base):
    __tablename__ = 'counters'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    
    sales = relationship('Sale')
