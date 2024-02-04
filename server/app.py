from flask import Flask, make_response,jsonify,request
from flask_migrate import Migrate
from flask_restful import Api,Resource
from models import db,Restaurant,RestaurantPizza,Pizza
from flask_cors import CORS


app = Flask(__name__)
api=Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False


migrate = Migrate(app, db)

CORS(app)

db.init_app(app)

class RestaurantData(Resource):
    def get(self):
        data =[{'id':one.id,'name':one.name,'address':one.address} for one in Restaurant.query.all()]

        response=make_response(
            data,
            200
        )
        return response
    
 
   

class RestaurantById(Resource):
   
    def get(self,id):
       
        data =Restaurant.query.filter_by(id=id).first()
        response_dict={'id':data.id,'name':data.name,'address':data.address,'pizzas':[]}
        for pizza in data.pizzas:
            data ={
                'id':pizza.id,
                'name':pizza.name,
                'ingredients':pizza.ingredients
                
            }
            
            
        response_dict['pizzas'].append(data)
        response=make_response(
        response_dict,
            200
        )
        
        return response
    
    def delete(self,id):
        data =Restaurant.query.filter_by(id=id).first()
        if not data:
            return make_response(jsonify({'errors': ['Missing required data']}), 400)
        
        RestaurantPizza.query.filter_by(restaurant_id=id).delete()
            
        db.session.delete(data)
        db.session.commit()
        
        response_dict = {}

        response = make_response(
            jsonify(response_dict),
            200
        )

        return response
        
    
   
    

class PizzaData(Resource):
    def get(self):
        data =[{'id':one.id,'ingredients':one.ingredients, 'name':one.name} for one in Pizza.query.all()]

        response=make_response(
            jsonify(data),
            200
        )
        
        return response
    
    
    
    
    
    
class RestaurantPizzaData(Resource):
    def post(self):
        data = request.json
        price = data['price'] 
        pizza_id = data['pizza_id']
        restaurant_id = data['restaurant_id']

        if price is None or pizza_id is None or restaurant_id is None:
            return make_response(jsonify({'errors': ['Missing required data']}), 400)
        
        new_restaurantpizza = RestaurantPizza(price=price, pizza_id=pizza_id, restaurant_id=restaurant_id)

        
        db.session.add(new_restaurantpizza)
        db.session.commit()
        # data =Pizza.query.filter_by(id=pizza_id).all()
        
        response_dict={
            'id':new_restaurantpizza.pizzas.id,
            'name':new_restaurantpizza.pizzas.name,
            'ingredients':new_restaurantpizza.pizzas.ingredients
        }

        

        response = make_response(
            jsonify(response_dict),
            200
        )
        
        return response

        
        # return make_response(jsonify({'errors': 'failed to add'}, 400))
            


api.add_resource(RestaurantData, '/restaurants') 
api.add_resource(RestaurantById, '/restaurants/<int:id>')    
api.add_resource(PizzaData, '/pizzas')    
api.add_resource(RestaurantPizzaData, '/restaurant_pizzas')


if __name__ =="__main__":
    app.run(port=5555, debug=True)