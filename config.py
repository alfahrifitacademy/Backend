from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_cors import CORS

#init db connect
app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)

app.config['JWT_SECRET_KEY'] = 'p~uTBD3-;m27(!jhz?v^,r'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://pwl:pwl123@localhost/db_flask_api'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

app.app_context().push()