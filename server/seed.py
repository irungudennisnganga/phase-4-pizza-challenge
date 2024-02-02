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
    Restaurant(name="Big 5 Restaurant & Meeting Place", address="PM9R+JC6, Dagoretti Rd, Nairobi"),
    Restaurant(name="Five Senses Restaurant", address="2nd Floor Galana Plaza, off Galana Road"),
    Restaurant(name="5th Avenue Cafe", address="QR86+JMQ 238, United Nations Ave, Nairobi"),
    Restaurant(name="Big Five Restaurant", address="Ole Sereni Hotel, Mombasa Rd, 69671 - 00400, Nairobi"),
]

# Example pizzas
pizzas = [
    Pizza(name="Pepperoni", ingredients="Pepperoni, cheese, sauce"),
    Pizza(name="Margherita", ingredients="Tomatoes, mozzarella, basil"),
    Pizza(name="Marinara", ingredients="Marinara sauce, Garlic, Olive oil, Basil, Oregano"),
    Pizza(name="Mozzarella", ingredients="Tomato Sauce, Buffalo mozzarella"),
    Pizza(name="Mazza", ingredients="Tomato sauce, Mozzarella, Bacon, Eggs, Onions, Chili peppers"),
]

# Associate pizzas with restaurants using RestaurantPizza
restaurant_pizzas = [
    RestaurantPizza(restaurant=restaurants[5], pizza=pizzas[0], price=12),
    RestaurantPizza(restaurant=restaurants[0], pizza=pizzas[1], price=10),
    RestaurantPizza(restaurant=restaurants[1], pizza=pizzas[4], price=11),
    RestaurantPizza(restaurant=restaurants[2], pizza=pizzas[2], price=20),
    RestaurantPizza(restaurant=restaurants[1], pizza=pizzas[3], price=22),
    RestaurantPizza(restaurant=restaurants[3], pizza=pizzas[3], price=3),
    RestaurantPizza(restaurant=restaurants[4], pizza=pizzas[4], price=23),
    RestaurantPizza(restaurant=restaurants[5], pizza=pizzas[2], price=1),
]

# Add data to the database
with SessionLocal() as session:
    session.add_all(restaurants)
    session.add_all(pizzas)
    session.add_all(restaurant_pizzas)
    session.commit()

print("Seed data created successfully!")