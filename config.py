"""configurations for app"""


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

    DEBUG = False

class HerokuConfig(BaseConfig):
    """
    Heroku Configurations
    """
    SQLALCHEMY_DATABASE_URI = "postgres://msrcptnhjmkcjg:9e39ca49dbdc3b5dd1dde34378239c7cc0449c19d7579e96d13e16c2cc593820@ec2-23-23-226-190.compute-1.amazonaws.com:5432/dbrf2b14uph6cl"

app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'heroku': HerokuConfig
}

if __name__ == '__main__':
    app_config['development']
