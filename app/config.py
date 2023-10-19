import os

base_dir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig:
    """
    Base application configuration
    """
    DEBUG = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'sdfa876dfa9df7&*^&*%&64sfasdf')
    BCRYPT_HASH_PREFIX = 14
    AUTH_TOKEN_EXPIRY_DAYS = 30
    AUTH_TOKEN_EXPIRY_SECONDS = 3000
    BUCKET_AND_ITEMS_PER_PAGE = 25


class DevelopmentConfig(BaseConfig):
    """
    Development application configuration
    """
    DEBUG = True
    BCRYPT_HASH_PREFIX = 4
    AUTH_TOKEN_EXPIRY_DAYS = 1
    AUTH_TOKEN_EXPIRY_SECONDS = 20
    BUCKET_AND_ITEMS_PER_PAGE = 4
    TOKEN    = '765185530:AAGaBUP8CiLfzPhpfni2NcUfpUnPodm7oAg'
    HOST     = '' # Same FQDN used when generating SSL Cert
    PORT     = 8443


class ProductionConfig(BaseConfig):
    """
    Production application configuration
    """
    DEBUG = False
    BCRYPT_HASH_PREFIX = 13
    AUTH_TOKEN_EXPIRY_DAYS = 30
    AUTH_TOKEN_EXPIRY_SECONDS = 20
    BUCKET_AND_ITEMS_PER_PAGE = 10
