class Config(object):
    DEBUG = False
    TESTING = False

    # Lines used to set application secret key to verify Json Web Tokens
    # And location where tokens will be kept.
    JWT_SECRET_KEY = 'aPdSgVkYp3s6v9y$B&E)H@MbQeThWmZq4t7w!z%C*F-JaNdRfUjXn2r5u8x/A?D('
    JWT_TOKEN_LOCATION = 'cookies'
    JWT_SESSION_COOKIE = True

    # Token will expire in 15 minutes
    JWT_ACCESS_TOKEN_EXPIRES = 900

    # Necessary lines for using SQLAlchemy Flask Database.
    SQLALCHEMY_DATABASE_URI = 'sqlite:///flaskdatabase.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProductionConfig(Config):
    JWT_COOKIE_SECURE = True
    JWT_COOKIE_CSRF_PROTECT = True

class DevelopmentConfig(Config):
    DEBUG = True
    JWT_COOKIE_CSRF_PROTECT = False
    JWT_COOKIE_SECURE = False

class TestingConfig(Config):
    TESTING = True

 # The following are different environment variables.
 # 'DEBUG': True,
 # 'ENV': 'development',
 # 'EXPLAIN_TEMPLATE_LOADING': False,
 # 'JSONIFY_MIMETYPE': 'application/json',
 # 'JSONIFY_PRETTYPRINT_REGULAR': False,
 # 'JSON_AS_ASCII': True,
 # 'JSON_SORT_KEYS': True,
 # 'MAX_CONTENT_LENGTH': None,
 # 'MAX_COOKIE_SIZE': 4093,
 # 'PERMANENT_SESSION_LIFETIME': datetime.timedelta(days=31),
 # 'PREFERRED_URL_SCHEME': 'http',
 # 'PRESERVE_CONTEXT_ON_EXCEPTION': None,
 # 'PROPAGATE_EXCEPTIONS': None,
 # 'SECRET_KEY': None,
 # 'SEND_FILE_MAX_AGE_DEFAULT': datetime.timedelta(seconds=43200),
 # 'SERVER_NAME': None,
 # 'SESSION_COOKIE_DOMAIN': None,
 # 'SESSION_COOKIE_HTTPONLY': True,
 # 'SESSION_COOKIE_NAME': 'session',
 # 'SESSION_COOKIE_PATH': None,
 # 'SESSION_COOKIE_SAMESITE': None,
 # 'SESSION_COOKIE_SECURE': False,
 # 'SESSION_REFRESH_EACH_REQUEST': True,
 # 'TEMPLATES_AUTO_RELOAD': None,
 # 'TESTING': False,
 # 'TRAP_BAD_REQUEST_ERRORS': None,
 # 'TRAP_HTTP_EXCEPTIONS': False,
 # 'USE_X_SENDFILE': False