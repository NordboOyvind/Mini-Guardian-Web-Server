from traveltogetherapp import create_app
from traveltogetherapp.models import db, User, TimeEntry
from datetime import date, datetime, timedelta
import csv
import os

app = create_app()

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
os.makedirs(DATA_DIR, exist_ok=True)

with app.app_context():
    today = date.today()
    # Last calendar week Monday-Sunday
    last_monday = today - timedelta(days=today.weekday() + 7)
    week_dates = [last_monday + timedelta(days=i) for i in range(7)]
    week_label = f"{last_monday.isocalendar()[0]}-W{last_monday.isocalendar()[1]}"

    users = db.session.execute(db.select(User)).scalars().all()

    combined_rows = []

    for user in users:
        per_day = []
        week_total_seconds = 0
        for d in week_dates:
            day_start = datetime(d.year, d.month, d.day)
            day_end = day_start + timedelta(days=1)

            q = db.select(TimeEntry).where(
                TimeEntry.user_id == user.id,
                TimeEntry.start_time < day_end,
                (TimeEntry.end_time == None) | (TimeEntry.end_time >= day_start),
            )
            entries = db.session.execute(q).scalars().all()
            seconds = 0
            for e in entries:
                s = e.start_time
                en = e.end_time or datetime.utcnow()
                if s < day_start:
                    s = day_start
                if en > day_end:
                    en = day_end
                delta = en - s
                secs = int(delta.total_seconds())
                seconds += secs

            hours = seconds // 3600
            rem_minutes = (seconds % 3600) // 60
            rem_seconds = seconds % 60
            per_day.append((d.isoformat(), d.strftime('%A'), hours, rem_minutes, rem_seconds, seconds))
            week_total_seconds += seconds

        # Write per-user CSV
        filename = os.path.join(DATA_DIR, f"weekly_report_{user.id}_{week_label}.csv")
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['date', 'weekday', 'hours', 'minutes', 'seconds', 'total_seconds'])
            for row in per_day:
                writer.writerow(row)
            writer.writerow([])
            writer.writerow(['TOTAL', '', week_total_seconds // 3600, (week_total_seconds % 3600)//60, week_total_seconds % 60, week_total_seconds])

        combined_rows.append((user, per_day, week_total_seconds))

    # Optionally write combined file
    combined_file = os.path.join(DATA_DIR, f"weekly_report_all_{week_label}.csv")
    with open(combined_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['user_id', 'user_email', 'date', 'weekday', 'hours', 'minutes', 'seconds', 'total_seconds'])
        for user, per_day, week_total_seconds in combined_rows:
            for row in per_day:
                writer.writerow([user.id, user.email] + list(row))
            writer.writerow([user.id, user.email, 'TOTAL', '', week_total_seconds // 3600, (week_total_seconds % 3600)//60, week_total_seconds % 60, week_total_seconds])

    print('Weekly reports written to', DATA_DIR)
