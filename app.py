"""Flask app for Cupcakes"""
from flask import Flask, request, jsonify, render_template

from models import Cupcake, connect_db, db

app = Flask(__name__)
app.app_context().push()

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "oh-so-secret"

connect_db(app)

@app.route('/')
def index_page():
    """Show list of all cupcakes in DB."""

    cupcakes = Cupcake.query.all()
    return render_template('home.html', cupcakes=cupcakes)

# *****************************
# RESTFUL CUPCAKES JSON API
# *****************************

@app.route('/api/cupcakes')
def list_cupcakes():
    all_cupcakes = [cupcake.serialize() for cupcake in Cupcake.query.all()]
    return jsonify(cupcakes=all_cupcakes)

@app.route('/api/cupcakes/<int:id>')
def view_cupcake(id):
    cupcake = Cupcake.query.get_or_404(id)
    return jsonify(cupcake=cupcake.serialize())

@app.route('/api/cupcakes', methods=["POST"])
def create_cupcake():
    new_cupcake = Cupcake(
        flavor=request.json['flavor'], 
        size=request.json['size'], 
        rating=request.json['rating'],
        image=request.json['image'])
    db.session.add(new_cupcake)
    db.session.commit()
    return (jsonify(cupcake = new_cupcake.serialize()), 201)

@app.route('/api/cupcakes/<int:id>', methods=["PATCH"])
def update_cupcake(id):
    cupcake = Cupcake.query.get_or_404(id)
    cupcake.flavor = request.json.get('flavor', cupcake.flavor)
    cupcake.size = request.json.get('size', cupcake.size)
    cupcake.rating = request.json.get('rating', cupcake.rating)
    cupcake.image = request.json.get('image', cupcake.image)
    db.session.commit()
    return (jsonify(cupcake=cupcake.serialize()), 200)

@app.route('/api/cupcakes/<int:id>', methods=["DELETE"])
def delete_cupcake(id):
    cupcake = Cupcake.query.get_or_404(id)
    db.session.delete(cupcake)
    db.session.commit()
    return jsonify(message="DELETED!")