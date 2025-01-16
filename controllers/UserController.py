from flask import jsonify, request
from models.UserModel import User
from models.LevelModel import Level
from config import db
from flask_jwt_extended import create_access_token, jwt_required
from datetime import timedelta
import bcrypt

# Fungsi untuk melakukan hash password
def hash_password(password):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')  # Simpan string, bukan byte

# Fungsi untuk memverifikasi password
def check_password_hash(hashed_password, user_password):
    return bcrypt.checkpw(user_password.encode('utf-8'), hashed_password.encode('utf-8'))

def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({'message': 'Invalid username or password'}), 401

    access_token = create_access_token(identity=user.username, expires_delta=timedelta(hours=1))
    return jsonify({'access_token': access_token})

# Get all users
@jwt_required()
def get_users():
    users = User.query.all()
    users_with_level =[]
    for user in users:
        #get level
        level = Level.query.get(user.level_id)
        #add details
        users_with_level.append({
            'id': user.id,
            'username': user.username,
            'fullname': user.fullname,
            'password' : user.password,
            'status': user.status,
            'level_name': level.level_name if level else "No Level"
        })
        
    response ={
        'status':'success',
        'data':{
            'users':users_with_level
        },
        'message':'Users retrived successfully!'
    }
    return jsonify(response),200

# Get a single user by id
@jwt_required()
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error' : 'user not found'}),404
    
    #get level
    level = Level.query.get(user.level_id)
    user_data = {
        'id': user.id,
        'username': user.username,
        'fullname': user.fullname,
        'password' : user.password,
        'status': user.status,
        'level_name': level.level_name if level else "No Level"
    }
    
    response ={
        'status':'success',
        'data':{
            'user':user_data
        },
        'message':'User retrieved successfuly!'
    }
    return jsonify(response),200

# Add a new user
@jwt_required()
def add_user():
    new_user_data = request.get_json()
    hashed_pw = hash_password(new_user_data['password'])  # Hash password
    new_user = User(
        username=new_user_data['username'],
        password=hashed_pw,  # Simpan password yang sudah di-hash
        fullname=new_user_data['fullname'],
        status=new_user_data['status'],
        level_id = new_user_data['level_id']
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User added successfully!', 'user': new_user.to_dict()}), 201

# Update a user (full update)
@jwt_required()
def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    updated_data = request.get_json()
    user.username = updated_data.get('username', user.username)
    user.password = updated_data.get('password', user.password)
    user.fullname = updated_data.get('fullname', user.fullname)
    user.status = updated_data.get('status', user.status)
    user.level_id = updated_data.get('level_id',user.level_id)

    db.session.commit()
    return jsonify({'message': 'User updated successfully!', 'user': user.to_dict()}), 200

# Delete a user
@jwt_required()
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully!'})

# Get all levels
def get_levels():
    levels = Level.query.all()
    level_list = [{'id': level.id_level, 'name': level.level_name} for level in levels]
    return jsonify({'status': 'success', 'data': level_list}), 200
