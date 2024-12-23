from config import app, db
from routes.Book_bp import book_bp
from routes.Category_bp import category_bp
from routes.User_bp import user_bp
from routes.Level_bp import level_bp
from flask import request, jsonify
from controllers.UserController import check_password_hash
from models.UserModel import User
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity

#Inisialisasi JWTManager
jwt = JWTManager(app)

@app.route("/api/protected", methods=["GET"])
@jwt_required()
def protected():
    print("Headers Received:", request.headers)  # Debugging Header
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

@app.before_request
def before_request():
    # Daftar endpoint yang dikecualikan dari autentikasi
    excluded_routes = ['/api/login', '/api/register']
    if request.path in excluded_routes:
        return None  # Lewati autentikasi untuk route ini
    return None

    # # Terapkan autentikasi untuk semua route lainnya
    # auth = request.authorization  # Mendapatkan data auth dari header
    # if not auth or not auth.username or not auth.password:
    #     return jsonify({"message": "Missing or invalid credentials"}), 401

    # # Cek user di database
    # user = User.query.filter_by(username=auth.username).first()
    # if not user or not check_password_hash(user.password, auth.password):
    #     return jsonify({"message": "Invalid username or password"}), 401

    # # Simpan user ke dalam request context untuk digunakan di endpoint
    # request.current_user = user

app.register_blueprint(book_bp)
app.register_blueprint(category_bp)
app.register_blueprint(user_bp)
app.register_blueprint(level_bp)

#db.create_all()
if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
