from socket import SO_VM_SOCKETS_BUFFER_MAX_SIZE
from flask import Flask, jsonify, send_file, request, make_response
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import json
from models import db, Product, User, Sessions, ProductsBought, ProductsInBag
from helperFunctions import hashFunction, isUserValid, createSession

app = Flask(__name__)
app.config.from_object(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True	
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db.init_app(app)
app.app_context().push()



CORS(app, origins='http://localhost:8080', supports_credentials=True)

@app.route('/products/<filter>')
def products(filter):

  products = []

  if filter == 'women':
    for i in Product.query.filter_by(isForWomen = True).all():
      products.append({'id': i.id, 'name':i.name, 'price':i.price, 'sizesOnStock': i.sizesOnStock.split(', ')})
  elif filter == 'men':
    for i in Product.query.filter_by(isForMen = True).all():
      products.append({'id': i.id, 'name':i.name, 'price':i.price, 'sizesOnStock': i.sizesOnStock.split(', ')}) 

  elif filter.split(',')[0].isnumeric():
    for i in filter.split(','):
      product = Product.query.filter_by(id=int(i)).first()
      products.append({'id': product.id, 'name': product.name, 'price': product.price, 'sizesOnStock': product.sizesOnStock.split(', ')})

  else:
    product = Product.query.filter_by(name = filter).first()
    try:
      return jsonify({'id': product.id, 'name': product.name, 'price': product.price, 'sizesOnStock': product.sizesOnStock.split(', ')})
    except:
      response = make_response("product(s) is not exist")
      response.status_code = 406
      return  response
    
  return jsonify(products)

@app.route('/images/<path:name>')
def showImage(name):
	return send_file(f'images/{name}')

@app.route('/sign-user', methods=['POST'])
def signUser():

	data = json.loads(request.data)
	if User.query.filter_by(email=data['email']).first() != None:
		return jsonify({'msg': 'email already taken', 'success': False, 'cause':'email'})

	if User.query.filter_by(username=data['username']).first() != None:
		return jsonify({'msg': 'username already taken', 'success': False, 'cause':'username'})

	user = User(email=data['email'], username=data['username'], password_hash=hashFunction(data['password']))
	db.session.add(user)
	db.session.commit()
	
	return jsonify({'msg': 'user successfully signed', 'success': True})

@app.route('/log-user', methods=['POST'])
def logUser():

    data = json.loads(request.data)

    if not isUserValid(data['email_username'], data['password']): 
        return jsonify({'msg': 'Username or password is wrong. ', 'success': False})

    sessionId = createSession(data['email_username'])

    responseData = jsonify({'msg': 'User successfully logged in.', 'success': True})
    response = make_response(responseData)
    response.set_cookie('sessionId', sessionId)

    return response

@app.route('/get-user-data', methods=['POST'])
def get_user_data():

    sessionId = json.loads(request.data)['sessionId']
    userId = Sessions.query.filter_by(sessionId=sessionId).first().userId
    user = User.query.filter_by(id=userId).first()
    
    userInfo = {
        'username': user.username,
        'email': user.email,
        'address': user.address
    }

    return jsonify({'msg': 'user successfully logged in', 'user_data': userInfo, 'success': True})

@app.route('/update-user', methods=['PUT'])
def update_user():     

    data = json.loads(request.data)
    sessionId = data['sessionId']
    session = Sessions.query.filter_by(sessionId=sessionId).first()
    if session == None:
        response = make_response(jsonify({'msg': 'unauthorized', 'success': False}))
        response.status_code = 401
        return response


    userId = session.userId
    user = User.query.filter_by(id=userId).first()

    user.email = data['email']
    user.username = data['username']
    user.address = data['address']
    db.session.commit()
     
    return jsonify({'msg': 'successfully changed', 'success': True})

@app.route('/update-bag', methods=['POST', 'DELETE'])
def add_to_bag():
    
    if request.method == 'DELETE':
        data = json.loads(request.data)
        sessionId = data['sessionId']
        productId = data['productId']
        userId = Sessions.query.filter_by(sessionId=sessionId).first().userId
        size = data['size']

        product = ProductsInBag.query.filter_by(productId=productId, userId=userId, size=size).first()
        db.session.delete(product)
        db.session.commit()

        return jsonify({'msg': 'product succesfully removed from bag', 'success': True}) 

    data = json.loads(request.data)
    sessionId = data['sessionId']
    product_name = data['productName']

    product = Product.query.filter_by(name=product_name).first()
    productId = product.id    

    session = Sessions.query.filter_by(sessionId=sessionId).first()
    userId = session.userId
    
    product_size = data['size']
    
    newProduct = ProductsInBag(productId=productId, userId=userId, size=product_size)
    db.session.add(newProduct)
    db.session.commit()

    return jsonify({'msg': 'product successfully added to the bag', 'success': True})

@app.route('/products-in-bag', methods=['POST'])
def products_in_bag():
    
    sessionId = json.loads(request.data)['sessionId']
    userId = Sessions.query.filter_by(sessionId=sessionId).first().userId

    products = ProductsInBag.query.filter_by(userId=userId).all()

    product_data = []
    for i in products:
        product_data.append({'id': i.productId, 'size': i.size})

    return jsonify({'product_data': product_data})
 
if __name__ == "__main__":
    app.run(debug=True)
