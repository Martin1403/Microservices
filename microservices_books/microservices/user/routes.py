from flask import Blueprint, jsonify, request, make_response
from flask_login import login_user, current_user, logout_user
from models import db, User
from werkzeug.security import generate_password_hash, check_password_hash

user_blueprint = Blueprint("user_api_routes", __name__, url_prefix="/api/user")


@user_blueprint.route("/all", methods=["GET"])
def get_all_users():
    all_users = User.query.all()
    result = [user.serialize() for user in all_users]
    response = {
        "message": "Returning all users",
        "result": result
    }
    return make_response(jsonify(response), 200)


@user_blueprint.route("/create", methods=["POST"])
def create_user():
    try:
        user = User()
        user.username = request.form["username"]
        user.password = generate_password_hash(request.form["password"], method="sha256")
        user.is_admin = True
        db.session.add(user)
        db.session.commit()
        response = {"message": "User Created", "result": user.serialize()}
        return jsonify(response)
    except Exception as e:
        print(str(e))
        response = {"message": "Error i create response"}
        return jsonify(response)


@user_blueprint.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    user = User.query.filter_by(username=username).first()
    if not user:
        response = {'message': 'username does not exists'}
        return make_response(jsonify(response), 401)
    if check_password_hash(user.password, password):
        user.update_api_key()
        db.session.commit()
        login_user(user)
        response = {'message': 'logged in ', 'api_key': user.api_key}
        return make_response(jsonify(response), 200)

    response = {'message': 'Access denied'}
    return make_response(jsonify(response), 401)


@user_blueprint.route("/logout", methods=["POST"])
def logout():
    if current_user.is_authenticated:
        logout_user()
        response = {"message": "logged out"}
        return make_response(jsonify(response), 200)
    response = {"message": "No user logged in"}
    return make_response(jsonify(response), 401)


@user_blueprint.route("/<username>/exists", methods=["GET"])
def user_exists(username):
    user = User.query.filter_by(username=username).first()
    if user:
        return make_response(jsonify({"result": True}), 200)
    return make_response(jsonify({"result": False}), 404)


@user_blueprint.route("/", methods=["GET"])
def get_current_user():
    if current_user.is_authenticated:
        return make_response(jsonify({"result": current_user.serialize()}), 200)
    else:
        return make_response(jsonify({"message": "User not logged in"}), 401)
