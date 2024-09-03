from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
from flask_jwt_extended import create_access_token, set_access_cookies, unset_access_cookies, jwt_required

import validations
from api.modules import db, bcrypt
from api.models import User

auth_api = Blueprint('auth', __name__)


@auth_api.post('/signup')
def signin():
    data = request.json
    if data.get("username") is None or data.get("password") is None:
        return jsonify('Invalid data'), 400
    username, password = data.get("username"), data.pop("password")
    if validations.validate_username(username) or validations.validate_password(password):
        return jsonify('Invalid data'), 422
    hashed_password = bcrypt.generate_password_hash(password).decode()
    try:
        user = User(
            username=username, password_hash=hashed_password, name=username.split('@')[0])
        db.session.add(user)
        db.session.commit()
        res = jsonify({
            "id": user.id,
            "name": user.name,
            "username": user.username,
        })
        access_token = create_access_token(identity=user.id)
        set_access_cookies(res, access_token)
        return res, 201
    except:
        return jsonify('cant create user'), 422


@auth_api.post('/login')
def login():
    data = request.json
    username, password = data.pop("username"), data.pop("password")
    if username is None or password is None:
        return jsonify('Invalid data'), 400
    if validations.validate_username(username) or validations.validate_password(password):
        return jsonify('Invalid data'), 422
    user = User.query.filter_by(username=username).first()
    if user and bcrypt.check_password_hash(user.password_hash, password):
        res = jsonify({
            "id": user.id,
            "name": user.name,
            "username": user.username,
        })
        access_token = create_access_token(identity=user.id)
        set_access_cookies(res, access_token)
        return res
    else:
        return jsonify({'message': 'Failed'}), 401


@auth_api.post('/logout')
@jwt_required()
def logout():
    res = jsonify()
    unset_access_cookies(res)
    return res
