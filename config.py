"""configurations for app"""
import os

class BaseConfig(object):
    """
    Common configurations
    """
    TESTING = False
    DEBUG = False
    # Put any configurations here that are common across all environments


class TestingConfig(BaseConfig):
    """Configurations for Testing, with a separate test database."""
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:magic@localhost/book_test_db"
    TESTING = True
    DEBUG = True


class DevelopmentConfig(BaseConfig):
    """
    Development configurations
    """
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:magic@localhost/book_a_meal_db"
    DEBUG = True


class ProductionConfig(BaseConfig):
    """
    Production configurations
    """
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    DEBUG = False


app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}

if __name__ == '__main__':
    app_config['development']
