from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators 
    @validates('phone_number')
    def validate_phone_number(self, key, value):
        if not (value.isdigit() and len(value) == 10):
            raise ValueError("Failed simple phone number validation")
        return value

    @validates('name')
    def validate_name(self, key, value):
        if not value:
            raise ValueError("Failed simple name validation")
        author = Author.query.filter_by(name=value).first()
        if author:
            raise ValueError("Failed simple name validation")
        return value
    

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators
    @validates('category')
    def validate_category(self, key, value):
        if value != 'Fiction' and value != 'Non-Fiction':
            raise ValueError("Failed simple category validation")
        return value
     
    @validates('summary')
    def validate_summary(self, key, value):
        if len(value) > 250:
            raise ValueError("Failed simple summary validation")
        return value
     
    @validates('content')
    def validate_content(self, key, value):
        if len(value) < 250:
            raise ValueError("Failed simple content validation")
        return value
    
    @validates('title')
    def validate_title(self, key, value):
        title_content = ["Won't Believe", "Secret", "Top", "Guess"]
        if not any(phrase in value for phrase in title_content):
            raise ValueError("Failed simple title validation")
        if not value:
            raise ValueError("Failed simple title validation")
        return value


    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
