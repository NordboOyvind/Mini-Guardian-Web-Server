from traveltogetherapp import create_app
from traveltogetherapp.models import db
from sqlalchemy import text

app = create_app()

with app.app_context():
    try:
        db.session.execute(text("ALTER TABLE time_entry ADD COLUMN duration_seconds INTEGER"))
        db.session.commit()
        print('Added column duration_seconds to time_entry table.')
    except Exception as e:
        print('ALTER may have failed or column exists:', e)
    try:
        db.session.execute(text("UPDATE time_entry SET duration_seconds = 60 * duration_minutes WHERE duration_seconds IS NULL AND EXISTS(SELECT 1 FROM sqlite_master WHERE type='table' AND name='time_entry')"))
        db.session.commit()
        print('Populated duration_seconds from duration_minutes where possible.')
    except Exception as e:
        print('Update failed (migration step):', e)
