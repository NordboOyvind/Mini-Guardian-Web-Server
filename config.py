import os

class Config:
    SECRET_KEY = "sett-en-sterk-nokkel-her"
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or "sqlite:///instance/MiniGuardian.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


