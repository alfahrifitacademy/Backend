from flask import Blueprint
from controllers.UserController import login, get_users, get_user , update_user, delete_user, add_user

user_bp = Blueprint('User_bp', __name__)

#Route for Login user
user_bp.route('/api/login',methods=['POST'])(login)

#get all user
user_bp.route('/api/users',methods=['GET'])(get_users)

#get by id
user_bp.route('/api/users/<int:user_id>',methods=['GET'])(get_user)

#add new user
user_bp.route('/api/users',methods=['POST'])(add_user)

#update user
user_bp.route('/api/users/<int:user_id>',methods=['PUT'])(update_user)

#delete user
user_bp.route('/api/users/<int:user_id>',methods=['DELETE'])(delete_user)
