class Config:
    SECRET_KEY = 'ade856f07576deb1f86bb2b12fb627d3619986f98116cc835205bd2db7a9'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BABEL_DEFAULT_LOCALE = 'ru'


class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:MySQL.root.146@localhost:3306/journal_2'
    DEBUG = True


class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:MySQL.root.146@localhost:3306/journal_2'
    DEBUG = False


config = {
    "default":DevConfig,
    "dev": DevConfig,
    "prod": ProdConfig
}