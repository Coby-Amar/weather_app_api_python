from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from api.modules import db
from api.models import User

users_api = Blueprint('users', __name__)


@users_api.get('')
@jwt_required()
def user():
    try:
        user_id = get_jwt_identity()
        user = User.query.filter_by(id=user_id).first()
        return jsonify({
            "id": user.id,
            "name": user.name,
            "username": user.username,
        })
    except:
        return '', 404


@users_api.delete('')
@jwt_required()
def delete_user():
    try:
        user_id = get_jwt_identity()
        row = User.query.delete(id == user_id)
        if row > 0:
            db.session.commit()
            return '', 204
        else:
            return '', 404
    except:
        return '', 404
