"""models.py."""

from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash


class User(db.Model):
    """This class represents the user table."""

    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(100), unique=True, null=False)
    password = db.Column(db.String(128))

    def __init__(self, password):
        """Initialize with setting a hashed password."""
        self.set_password(password)

    def set_password(self, password):
        """Hash the password."""
        self.pw_hash = generate_password_hash(password)


class Item(db.Model):
    """This class represents the items table."""

    __tablename__ = 'items'
    item_id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(100))
    description = db.Column(db.String(200))
    is_completed = db.Column(db.Boolean, default=False)
    created_date = db.Column(db.DateTime, default=datetime.now)
    modified_date = db.Column(
        db.DateTime, default=datetime.now,
        onupdate=datetime.now)
    bucketlist_id = db.Column(db.integer,
                              db.ForeginKey(bucketlists.bucketlists_id))

    def __init__(self, item_name):
        """Initialize with item name."""
        self.item_name = item_name


class Bucketlist(db.Model):
    """This class represents the bucketlist table."""

    __tablename__ = 'bucketlists'

    bucketlist_id = db.Column(db.Integer, primary_key=True)
    bucketlist_title = db.Column(db.String(100))
    date_created = db.Column(db.DateTime, default=datetime.now)
    date_modified = db.Column(
        db.DateTime, default=datetime.now,
        onupdate=datetime.now)
    creator_id = db.Column(db.integer, db.ForeginKey(users.user_id))
    created_by = db.relationship('users',
                                 backref=db.backref('items', lazy='dynamic'))
    items = db.relationship('items',
                            backref=db.backref('items', lazy='dynamic'))

    def __repr__(self):
        """Return printable representation of the object."""
        return "Bucketlist: %d" % self.bucketlist_title

    def save(self):
        """Save a bucketlist."""
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """Delete a bucketlist."""
        db.session.delete(self)
        db.session.commit()