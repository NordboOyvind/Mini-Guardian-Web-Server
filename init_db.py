from traveltogetherapp import create_app
from traveltogetherapp.models import db

app = create_app()

with app.app_context():
    # Note: `db.create_all()` will create tables that do not exist yet.
    # It will not alter existing tables to add new columns. If you already
    # have a database and want to add the `alias` column to the `user` table,
    # either:
    #  - Use Flask-Migrate / Alembic to generate a migration and apply it, or
    #  - Run a manual ALTER TABLE statement, for example:
    #      ALTER TABLE user ADD COLUMN alias VARCHAR(50);
    # For fresh development installs, `create_all()` will create the new column.
    db.create_all()
    print("Database tables created successfully!")
