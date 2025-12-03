import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "defaultsecret")
    
    # Database configuration for UC3M lab infrastructure
    # Format: mysql+pymysql://26_webapp_XX:PASSWORD@mysql.lab.it.uc3m.es/26_webapp_XXa
    # Replace XX with your assigned number and set DB_PASS environment variable
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{os.getenv('DB_USER', '26_webapp_16')}:{os.getenv('DB_PASS', '')}"
        f"@{os.getenv('DB_HOST', 'mysql.lab.it.uc3m.es')}/{os.getenv('DB_NAME', '26_webapp_16a')}"
    )
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False

