import datetime
import enum
import os

from flask import Flask
from flask_admin import Admin
from flask_login import login_required
from flask_security import UserMixin, RoleMixin, SQLAlchemyUserDatastore, Security
from flask_security.utils import hash_password
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint
from sqlalchemy.sql import func

app = Flask(__name__)

app.config['FLASK_ADMIN_SWATCH'] = 'superhero'
app.config['SECURITY_TRACKABLE'] = True

# Create dummy secrey key so we can use sessions
app.config['SECRET_KEY'] = 'iamthesecretkeypuffbadabum'

# Create database
app.config['DATABASE_FILE'] = 'liga_db.sqlite'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + app.config['DATABASE_FILE']
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SECURITY_PASSWORD_SALT'] = 'theissaltysalt'
app.config['SECURITY_TRACKABLE'] = 'salty'

# db = SQLAlchemy(app, session_options={'autocommit': True})
db = SQLAlchemy(app)


# Create models
class Source(db.Model):
    __tablename__ = 'source'
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    sid = db.Column(db.String(length=256), nullable=False, unique=True)
    name = db.Column(db.String(length=256), nullable=False, unique=True)
    url = db.Column(db.String(length=2083))  # lowest max url length - Internet Explorer
    documents = db.relationship('Document', backref='source', lazy='dynamic')


role_user = db.Table(
    'role_user',
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


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    email = db.Column(db.String(length=254), nullable=False, unique=True)  # rfc=3696
    password = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean)
    confirmed_at = db.Column(db.DateTime)
    name = db.Column(db.String(length=256), unique=True)
    documents = db.relationship('Document', backref='user', lazy='dynamic')
    roles = db.relationship('Role', backref='user', secondary=role_user, lazy='dynamic')

    # SECURITY_TRACKABLE requirements
    last_login_at = db.Column(db.DateTime, default=None)
    current_login_at = db.Column(db.DateTime, default=None)
    last_login_ip = db.Column(db.String(length=45), default=None)
    current_login_ip = db.Column(db.String(length=45), default=None)
    login_count = db.Column(db.Integer, default=None)


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


# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)


# Flask views
@app.route('/')
@login_required
def index():
    return '<a href="/admin/">Click me to get to Admin!</a>'


# Create admin
admin = Admin(app, name='Liga documents', template_mode='bootstrap3')


def build_sample_db():
    db.create_all()
    admin_role = user_datastore.create_role(name='admin', description='Superuser')
    db.session.add(admin_role)
    db.session.commit()
    with app.app_context():
        password_hash = hash_password('1234')
    admin_user = user_datastore.create_user(
        name='madzohan', password=password_hash,
        email='madzohan@gmail.com', confirmed_at=datetime.datetime.now(), active=True,
        roles=['admin'])

    db.session.add(admin_user)
    db.session.commit()


if __name__ == '__main__':
    app_dir = os.path.realpath(os.path.dirname(__file__))
    database_path = os.path.join(app_dir, app.config['DATABASE_FILE'])
    if not os.path.exists(database_path):
        build_sample_db()
    app.run(debug=True)
