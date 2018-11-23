from app import db


class Source(db.Model):
    __tablename__ = 'source'
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    sid = db.Column(db.String(length=256), nullable=False, unique=True)
    name = db.Column(db.String(length=256), nullable=False, unique=True)
    url = db.Column(db.String(length=2083))  # lowest max url length - Internet Explorer
    documents = db.relationship('Document', backref='source', lazy='dynamic')
