# jwt setup
import jwt
from flask import jsonify, request
from functools import wraps
from mange import app
from models import User


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'Authorization' in request.headers:
            token = request.headers['Authorization']
            token = token[7:]

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            user = User.query.filter_by(public_id=data['public_id']).first()
            if user is None:
                raise ValueError
            return f(user, *args, **kwargs)
        except:
            return jsonify({'message': 'Token is invalid!'}), 401

    return decorated


