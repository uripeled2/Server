# API setup
from mange import app
from models import User, Activity
from flask import jsonify, request
from werkzeug.security import check_password_hash, generate_password_hash
import datetime
import uuid
from my_token import token_required
from mange import db
import jwt
import json
from my_helper import create_act, update_act


@app.route('/activity/<activity_ids>', methods=['GET', 'PUT', 'DELETE'])
@token_required
def activity_controller(user, activity_ids):
    response_object = {'status': None}

    if not user.is_login:
        response_object['message'] = 'User is no longer login'
        response_object['status'] = 403
        return jsonify(response_object)

    # GET: get activity details
    elif request.method == "GET":
        act = Activity.query.filter_by(id=activity_ids).first()
        if act is not None:
            response_object['Activity'] = act.serialize
            response_object['status'] = 200
        else:
            response_object['message'] = 'Invalid activity id'
            response_object['status'] = 502

    # PUT: update activity details
    elif request.method == "PUT":
        data = request.get_json()
        description = data.get("description")
        spot = data.get("spot")
        policy_type = data.get("policy_type")
        penalty_price = data.get("penalty_price")
        penalty_time = data.get("penalty_time")
        days = data.get("days")
        time_step = data.get('time_step')
        weekly = data.get('weekly')

        act = update_act(description, spot, policy_type, penalty_price, penalty_time, days, time_step, weekly,
                         activity_ids)
        if act:
            try:
                db.session.add(act)
                db.session.commit()
                response_object['message'] = 'activity updated!'
                response_object['status'] = 200
                response_object['activity'] = act.serialize
            except:
                response_object['message'] = 'db error'
                response_object['status'] = 500
        else:
            response_object['message'] = 'Wrong data'
            response_object['status'] = 400

    # DELETE: delete activity
    elif request.method == 'DELETE':
        act = Activity.query.filter_by(id=activity_ids).first()
        if act is None:
            response_object['message'] = "Invalid activity id"
            response_object['status'] = 502
        else:
            try:
                db.session.delete(act)
                db.session.commit()
                response_object['message'] = 'activity deleted!'
                response_object['status'] = 200
            except:
                response_object['message'] = 'db error'
                response_object['status'] = 500

    # Not Implemented request
    else:
        response_object['message'] = 'Cant the preform the request'
        response_object['status'] = 405

    return jsonify(response_object)


@app.route('/activity', methods=['GET', 'POST'])
@token_required
def user_activities_controller(user):
    response_object = {'status': None}

    if not user.is_login:
        response_object['message'] = 'User is no longer login'
        response_object['status'] = 403
        return jsonify(response_object)

    # GET: get all user's the activities
    elif request.method == "GET":
        try:
            acts = Activity.query.filter_by(user_id=user.id).all()
            response_object['activities'] = [act.serialize for act in acts]
            response_object['status'] = 200
        except:
            response_object['message'] = 'db error'
            response_object['status'] = 500

    # POST: create new activity
    elif request.method == "POST":
        try:
            data = request.get_json()
            description = data["description"]
            spot = data["spot"]
            policy_type = data["policy_type"]
            penalty_price = data["penalty_price"]
            penalty_time = data["penalty_time"]
            days = data["days"]
            time_step = data['time_step']
            weekly = data['weekly']
        except:
            response_object['message'] = 'Wrong data'
            response_object['status'] = 400
            return jsonify(response_object)

        act = create_act(description, spot, policy_type, penalty_price, penalty_time, days, time_step, weekly, user.id)
        if not act:
            response_object['message'] = 'Wrong data'
            response_object['status'] = 400
            return jsonify(response_object)

        try:
            db.session.add(act)
            db.session.commit()
            response_object['message'] = 'activity added!'
            response_object['activity'] = act.serialize
            response_object['status'] = 201
        except:
            response_object['message'] = 'db error'
            response_object['status'] = 500

    # Not Implemented request
    else:
        response_object['message'] = 'Cant the preform the request'
        response_object['status'] = 405

    return jsonify(response_object)


@app.route('/logout', methods=['GET', 'DELETE'])
@token_required
def logout(user):

    response_object = {'status': None}

    if not user.is_login:
        response_object['message'] = 'User is no longer login'
        response_object['status'] = 403
        return jsonify(response_object)

    # GET: logout user
    elif request.method == "GET":
        user.is_login = False
        db.session.add(user)
        db.session.commit()
        response_object['message'] = 'User logout!'
        response_object['status'] = 200

    # DELETE: delete user and all his activities
    elif request.method == "DELETE":
        activities = Activity.query.filter_by(user_id=user.id).all()
        for act in activities:
            db.session.delete(act)
            db.session.commit()
        db.session.delete(user)
        db.session.commit()
        response_object['message'] = 'Delete user!'
        response_object['status'] = 200

    # Not Implemented request
    else:
        response_object['message'] = 'Cant the preform the request'
        response_object['status'] = 405

    return jsonify(response_object)


@app.route('/user', methods=['POST', 'PUT'])
def user_controller():
    response_object = {'status': None}

    # POST: create new user
    if request.method == "POST":
        data = request.get_json()
        try:
            name = data["username"]
            if not isinstance(name, str):
                raise ValueError
        except:
            response_object['message'] = 'Missing username'
            response_object['status'] = 400
            return jsonify(response_object)
        try:
            password = data['password']
            if not isinstance(password, str):
                raise ValueError
            hashed = generate_password_hash(password, method='sha256')
        except:
            response_object['message'] = 'Missing password'
            response_object['status'] = 400
            return jsonify(response_object)

        if User.query.filter_by(username=name).first() is not None:
            response_object['message'] = "Invalid username"
            response_object['status'] = 502
            return jsonify(response_object)

        user = User(username=name, password_hash=hashed)
        try:
            db.session.add(user)
            db.session.commit()
        except:
            response_object['message'] = 'db error'
            response_object['status'] = 500
            return jsonify(response_object)

        token = jwt.encode({'public_id': user.public_id, 'exp': datetime.datetime.utcnow() +
                            datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])
        response_object['token'] = token.decode('UTF-8')
        response_object['message'] = 'user added!'
        response_object['status'] = 201

    # PUT: login user
    elif request.method == "PUT":
        data = request.get_json()
        try:
            name = data["username"]
            if not isinstance(name, str):
                raise ValueError
        except:
            response_object['message'] = 'Missing username'
            response_object['status'] = 400
            return jsonify(response_object)
        try:
            password = data["password"]
            if not isinstance(password, str):
                raise ValueError
        except:
            response_object['message'] = 'Missing password'
            response_object['status'] = 400
            return jsonify(response_object)

        user = User.query.filter_by(username=name).first()

        if not user:
            response_object['message'] = 'Invalid username'
            response_object['status'] = 401

        elif check_password_hash(user.password_hash, password):
            user.is_login = True
            try:
                db.session.add(user)
                db.session.commit()
            except:
                response_object['message'] = 'db error'
                response_object['status'] = 500
                return jsonify(response_object)

            token = jwt.encode({'public_id': user.public_id, 'exp': datetime.datetime.utcnow() +
                                datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])
            response_object['token'] = token.decode('UTF-8')
            response_object['status'] = 200

        else:
            response_object['message'] = 'Invalid password'
            response_object['status'] = 401

    # Not Implemented request
    else:
        response_object['message'] = 'Cant the preform the request'
        response_object['status'] = 405

    return jsonify(response_object)


@app.route('/')
def hello_world():
    return 'Hello from Uri'
