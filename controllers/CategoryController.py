from flask import jsonify, request
from models.CategoryModel import Category
from config import db
from flask_jwt_extended import jwt_required

# Get all categories
@jwt_required()
def get_categories():
    categories = Category.query.all()
    return jsonify([category.to_dict() for category in categories])

# Get a single category by id
@jwt_required()
def get_category(id):
    category = Category.query.get(id)
    if not category:
        return jsonify({'error': 'Category not found'}), 404
    return jsonify(category.to_dict())

# Add a new category (POST)
@jwt_required()
def add_category():
    new_category_data = request.get_json()
    new_category = Category(name=new_category_data['name'])
    db.session.add(new_category)
    db.session.commit()
    return jsonify({'message': 'Category added successfully!', 'category': new_category.to_dict()}), 201

# Update a category (PUT)
@jwt_required()
def update_category(id):
    category = Category.query.get(id)
    if not category:
        return jsonify({'error': 'Category not found'}), 404
    updated_data = request.get_json()
    category.name = updated_data.get('name', category.name)
    db.session.commit()
    return jsonify({'message': 'Category updated successfully!', 'category': category.to_dict()})

# Delete a category (DELETE)
@jwt_required()
def delete_category(id):
    category = Category.query.get(id)
    if not category:
        return jsonify({'error': 'Category not found'}), 404
    db.session.delete(category)
    db.session.commit()
    return jsonify({'message': 'Category deleted successfully!'})
