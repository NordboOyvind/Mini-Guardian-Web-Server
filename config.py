import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "defaultsecret")
    SQLALCHEMY_DATABASE_URI = (
        f"mysql://{os.getenv('DB_USER', '26_webapp_16')}:{os.getenv('DB_PASS', '')}"
        f"@{os.getenv('DB_HOST', 'mysql')}/{os.getenv('DB_NAME', '26_webapp_16a')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

