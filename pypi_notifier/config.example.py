class BaseConfig(object):
    SECRET_KEY = 'insecure'
    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/pypi_notifier.db'
    CACHE_TYPE = 'filesystem'
    CACHE_DIR = '/tmp'


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/pypi_notifier.db'
    GITHUB_CLIENT_ID = ''
    GITHUB_CLIENT_SECRET = ''
    GITHUB_CALLBACK_URL = 'http://localhost:5000/github-callback'


class TestingConfig(BaseConfig):
    TESTING = True
    CSRF_ENABLED = False
    DEBUG_TB_ENABLED = False
    GITHUB_CLIENT_ID = 'a'
    GITHUB_CLIENT_SECRET = 'b'
    GITHUB_CALLBACK_URL = 'http://localhost:5000/github-callback'


class ProductionConfig(BaseConfig):
    SECRET_KEY = ''
    GITHUB_CLIENT_ID = ''
    GITHUB_CLIENT_SECRET = ''
    GITHUB_CALLBACK_URL = 'http://www.pypi-notifier.org/github-callback'
    SENTRY_DSN = None
    POSTMARK_APIKEY = ''
