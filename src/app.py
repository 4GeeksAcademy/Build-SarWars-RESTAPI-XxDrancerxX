"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Planet, Character, Favorite_character, Favorite_Planets
import logging
from sqlalchemy.orm import joinedload

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace(
        "postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object


@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints


@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/user/<int:user_id>', methods=['GET'])
def get_one_user(user_id):
    user = User.query.get(user_id)
    return jsonify(user.serialize()), 200


       

@app.route('/user', methods=['GET'])
def get_user():
    users = User.query.all()
    users_list = [userData.serialize() for userData in users]
    return jsonify(users_list), 200

# [GET] /users/favorites
@app.route('/user/<int:user_id>/all_favorites', methods=['GET'])
def get_favorites_user(user_id):
    try:
        user = User.query.get(user_id)
        if user is None:
            logger.warning(f"User with ID {user_id} not found")
            return jsonify({"error": "User not found"}), 404
        favorite_characters = user.favorite_characters
        favorite_planets = user.favorite_planets
        
        favorite_characters_list = [fav_char.serialize() for fav_char in favorite_characters]
        favorite_planets_list = [fav_planet.serialize() for fav_planet in favorite_planets]
        
        response = {
            "user_id": user_id,
            "favorite_characters": favorite_characters_list,
            "favorite_planets": favorite_planets_list
        }
        logger.info(f"Successfully fetched favorites for user ID {user_id}")
        return jsonify(response), 200
    except Exception as e:
        logger.error(f"Error fetching favorites for user ID {user_id}: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route('/planet/<int:planet_id>', methods=['GET'])
def get_one_planet(planet_id):
    planet = Planet.query.get(planet_id)
    return jsonify(planet.serialize()), 200
           

@app.route('/planet', methods=['GET'])
def get_planet():
    planets = Planet.query.all()
    planets_list = [planet.serialize() for planet in planets]
    return jsonify(planets_list), 200


@app.route('/character', methods=['GET'])
def get_charc():
    characters = Character.query.all()
    users_list = [character.serialize() for character in characters]
    return jsonify(users_list), 200

@app.route('/character/<int:character_id>', methods=['GET'])
def get_one_character(character_id):
    get_character = Character.query.get(character_id)
    return jsonify(get_character.serialize()), 200

@app.route('/fav_char', methods=['GET'])
def get_fav_char():
    fav_chars = Favorite_character.query.all()
    fav_char_list = [fav_char.serialize() for fav_char in fav_chars]
    return jsonify(fav_char_list), 200

@app.route('/fav_planets', methods=['GET'])
def get_fav_planets():
    fav_planets = Favorite_Planets.query.all()
    fav_planets_list = [fav_planet.serialize() for fav_planet in fav_planets]
    return jsonify(fav_planets_list), 200
    

@app.route('/user', methods=['POST'])
def user_post():
    data = request.get_json()
    new_user = User(

        email=data["email"],
        password=data["password"],
        is_active=data["is_active"]
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.serialize()), 200


@app.route('/character', methods=['POST'])
def person_post():
    data = request.get_json()
    new_person = Character(

        name=data["name"],
        age=data["age"],
        height=data["height"],
        weight=data["weight"]

    )
    db.session.add(new_person)
    db.session.commit()
    return jsonify(new_person.serialize()), 200

@app.route('/planet', methods=['POST'])
def planet_post():
    data = request.get_json()
    new_planet = Planet(

        name=data["name"],
        age=data["age"],
        color=data["color"],
        population=data["population"],
        density=data["density"]
    )
    db.session.add(new_planet)
    db.session.commit()
    return jsonify(new_planet.serialize()), 200


@app.route('/fav_char', methods=['POST'])
def fav_char_post():
    data = request.get_json()
    new_char = Favorite_character(
       
        user_id= data["user_id"],
        character_id= data["character_id"],
        
    )
    db.session.add(new_char)
    db.session.commit()
    return jsonify(new_char.serialize()), 200


@app.route('/fav_planets', methods=['POST'])
def fav_planets_post():
    data = request.get_json()
    new_fav_planets = Favorite_Planets(
       
        user_id= data["user_id"],
        planet_id= data["planet_id"],        
       
    )
    db.session.add(new_fav_planets)
    db.session.commit()
    return jsonify(new_fav_planets.serialize()), 200





@app.route('/fav_planets/<int:fav_planet_id>', methods=['DELETE'])
def delete_planet(fav_planet_id):
    planet = Favorite_Planets.query.filter_by(id=fav_planet_id).first()
    if planet is None:
        return jsonify({"error": "Favorite planet not found"}), 404        
    response = {
        "message": "favorite planet was deleted",
        "planet": planet.serialize()
    }
    db.session.delete(planet)
    db.session.commit()
    return jsonify(response), 200

@app.route('/fav_char/<int:fav_char_id>', methods=['DELETE'])
def delete_fav_char(fav_char_id):
    char = Favorite_character.query.filter_by(id=fav_char_id).first()
    if char is None:
        return jsonify({"error": "Favorite char not found"}), 404        
    response = {
        "message": "favorite char was deleted",
        "char": char.serialize()
    }
    db.session.delete(char)
    db.session.commit()
    return jsonify(response), 200





# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)



