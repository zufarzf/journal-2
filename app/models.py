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
    __searchable__=['text', 'author_']
    id = db.Column(db.Integer, primary_key=True)
    file = db.Column(db.String(100))
    author_ = db.Column(db.String(255))
    text = db.Column(db.String(150), nullable=False)
    views = db.Column(db.Integer, nullable=False)
    author_email = db.Column(db.String(100))

    editional = db.Column(db.Boolean, default=False)
    special = db.Column(db.Boolean, default=False)

    vol_cat = db.Column(db.Integer, db.ForeignKey('volumecat.id'))
    author = db.relationship('VolumeCkeditor', backref='volumeinfo', lazy='dynamic')

    
    def __repr__(self):
        return f"<{self.text}>"


class VolumeCkeditor(db.Model):
    __tablename__='volumeckeditor'
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(255))
    abstract = db.Column(db.Text)
    cite = db.Column(db.String(255))

    vol_info = db.Column(db.Integer, db.ForeignKey('volumeinfo.id'))

    def __repr__(self):
        return f"{self.author}"

    
class Email(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    text = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)


class Personal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(250))
    psw = db.Column(db.Text)
    is_admin = db.Column(db.Boolean, default=True)