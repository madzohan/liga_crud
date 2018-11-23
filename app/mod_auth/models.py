import enum

from flask_security import RoleMixin, UserMixin
from six import string_types

from app import db


roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))


class RolesEnum(enum.Enum):
    user = 0
    admin = 1


class Role(db.Model, RoleMixin):
    __tablename__ = 'role'
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    name = db.Column(db.Enum(RolesEnum), nullable=False)
    description = db.Column(db.String(255))

    def __repr__(self):
        return '<Role {}>'.format(self.name)


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    email = db.Column(db.String(length=254), nullable=False, unique=True)  # rfc=3696
    password = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean)
    confirmed_at = db.Column(db.DateTime)
    name = db.Column(db.String(length=256), unique=True)
    documents = db.relationship('Document', backref='user', lazy='dynamic')
    roles = db.relationship('Role', backref='user', secondary=roles_users, lazy='dynamic')

    # SECURITY_TRACKABLE requirements
    last_login_at = db.Column(db.DateTime, default=None)
    current_login_at = db.Column(db.DateTime, default=None)
    last_login_ip = db.Column(db.String(length=45), default=None)
    current_login_ip = db.Column(db.String(length=45), default=None)
    login_count = db.Column(db.Integer, default=None)

    def has_role(self, role):
        """Returns `True` if the user identifies with the specified role.

        :param role: A role name or `Role` instance"""
        if isinstance(role, string_types):
            return role in (role.name.name for role in self.roles)
        else:
            return role in self.roles

    def __repr__(self):
        return '<User {}>'.format(self.email)
