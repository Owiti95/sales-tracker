import click
from sqlalchemy.orm import Session
from models import Product, Sale, Counter
from products_service import create_product, delete_product, get_all_products
from sales_service import add_sale, get_sales
from database import SessionLocal
from barcode import Code128
from barcode.writer import ImageWriter
import os

# Function to generate a barcode and save it as an image
def generate_barcode(product_name):
    barcode = Code128(product_name, writer=ImageWriter())
    barcode_file = f"barcodes/{product_name}.png"
    barcode.save(barcode_file)
    return barcode_file

@click.group()
def cli():
    """Command Line Interface for Sales Tracker."""
    pass

@cli.command()
@click.option('--name', prompt='Product name', help='The name of the product.')
@click.option('--price', prompt='Product price', type=float, help='The price of the product.')
def add_product(name, price):
    """Add a new product."""
    with SessionLocal() as session:
        product = create_product(session, name, price)
        barcode_file = generate_barcode(product.name)
        click.echo(f"Product {product.name} added with price {product.price}. Barcode saved at {barcode_file}.")

@cli.command()
@click.option('--product_id', prompt='Product ID', type=int, help='The ID of the product to delete.')
def remove_product(product_id):
    """Remove a product."""
    with SessionLocal() as session:
        try:
            delete_product(session, product_id)
            click.echo(f"Product with ID {product_id} deleted.")
        except ValueError as e:
            click.echo(str(e))

@cli.command()
def list_products():
    """List all products."""
    with SessionLocal() as session:
        products = get_all_products(session)
        if products:
            for product in products:
                click.echo(f"ID: {product.id}, Name: {product.name}, Price: {product.price}")
        else:
            click.echo("No products found.")

@cli.command()
@click.option('--product_id', prompt='Product ID', type=int, help='The ID of the product being sold.')
@click.option('--quantity', prompt='Quantity', type=int, help='Quantity of the product sold.')
def sell_product(product_id, quantity):
    """Record a sale."""
    with SessionLocal() as session:
        try:
            sale = add_sale(session, product_id, quantity)
            click.echo(f"Sale recorded: {sale.quantity} of Product ID {sale.product_id} sold for {sale.total_price}.")
        except ValueError as e:
            click.echo(str(e))

@cli.command()
def list_sales():
    """List all sales."""
    with SessionLocal() as session:
        sales = get_sales(session)
        if sales:
            for sale in sales:
                click.echo(f"Sale ID: {sale.id}, Product ID: {sale.product_id}, Quantity: {sale.quantity}, Total Price: {sale.total_price}")
        else:
            click.echo("No sales recorded.")

@cli.command()
@click.option('--name', prompt='Counter name', help='The name of the counter.')
def add_counter(name):
    """Add a new counter."""
    with SessionLocal() as session:
        counter = Counter(name=name)
        session.add(counter)
        session.commit()
        click.echo(f"Counter {counter.name} added.")

@cli.command()
def list_counters():
    """List all counters."""
    with SessionLocal() as session:
        counters = session.query(Counter).all()
        if counters:
            for counter in counters:
                click.echo(f"Counter ID: {counter.id}, Name: {counter.name}")
        else:
            click.echo("No counters found.")

if __name__ == '__main__':
    cli()
