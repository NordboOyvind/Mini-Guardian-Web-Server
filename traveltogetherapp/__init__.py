# -*- coding: utf-8 -*-
import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from .models import db, User
from . import models  # Sørger for at modellene lastes

# Initialiser login-manager
login_manager = LoginManager()
login_manager.login_view = "auth.login"

@login_manager.user_loader
def load_user(user_id):
    """Last inn bruker fra databasen ved login."""
    return User.query.get(int(user_id))


def create_app():
    """Oppretter og konfigurerer Flask-applikasjonen."""
    # Pek Flask til riktig templates- og static-mappe
    base_dir = os.path.dirname(__file__)
    template_dir = os.path.join(base_dir, "..", "templates")
    static_dir = os.path.join(base_dir, "..", "static")

    app = Flask(
        __name__,
        template_folder=template_dir,
        static_folder=static_dir,
    )

    # Les konfigurasjon fra config.py
    app.config.from_object("config.Config")

    # Koble opp database og login-manager
    db.init_app(app)
    login_manager.init_app(app)

    # Registrer blueprint-moduler
    from .auth import auth_bp
    from .proposals import proposals_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(proposals_bp)

    # Standard forside
    @app.route("/")
    def index():
        return render_template("index.html")

    return app
