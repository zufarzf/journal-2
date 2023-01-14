from datetime import datetime

from . import db

class VolumeCat(db.Model):
    __tablename__='volumecat'
    __searchable__ = ['name']
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), default = 'Vol')
    published_date = db.Column(db.DateTime, default=datetime.utcnow())
    doi = db.Column(db.String(150), unique=True)

    current = db.Column(db.Boolean, default=False)
    just = db.Column(db.Boolean, default=False)
    special = db.Column(db.Boolean, default=False)

    volume = db.relationship('VolumeInfo', backref='volumecat', lazy='dynamic')


    def __repr__(self):
        return f"<{self.name}>"


class VolumeInfo(db.Model):
    __tablename__='volumeinfo'
    __searchable__=['text', 'author']
    id = db.Column(db.Integer, primary_key=True)
    file = db.Column(db.String(100))
    text = db.Column(db.String(150), nullable=False)
    author = db.Column(db.String(150), nullable=False)
    abstract = db.Column(db.Text, nullable=False)
    cite = db.Column(db.String(255))
    views = db.Column(db.Integer, nullable=False)

    editional = db.Column(db.Boolean, default=False)
    special = db.Column(db.Boolean, default=False)

    vol_cat = db.Column(db.Integer, db.ForeignKey('volumecat.id'))

    
    def __repr__(self):
        return f"<{self.author}>"

    
class Email(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    text = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)


class Personal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(50))
    psw = db.Column(db.String(50))
    is_admin = db.Column(db.Boolean, default=True)