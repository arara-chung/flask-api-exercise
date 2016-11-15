from flask import Flask, request, render_template


# MARK: app config

app = Flask(__name__)

# END MARK: app config




# MARK: define end points

@app.route("/")
def home():
    return render_template("home.html", name="home")

@app.route("/puppies", methods = ['GET', 'POST'])
def puppiesFunction():

  message=None

  if request.method == 'GET':
    message = getAllPuppies()
  elif request.method == 'POST':
    message = makeANewPuppy()

  return render_template("puppies.html", message=message)


@app.route("/puppies/<int:id>", methods = ['GET', 'PUT', 'DELETE'])
def puppiesFunctionId(id):
    if request.method == 'GET':
        return getPuppy(id)
    if request.method == 'PUT':
        return updatePuppy(id)
    elif request.method == 'DELETE':
        return deletePuppy(id) 

# END MARK: define end points






# MARK: get, make, put, delete method

def getAllPuppies():
    return "Getting All the puppies!"
  
def makeANewPuppy():
    return "Creating A New Puppy!"

def getPuppy(id):
  return "Getting Puppy with id %s" % id
  
def updatePuppy(id):
    return "Updating a Puppy with id %s" % id

def deletePuppy(id):
    return "Removing Puppy with id %s" % id

# END MARK: get, make, put, delete method







# MARK: launch options

if __name__ == "__main__":
    app.run(debug=True)

# END MARK: launch options