import os
basedir = os.path.abspath(os.path.dirname(__file__))
 
class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = 'postgresql://vmkulevxsk:7008LW3UED8L43EF$@vcdiratemyrigdb.postgres.database.azure.com:5432/ratemyrig'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
