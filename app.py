# -*- coding: utf-8 -*-

# ----------------------
# web framework
# ----------------------
from flask import Flask, request, render_template, jsonify

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
from ml.xor.loader import predict



# ----------------------
# app configs
# ----------------------

puppy_engine = create_engine('sqlite:///puppies.db', encoding='utf8')
puppy.Base.metadata.bind = puppy_engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

app = Flask(__name__)





# ----------------------
# end points: home
# ----------------------
@app.route("/")
def home():
    return render_template("home.html", name="home")


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
        data_jsonify = puppy.getAllPuppies(session)
    
    elif request.method == 'POST':
        name = request.form.get('name', '')
        description = request.form.get('description', '')
        data_jsonify = puppy.makeANewPuppy(name, description, session)

    return data_jsonify


@app.route("/api/puppies/<int:id>", methods = ['GET', 'PUT', 'DELETE'])
def puppiesFunctionId(id):

    if request.method == 'GET':
        return puppy.getPuppy(id, session)

    if request.method == 'PUT':
        name = request.form.get('name', '')
        description = request.form.get('description', '')
        return puppy.updatePuppy(id, name, description, session)

    elif request.method == 'DELETE':
        return puppy.deletePuppy(id, session) 


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







