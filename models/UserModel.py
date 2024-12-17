from config import db

# Model User
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)  # Hash password akan disimpan di sini
    fullname = db.Column(db.String(150), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    # Foreign key ke tabel level
    level_id = db.Column(db.Integer, db.ForeignKey('level.id_level'), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'fullname': self.fullname,
            'password' : self.password,
            'status': self.status,
            'level_id': self.level_id
        }