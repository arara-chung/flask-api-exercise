# -*- coding: utf-8 -*-

# ----------------------
# web framework
# ----------------------
from flask import Flask, request, render_template, jsonify, json


# ----------------------
# DB
# ----------------------
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


# ----------------------
# Models
# ----------------------
from models import Base, Puppy
from ml.xor.loader import predict



# ----------------------
# app configs
# ----------------------

engine = create_engine('sqlite:///puppies.db', encoding='utf8')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

app = Flask(__name__)





# ----------------------
# end points: puppies
# ----------------------

@app.route("/")
def home():
    return render_template("home.html", name="home")


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
        data_jsonify = getAllPuppies()
    
    elif request.method == 'POST':
        name = request.form.get('name', '')
        description = request.form.get('description', '')
        data_jsonify = makeANewPuppy(name, description)

    return data_jsonify


@app.route("/api/puppies/<int:id>", methods = ['GET', 'PUT', 'DELETE'])
def puppiesFunctionId(id):

    if request.method == 'GET':
        return getPuppy(id)

    if request.method == 'PUT':
        name = request.form.get('name', '')
        description = request.form.get('description', '')
        return updatePuppy(id, name, description)

    elif request.method == 'DELETE':
        return deletePuppy(id) 


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
# end points: machine learning
# ----------------------

@app.route('/ml')
def ml_landing_page():
    return render_template("ml.html", message="Welcome to tensorflow api experiment")

@app.route('/api/xor/predict')
def _ml_xor_get_prediction():

    input1 = request.args.get('input1', 0, type=float)
    input2 = request.args.get('input2', 0, type=float)
    result = predict(input1, input2)

    return jsonify(result = str(result))






# ----------------------
# Puppy methods: get, make, put, delete 
# ----------------------

def getAllPuppies():
    puppies = session.query(Puppy).all()
    return jsonify(puppies=[i.serialize for i in puppies])
  
def makeANewPuppy(name, description):
    puppy = Puppy(name=name, description=description)
    session.add(puppy)
    session.commit()
    return jsonify(puppy=puppy.serialize) 

def getPuppy(id):
    puppy = session.query(Puppy).filter_by(id=id).one()
    return jsonify(puppy=puppy.serialize)
  
def updatePuppy(id, name, description):
    puppy = session.query(Puppy).filter_by(id=id).one()

    if name:
        puppy.name = name
    if description:
        puppy.description = description

    session.add(puppy)
    session.commit()

    return jsonify(message="Updating a Puppy with id %s" % id) 

def deletePuppy(id):
    puppy = session.query(Puppy).filter_by(id=id).one()

    session.delete(puppy)
    session.commit()

    return jsonify(message="Removing Puppy with id %s" % id)



# ----------------------
# launch options
# ----------------------

if __name__ == "__main__":
    app.run(debug=True)







