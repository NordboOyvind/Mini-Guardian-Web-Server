import os

class Config:
    SECRET_KEY = "sett-en-sterk-nokkel-her"
    SQLALCHEMY_DATABASE_URI = os.environ["DATABASE_URL"]  # Må settes i Render
    SQLALCHEMY_TRACK_MODIFICATIONS = False


