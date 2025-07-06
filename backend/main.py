import os
from flask import Flask, jsonify, request, make_response, Response
import json
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from models import Product, User, Sessions, ProductsInBag
from helperFunctions import hashFunction, isUserValid, createSession
from flask_cors import CORS
from botocore.client import Config
import boto3

# Get environment variables
TURSO_DATABASE_URL = os.getenv("TURSO_DATABASE_URL")
TURSO_AUTH_TOKEN = os.getenv("TURSO_AUTH_TOKEN")
R2_ENDPOINT = os.getenv("R2_ENDPOINT")
R2_ACCESS_KEY_ID = os.getenv("R2_ACCESS_KEY_ID")
R2_SECRET_ACCESS_KEY = os.getenv("R2_SECRET_ACCESS_KEY")
R2_BUCKET = os.getenv("R2_BUCKET")

# construct special SQLAlchemy URL
dbUrl = f"sqlite+{TURSO_DATABASE_URL}/?secure=true"
engine = create_engine(dbUrl, connect_args={"auth_token": os.getenv("TURSO_AUTH_TOKEN")}, echo=True)
app = Flask(__name__)
CORS(app, origins='http://localhost:8080', supports_credentials=True)

# Initialize S3 client
s3 = boto3.client('s3', endpoint_url=R2_ENDPOINT, aws_access_key_id=R2_ACCESS_KEY_ID, aws_secret_access_key=R2_SECRET_ACCESS_KEY, config=Config(signature_version='s3v4'), region_name='auto')


@app.route('/')
def Home():
    return "Flask app running, and its deployed from github"


@app.route('/products/<filter>')
def products(filter):
    products = []

    with Session(engine) as session:
        if filter == 'women':
            stmt = select(Product).where(Product.isForWomen)
            results = session.scalars(stmt)
            for i in results:
                products.append({
                    'id': i.id,
                    'name': i.name,
                    'price': i.price,
                    'sizesOnStock': i.sizesOnStock.split(', ')
                })

        elif filter == 'men':
            stmt = select(Product).where(Product.isForMen)
            results = session.scalars(stmt)
            for i in results:
                products.append({
                    'id': i.id,
                    'name': i.name,
                    'price': i.price,
                    'sizesOnStock': i.sizesOnStock.split(', ')
                })

        elif filter.split(',')[0].isnumeric():
            for i in filter.split(','):
                stmt = select(Product).where(Product.id == int(i))
                product = session.scalar(stmt)
                if product:
                    products.append({
                        'id': product.id,
                        'name': product.name,
                        'price': product.price,
                        'sizesOnStock': product.sizesOnStock.split(', ')
                    })

        else:
            stmt = select(Product).where(Product.name == filter)
            product = session.scalar(stmt)
            if product:
                return jsonify({
                    'id': product.id,
                    'name': product.name,
                    'price': product.price,
                    'sizesOnStock': product.sizesOnStock.split(', ')
                })
            else:
                response = make_response("product(s) is not exist")
                response.status_code = 406
                return response

    return jsonify(products)


@app.route('/images/<path:filename>')
def showImage(filename):
    try:
        s3_object = s3.get_object(Bucket=R2_BUCKET, Key=filename)
        body = s3_object['Body'].read()
        print(f"Serving {filename}: {s3_object['ContentType']}, {len(body)} bytes")
        response = Response(body, content_type=s3_object['ContentType'])
        return response
    except Exception as e:
        print(jsonify({'error': str(e)}))
        return jsonify({'error': 'An exception occured'}), 500


@app.route('/sign-user', methods=['POST'])
def signUser():
    data = json.loads(request.data)

    with Session(engine) as session:
        # Check for duplicate email
        stmt_email = select(User).where(User.email == data['email'])
        existing_email = session.scalar(stmt_email)
        if existing_email:
            return jsonify({'msg': 'email already taken', 'success': False, 'cause': 'email'})

        # Check for duplicate username
        stmt_username = select(User).where(User.username == data['username'])
        existing_username = session.scalar(stmt_username)
        if existing_username:
            return jsonify({'msg': 'username already taken', 'success': False, 'cause': 'username'})

        print(1)
        # Create and add the new user
        user = User(
            email=data['email'],
            username=data['username'],
            password_hash=hashFunction(data['password'])
        )
        print(2)
        session.add(user)
        print(3)
        session.commit()
        print(4)
    return jsonify({'msg': 'user successfully signed', 'success': True})


