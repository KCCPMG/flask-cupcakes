"""Flask app for Cupcakes"""

from flask import Flask, jsonify, render_template, redirect, request
from models import db, connect_db, Cupcake
from flask_debugtoolbar import DebugToolbarExtension
# from forms import 

app = Flask(__name__)

app.config["SECRET_KEY"] = "terces"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes_test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

# TESTING
app.config['WTF_CSRF_ENABLED'] = False

debug = DebugToolbarExtension(app)

connect_db(app)
# db.drop_all()
# db.create_all()



@app.route("/", methods=["GET"])
def get_home():

  return render_template("index.html")


@app.route("/api/cupcakes", methods=["GET", "POST"])
def get_cupcakes():
  """
  GET:
  Get data about all cupcakes.

  Respond with JSON like: {cupcakes: [{id, flavor, size, rating, image}, ...]}.

  The values should come from each cupcake instance.

  POST:
  Create a cupcake with flavor, size, rating and image data from the body of the request.

  Respond with JSON like: {cupcake: {id, flavor, size, rating, image}}.
  """
  if request.method == "GET":
    cupcakes = Cupcake.query.all()

    cupcake_list = [serialize_cupcake(cupcake) for cupcake in cupcakes]

    return jsonify(cupcakes=cupcake_list)
    
  else: # POST
    cupcake = Cupcake(flavor=request.json["flavor"],
    size=request.json["size"],
    rating=request.json["rating"],
    image=request.json["image"])

    db.session.add(cupcake)
    db.session.commit()

    return (jsonify(cupcake=serialize_cupcake(cupcake)), 201)


@app.route("/api/cupcakes/<int:cupcake_id>", methods=["GET"])
def get_cupake(cupcake_id):
  """
  Get data about a single cupcake.

  Respond with JSON like: {cupcake: {id, flavor, size, rating, image}}.

  This should raise a 404 if the cupcake cannot be found.
  """
  cupcake = Cupcake.query.get_or_404(cupcake_id)

  return jsonify(cupcake=serialize_cupcake(cupcake))


@app.route("/api/cupcakes/<int:cupcake_id>", methods=["PATCH"])
def patch_cupcake(cupcake_id):
  """
  Update a cupcake with the id passed in the URL and flavor, size, rating and image data from the body of the request. You can always assume that the entire cupcake object will be passed to the backend.

  This should raise a 404 if the cupcake cannot be found.

  Respond with JSON of the newly-updated cupcake, like this: {cupcake: {id, flavor, size, rating, image}}.
  """
  cupcake = Cupcake.query.get_or_404(cupcake_id)

  cupcake.flavor=request.json["flavor"]
  cupcake.size=request.json["size"]
  cupcake.rating=request.json["rating"]
  cupcake.image=request.json["image"]

  db.session.commit()

  return jsonify(cupcake=serialize_cupcake(cupcake))




@app.route("/api/cupcakes/<int:cupcake_id>", methods=["DELETE"])
def delete_cupcake(cupcake_id):
  """
  DELETE 
  This should raise a 404 if the cupcake cannot be found.

  Delete cupcake with the id passed in the URL. Respond with JSON like {message: "Deleted"}.

  Test these routes in Insomnia.
  """
  cupcake = Cupcake.query.get_or_404(cupcake_id)

  db.session.delete(cupcake)
  db.session.commit()

  # status code 200
  return jsonify(message="Deleted")



def serialize_cupcake(cupcake):
  return {
    "id": cupcake.id,
    "flavor": cupcake.flavor, 
    "size": cupcake.size, 
    "rating": cupcake.rating, 
    "image": cupcake.image
  }