from config import db

# Model Level
class Level(db.Model):
    id_level = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)

    # Relationship dengan User (one-to-many)
    users = db.relationship('User', backref='level', lazy=True)

    def to_dict(self):
        return {
            'id_level': self.id_level,
            'name': self.name
        }