@app.route('/log-user', methods=['POST'])
def logUser():
    data = json.loads(request.data)

    # Use 2.0-style DB session in helper function
    with Session(engine) as session:
        if not isUserValid(session, data['email_username'], data['password']):
            return jsonify({'msg': 'Username or password is wrong.', 'success': False})

        sessionId = createSession(session, data['email_username'])

    responseData = jsonify({'msg': 'User successfully logged in.', 'success': True})
    response = make_response(responseData)
    response.set_cookie('sessionId', sessionId)

    return response


@app.route('/get-user-data', methods=['POST'])
def get_user_data():
    sessionId = json.loads(request.data)['sessionId']

    with Session(engine) as session:
        # Get the session object by sessionId
        stmt_session = select(Sessions).where(Sessions.sessionId == sessionId)
        session_obj = session.scalar(stmt_session)

        if not session_obj:
            return jsonify({'msg': 'Invalid session ID', 'success': False}), 401

        # Get the user by ID
        stmt_user = select(User).where(User.id == session_obj.userId)
        user = session.scalar(stmt_user)

        if not user:
            return jsonify({'msg': 'User not found', 'success': False}), 404

        userInfo = {
            'username': user.username,
            'email': user.email,
            'address': user.address
        }

        return jsonify({'msg': 'User successfully logged in', 'user_data': userInfo, 'success': True})


@app.route('/update-user', methods=['PUT'])
def update_user():
    data = json.loads(request.data)
    session_id = data['sessionId']

    with Session(engine) as session:
        # Check if session exists
        stmt_session = select(Sessions).where(Sessions.sessionId == session_id)
        session_obj = session.scalar(stmt_session)

        if session_obj is None:
            response = make_response(jsonify({'msg': 'unauthorized', 'success': False}))
            response.status_code = 401
            return response

        # Get user by ID
        stmt_user = select(User).where(User.id == session_obj.userId)
        user = session.scalar(stmt_user)

        if user is None:
            response = make_response(jsonify({'msg': 'user not found', 'success': False}))
            response.status_code = 404
            return response

        # Update user fields
        user.email = data['email']
        user.username = data['username']
        user.address = data['address']
        session.commit()

        return jsonify({'msg': 'successfully changed', 'success': True})


@app.route('/update-bag', methods=['POST', 'DELETE'])
def update_bag():
    data = json.loads(request.data)
    session_id = data['sessionId']

    with Session(engine) as session:
        # Get session object
        stmt_session = select(Sessions).where(Sessions.sessionId == session_id)
        session_obj = session.scalar(stmt_session)

        if session_obj is None:
            return jsonify({'msg': 'unauthorized', 'success': False}), 401

        user_id = session_obj.userId

        # DELETE request logic
        if request.method == 'DELETE':
            product_id = data['productId']
            size = data['size']

            stmt_product = select(ProductsInBag).where(
                (ProductsInBag.productId == product_id) &
                (ProductsInBag.userId == user_id) &
                (ProductsInBag.size == size)
            )
            product = session.scalar(stmt_product)

            if product:
                session.delete(product)
                session.commit()
                return jsonify({'msg': 'product successfully removed from bag', 'success': True})
            else:
                return jsonify({'msg': 'product not found in bag', 'success': False}), 404

        # POST request logic (add to bag)
        product_name = data['productName']
        product_size = data['size']

        stmt_product = select(Product).where(Product.name == product_name)
        product = session.scalar(stmt_product)

        if product is None:
            return jsonify({'msg': 'product not found', 'success': False}), 404

        new_item = ProductsInBag(productId=product.id, userId=user_id, size=product_size)
        session.add(new_item)
        session.commit()

        return jsonify({'msg': 'product successfully added to the bag', 'success': True})


@app.route('/products-in-bag', methods=['POST'])
def products_in_bag():
    data = json.loads(request.data)
    session_id = data['sessionId']

    with Session(engine) as session:
        # Get session object
        stmt_session = select(Sessions).where(Sessions.sessionId == session_id)
        session_obj = session.scalar(stmt_session)

        if session_obj is None:
            return jsonify({'msg': 'unauthorized', 'success': False}), 401

        user_id = session_obj.userId

        # Get all products in bag for user
        stmt_products = select(ProductsInBag).where(ProductsInBag.userId == user_id)
        products = session.scalars(stmt_products).all()

        product_data = [{'id': p.productId, 'size': p.size} for p in products]

        return jsonify({'product_data': product_data})


if __name__ == "__main__":
    app.run(debug=True)
