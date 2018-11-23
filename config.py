import os


# Statement for enabling the development environment
DEBUG = True
SQLALCHEMY_ECHO = True

# Disable Signalling Support http://flask-sqlalchemy.pocoo.org/dev/signals/
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Define the application directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Define the database - we are working with
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'liga_db.sqlite')
DATABASE_CONNECT_OPTIONS = {}

# Application threads. A common general assumption is
# using 2 per available processor cores - to handle
# incoming requests using one and performing background
# operations using the other.
THREADS_PER_PAGE = 2

# Enable protection agains *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED = True

# Use a secure, unique and absolutely secret key for
# signing the data.
CSRF_SESSION_KEY = 'iAmCrsfTheSecretKeyPuffBuduBoom'

# Secret key for signing cookies
SECRET_KEY = 'iAmCookieTheSecretKeyPuffBuduBoom'

# >-------------------------------------------> Flask-Security configs >----------------------------------------------->
SECURITY_URL_PREFIX = '/admin'

# Enable user tracking
SECURITY_TRACKABLE = True

SECURITY_LOGIN_URL = '/login/'
SECURITY_LOGOUT_URL = '/logout/'
SECURITY_REGISTER_URL = '/register/'

SECURITY_POST_LOGIN_VIEW = '/admin/'
SECURITY_POST_LOGOUT_VIEW = '/admin/'
SECURITY_POST_REGISTER_VIEW = '/admin/'

# Flask-Security features
SECURITY_REGISTERABLE = False
SECURITY_SEND_REGISTER_EMAIL = False

# Required cryptography settings for password derivation
SECURITY_PASSWORD_HASH = 'pbkdf2_sha512'
SECURITY_PASSWORD_SALT = 'iAmPaawordSaltTheSecretKeyPuffBuduBoom'
# <-------------------------------------------< Flask-Security configs <-----------------------------------------------<

# Admin app skin theme
FLASK_ADMIN_SWATCH = 'cerulean'
