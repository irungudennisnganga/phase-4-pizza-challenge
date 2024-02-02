from flask import Flask, make_response,jsonify,request
from flask_migrate import Migrate
from flask_restful import Api,Resource
from models import db,Restaurant,RestaurantPizza,Pizza
from flask_cors import CORS
app = Flask(__name__)
api=Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

CORS(app)

db.init_app(app)

class RestaurantData(Resource):
    def get(self):
        data =[one.to_dict() for one in Restaurant.query.all()]

        response=make_response(
            data,
            200
        )
        return response
    
 
   

class RestaurantById(Resource):
   
    def get(self,id):
       
        data =Restaurant.query.filter_by(id=id).first()
        response_dict=data.to_dict()

        response=make_response(
        response_dict,
            200
        )
        
        return response
    
    def delete(self,id):
        data =Restaurant.query.filter_by(id=id).first()
        
        for one in RestaurantPizza.query.filter_by(restaurant_id=id).all():
            db.session.delete(one)
        
        db.session.delete(data)
        db.session.commit()
        
        response_dict = {}

        response = make_response(
            response_dict,
            200
        )

        return response
        
    
   
    

class PizzaData(Resource):
    def get(self):
        data =[one.to_dict() for one in Pizza.query.all()]

        response=make_response(
            jsonify(data),
            200
        )
        
        return response
    
    
    
    
    
    
class RestaurantPizzaData(Resource):
    def post(self):
        data = request.get_json()
        price = data.get('price')   
        pizza_id = data.get('pizza_id')
        restaurant_id = data.get('restaurant_id')

        if price is None or pizza_id is None or restaurant_id is None:
            return make_response(jsonify({'errors': ['Missing required data']}), 400)
        
        new_restaurantpizza = RestaurantPizza(price=price, pizza_id=pizza_id, restaurant_id=restaurant_id)

        try:
            db.session.add(new_restaurantpizza)
            db.session.commit()
            data =Pizza.query.filter_by(id=pizza_id).first()

            response_dict =data.to_dict()

            response = make_response(
                jsonify(response_dict),
                200
            )
            
            return response

        except Exception as e:
            return make_response(jsonify({'errors': 'failed to add'}, 400))
            


api.add_resource(RestaurantData, '/restaurants') 
api.add_resource(RestaurantById, '/restaurant/<int:id>')    
api.add_resource(PizzaData, '/pizzas')    
api.add_resource(RestaurantPizzaData, '/restaurant_pizzas')