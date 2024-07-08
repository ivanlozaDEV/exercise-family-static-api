"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person


app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def handle_get_all_members():

    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    response_body = {
        "hello": "world",
        "family": members
    }


    return jsonify(response_body), 200


@app.route('/members/<int:id>', methods=['GET'])
def handle_get_member(id):

    # this is how you can use the Family datastructure by calling its methods
    member = jackson_family.get_member(id)
    if member:
        return jsonify(member), 200
    else:
        return jsonify({"error": "Member does not exist"}),400

@app.route('/members', methods=['POST'])
def handle_add_member():
    data = request.get_json()
    if not data or not all(key in data for key in ('first_name', 'age', 'lucky_numbers')):
        return jsonify({"error": "Invalid input, something is missing"}), 400
    
    new_member = {
        "first_name": data['first_name'],
        "age": data['age'],
        "lucky_numbers": data['lucky_numbers']
    }
    added_member = jackson_family.add_member(new_member)
    return jsonify(added_member), 201

@app.route('/members/<int:id>', methods=['DELETE'])
def handle_delete_member(id):
    try:
        success = jackson_family.delete_member(id)
        if success:
            return jsonify({"member deleted": True}), 200
        else:
            return jsonify({"error": "Member not found"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
