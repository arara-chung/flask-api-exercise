# -*- coding: utf-8 -*-

# ----------------------
# web framework
# ----------------------
from flask import Flask, request, render_template, jsonify, url_for, abort

# ----------------------
# DB
# ----------------------
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# ----------------------
# Models
# ----------------------
import models.puppy as puppy
from models.puppy import Puppy
import models.user as user
from models.user import User

from ml.xor.loader import predict



# ----------------------
# app and DB configs
# ----------------------

puppy_engine = create_engine('sqlite:///puppies.db', encoding='utf8')
puppy.Base.metadata.bind = puppy_engine
puppy_DBSession = sessionmaker(bind=puppy_engine)
puppy_session = puppy_DBSession()

user_engine = create_engine('sqlite:///puppies.db')
user.Base.metadata.bind = user_engine
user_DBSession = sessionmaker(bind=user_engine)
user_session = user_DBSession()

app = Flask(__name__)



# ----------------------
# end points: home
# ----------------------
@app.route("/")
def home():
    return render_template("home.html", name="home")

# ----------------------
# end points: user
# ----------------------
@app.route("/users", methods = ['GET'])
def user_landing_page():
    return render_template("users.html", 
        name="home",
        message="welcome to my user landing page")

@app.route("/api/users", methods = ['POST'])
def create_user():
    username = request.json.get('username')
    password = request.json.get('password')

    print(username)
    print(password)

    if username is None or password is None:
        abort(400) # missing args
    if user_session.query(User).filter_by(username=username).first() is not None:
        abort(400) # existing user
    user = User(username = username)
    user.hash_password(password)
    user_session.add(user)
    user_session.commit()
    return jsonify(user=user.serialize), 201, {'Location': url_for('get_user', id=user.id, _external = True)}

@app.route('/api/users/<int:id>')
def get_user(id):
    user = session.query(User).filter_by(id=id).one()
    if not user:
        abort(400)
    return jsonify({'username':user.username})



# ----------------------
# end points: puppy
# ----------------------
@app.route("/puppies", methods = ['GET', 'POST'])
def puppies_landing_page():

    message = None

    if request.method == 'GET':
        message = "Getting All the puppies!"
    elif request.method == 'POST':
        message = "Creating A New Puppy!"

    return render_template("puppies.html", message=message)

@app.route("/api/puppies", methods = ['GET', 'POST'])
def puppiesFunction():

    data_jsonify = None

    if request.method == 'GET':
        data_jsonify = puppy.getAllPuppies(puppy_session)
    
    elif request.method == 'POST':
        name = request.form.get('name', '')
        description = request.form.get('description', '')
        data_jsonify = puppy.makeANewPuppy(name, description, puppy_session)

    return data_jsonify


@app.route("/api/puppies/<int:id>", methods = ['GET', 'PUT', 'DELETE'])
def puppiesFunctionId(id):

    if request.method == 'GET':
        return puppy.getPuppy(id, puppy_session)

    if request.method == 'PUT':
        name = request.form.get('name', '')
        description = request.form.get('description', '')
        return puppy.updatePuppy(id, name, description, puppy_session)

    elif request.method == 'DELETE':
        return puppy.deletePuppy(id, puppy_session) 


# ----------------------
# end points: number
# ----------------------
@app.route('/number')
def number_landing_page():
    return render_template("number.html")

@app.route('/_add_numbers')
def add_numbers():
    a = request.args.get('a', 0, type=int)
    b = request.args.get('b', 0, type=int)
    return jsonify(result = a + b)


# ----------------------
# end points: machine learning / tensorflow / xor
# ----------------------
@app.route('/ml')
def ml_landing_page():
    return render_template("ml.html", message="Welcome to tensorflow api experiment")

@app.route('/api/xor/predict')
def _ml_xor_get_prediction():

    input1 = request.args.get('input1', 0, type=float)
    input2 = request.args.get('input2', 0, type=float)
    result = predict(input1, input2)

    return jsonify(result = 'Result = ' + str(result))





# ----------------------
# launch options
# ----------------------

if __name__ == "__main__":
    app.run(debug=True)







