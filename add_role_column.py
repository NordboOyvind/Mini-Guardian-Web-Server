from traveltogetherapp import create_app
from traveltogetherapp.models import db
from sqlalchemy import text

app = create_app()

with app.app_context():
    try:
        db.session.execute(text("ALTER TABLE user ADD COLUMN role VARCHAR(20) DEFAULT 'user'"))
        db.session.commit()
        print('Added column role to user table.')
    except Exception as e:
        print('ALTER may have failed or column exists:', e)
    try:
        db.session.execute(text("UPDATE user SET role='user' WHERE role IS NULL"))
        db.session.commit()
        print('Ensured existing rows have role set.')
    except Exception as e:
        print('Update failed:', e)
