from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy_serializer import SerializerMixin

from config import db, bcrypt, validates

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    serialize_rules = ("-recipes.user", "-_password_hash",)

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    _password_hash =  db.Column(db.String)
    image_url = db.Column(db.String)
    bio = db.Column(db.String)

    recipes = db.relationship("Recipe", backref="user")


    @validates("username")
    def validate_username(self, key, name):
        # name = [user.name for user in User.query.all()]
        if not name:
            raise ValueError("Username must exist")
        elif name in name:
            raise ValueError("Username must be unique")
        return name


    @hybrid_property
    def password_hash(self):
        return self._password_hash
    
    
    @password_hash.setter
    def password_hash(self, password):
        password_hash = bcrypt.generate_password_hash(password.encode("utf-8"))
        self._password_hash = password_hash.decode("utf-8")


    def authenticate(self, password):
        return bcrypt.check_password_hash(self._password_hash, password.encode("utf-8"))
    
    def __repr__(self):
        return f"User ID: {self.id}, Username: {self.username}, Image URL: {self.image_url}, Bio: {self.bio}"




class Recipe(db.Model, SerializerMixin):
    __tablename__ = 'recipes'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    instructions = db.Column(db.String, nullable=False)
    minutes_to_complete = db.Column(db.Integer)

    user_id = db.Column(db.Integer(), db.ForeignKey("users.id"))



    @validates("title")
    def validate_title(self, key, title):
        if not title:
            raise ValueError("title must be present")
        return title


    @validates("instructions")
    def validate_instructions(self, key, instructions):
        if not instructions:
            raise ValueError("instructions must be present")
        elif len(instructions) <= 50:
            raise ValueError("instructions must be at least 50 charachters long")
        return instructions

    def __repr__(self):
        return f"Recipe ID: {self.id}, Title: {self.tile}, Instructions: {self.instructions}, Completion time: {self.minutes_to_complete}"


