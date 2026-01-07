import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "defaultsecret")
    
    # SQLite database configuration
    base_dir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(base_dir, 'app.db')}"
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TEMPLATES_AUTO_RELOAD = True


