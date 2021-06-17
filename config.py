import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY=os.getenv("SECRET_KEY") or "faiosdfjasdf"
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL").replace('postgres', 'postgresql') if os.getenv("DATABASE_URL") else 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False