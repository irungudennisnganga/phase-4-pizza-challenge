from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates

db = SQLAlchemy()

class Restaurant(db.Model, SerializerMixin):
    __tablename__ = 'restaurants'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)

    restaurantspizzas = db.relationship("RestaurantPizza", back_populates='restaurant')  
    serialize_rules = ('-restaurantspizzas.restaurant',)


class Pizza(db.Model, SerializerMixin):
    __tablename__ = 'pizzas'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    ingredients = db.Column(db.String, nullable=False)

    restaurantspizzas = db.relationship("RestaurantPizza", back_populates='pizza')  
    serialize_rules = ('-restaurantspizzas.pizza',)


class RestaurantPizza(db.Model, SerializerMixin):
    __tablename__ = 'restaurantspizzas'

    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer,  default=0)
    pizza_id = db.Column(db.Integer, db.ForeignKey('pizzas.id'), nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'), nullable=False)

    restaurant = db.relationship("Restaurant", back_populates='restaurantspizzas')  
    pizza = db.relationship("Pizza", back_populates='restaurantspizzas')  

    serialize_rules = ('-restaurant', '-pizza')
    
    @validates('price')
    def validate_strength(self, key, value):
        pass