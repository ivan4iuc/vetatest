from config import db
from sqlalchemy.sql import func

class users(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    email = db.Column(db.String(255))
    password = db.Column(db.String(255))

    created_at = db.Column(db.DateTime, server_default=func.NOW()) 
    updated_at = db.Column(db.DateTime, server_default = func.NOW())

class cards(db.Model):
    __tablename__ = "teams"
    id = db.Column(db.Integer, primary_key=True)
    holiday = db.Column(db.String(3))

    created_at = db.Column(db.DateTime, server_default=func.NOW()) 
    updated_at = db.Column(db.DateTime, server_default = func.NOW())

class contacts(db.Model):
    __tablename__ = "contacts"
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(255))
    address = db.Column(db.String(255))
    city = db.Column(db.String(255))
    zip_code = db.Column(db.Integer)
    country = db.Column(db.String(255))

class history(db.Model):
    __tablename__ = "messages"
    id = db.Column(db.Integer, primary_key = True)

    #### One-to-Many Relationship w/ Users ####
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="cascade"), nullable=False)
    assoc_users = db.relationship('users', foreign_keys=[user_id], backref="assoc_history")
    ###########################################

    #### One-to-Many Relationship w/ Cards ####
    card_id = db.Column(db.Integer, db.ForeignKey('cards.id', ondelete="cascade"), nullable=False)
    assoc_cards = db.relationship('cards', foreign_keys=[card_id], backref="assoc_history")
    ###########################################

    #### One-to-Many Relationship w/ Contacts ####
    contact_id = db.Column(db.Integer, db.ForeignKey('contacts.id', ondelete="cascade"), nullable=False)
    assoc_contacts = db.relationship('contacts', foreign_keys=[contact_id], backref="assoc_history")
    ###########################################

    message = db.Column(db.Text)
    
    created_at = db.Column(db.DateTime, server_default = func.NOW())
    updated_at = db.Column(db.DateTime, server_default = func.NOW())