import os

class Config:
    SECRET_KEY = "sett-en-sterk-nokkel-her"
    basedir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get("DATABASE_URL")
        or f"sqlite:///{os.path.join(basedir, 'instance', 'MiniGuardian.db')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False


