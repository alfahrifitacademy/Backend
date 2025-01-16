from flask import jsonify, request
from models.LevelModel import Level
from config import db
from flask_jwt_extended import jwt_required

# Get all levels
@jwt_required()
def get_levels():
    levels = Level.query.all()
    return jsonify([level.to_dict() for level in levels]), 200

# Get a single level by id
@jwt_required()
def get_level(id):
    level = Level.query.get(id)
    if not level:
        return jsonify({'error': 'Level not found'}), 404
    return jsonify(level.to_dict()), 200

# Add a new level (POST)
@jwt_required()
def add_level():
    new_level_data = request.get_json()
    new_level = Level(name=new_level_data['name'])
    db.session.add(new_level)
    db.session.commit()
    return jsonify({'message': 'Level added successfully!', 'level': new_level.to_dict()}), 201

# Update a level (PUT)
@jwt_required()
def update_level(id):
    level = Level.query.get(id)
    if not level:
        return jsonify({'error': 'Level not found'}), 404
    updated_data = request.get_json()
    level.name = updated_data.get('name', level.name)
    db.session.commit()
    return jsonify({'message': 'Level updated successfully!', 'level': level.to_dict()}), 200

# Delete a level (DELETE)
@jwt_required()
def delete_level(id):
    level = Level.query.get(id)
    if not level:
        return jsonify({'error': 'Level not found'}), 404
    db.session.delete(level)
    db.session.commit()
    return jsonify({'message': 'Level deleted successfully!'}), 200

# Get all levels
def get_levels():
    levels = Level.query.all()
    level_list = [{'id': level.id_level, 'name': level.level_name} for level in levels]
    return jsonify({'status': 'success', 'data': level_list}), 200
