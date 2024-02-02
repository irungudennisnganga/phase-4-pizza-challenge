from models import db,Restaurant,RestaurantPizza,Pizza
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
engine = create_engine('sqlite:///instance/app.db')
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Example restaurants

with SessionLocal() as session:
    session.query(RestaurantPizza).delete()  # Delete associations first
    session.query(Pizza).delete()
    session.query(Restaurant).delete()  # Delete restaurants last (due to foreign keys)
    session.commit()
    
restaurants = [
    Restaurant(name="Pizza Palace", address="123 Main St"),
    Restaurant(name="Slice of Life", address="456 Elm St"),
]

# Example pizzas
pizzas = [
    Pizza(name="Pepperoni", ingredients="Pepperoni, cheese, sauce"),
    Pizza(name="Margherita", ingredients="Tomatoes, mozzarella, basil"),
    Pizza(name="Hawaiian", ingredients="Ham, pineapple, cheese"),
]

# Associate pizzas with restaurants using RestaurantPizza
restaurant_pizzas = [
    RestaurantPizza(restaurant=restaurants[0], pizza=pizzas[0], price=12),
    RestaurantPizza(restaurant=restaurants[0], pizza=pizzas[1], price=10),
    RestaurantPizza(restaurant=restaurants[1], pizza=pizzas[1], price=11),
    RestaurantPizza(restaurant=restaurants[1], pizza=pizzas[2], price=13),
]

# Add data to the database
with SessionLocal() as session:
    session.add_all(restaurants)
    session.add_all(pizzas)
    session.add_all(restaurant_pizzas)
    session.commit()

print("Seed data created successfully!")