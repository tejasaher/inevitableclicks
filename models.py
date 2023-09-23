from flask_sqlalchemy import SQLAlchemy
 
 db = SQLAlchemy()
 
 class Product(db.Model):
     id = db.Column(db.Integer, primary_key=True)
     name = db.Column(db.String(100))
     price = db.Column(db.Float)
     description = db.Column(db.Text)
 
     def __init__(self, name, price, description):
         self.name = name
         self.price = price
         self.description = description
 
 # Example product data
 products_data = [
     {
         'name': 'Product 1',
         'price': 19.99,
         'description': 'Description for Product 1.'
     },
     {
         'name': 'Product 2',
         'price': 29.99,
         'description': 'Description for Product 2.'
     },
     {
         'name': 'Product 3',
         'price': 39.99,
         'description': 'Description for Product 3.'
     },
     # Add more products as needed
 ]
