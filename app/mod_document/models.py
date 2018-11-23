from sqlalchemy import UniqueConstraint, func

from app import db


class Document(db.Model):
    __tablename__ = 'document'
    __table_args__ = (UniqueConstraint("title", "text"),)
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    title = db.Column(db.String, nullable=False, index=True)
    text = db.Column(db.String, nullable=False, index=True)
    url = db.Column(db.String)
    created = db.Column(db.DateTime, nullable=False, index=True)  # user defined one
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, onupdate=func.now(), index=True)
    number_of_changes = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)
    source_id = db.Column(db.Integer, db.ForeignKey('source.id'), nullable=False, index=True)
