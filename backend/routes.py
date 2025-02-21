from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################


@app.route("/picture", methods=["GET"])
def get_pictures():
    return jsonify(data), 200

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>")
def get_picture_by(id):
    try:
        if data and len(data) > 0:
            for pic in data:
                if 'id' in pic.keys() and id == pic['id']:
                    return pic, 200
            return "Not found", 404
    
    except NameError:
        return jsonify({'error_message': 'Something went wrong'}), 500


######################################################################
# CREATE A PICTURE
######################################################################


@app.route("/picture", methods=["POST"])
def create_picture():
    new_pic = request.get_json()
    if new_pic and data and len(data) > 0:
        for pic in data:
            if 'id' in pic.keys() and new_pic['id'] == pic['id']:
                return {"Message": f"picture with id {pic['id']} already present"}, 302
        data.append(new_pic)
        return jsonify(new_pic), 201

######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    new_pic = request.get_json()
    if new_pic and data and len(data) > 0:
        for pic in data:
            if 'id' in pic.keys() and id == pic['id']:
                data.remove(pic)
                data.append(new_pic)
                return jsonify(data), 200
        return jsonify({"message": "picture not found"}), 404

######################################################################
# DELETE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    if data and len(data) > 0:
        for pic in data:
            if 'id' in pic.keys() and id == pic['id']:
                data.remove(pic)
                return {}, 204
            return {"message": "picture not found"}, 404