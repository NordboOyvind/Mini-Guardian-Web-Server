import csv
import io
from flask_login import login_user, logout_user, login_required, current_user
# ...resten av koden beholdes...
from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from .models import db, User, TimeEntry
from .forms import RegisterForm, LoginForm, ProfileForm
import re
from datetime import datetime, timedelta

auth_bp = Blueprint("auth", __name__)

# Admin/bruker kan sette RFID for en bruker
@auth_bp.route('/profile/<int:user_id>/set_rfid', methods=['POST'])
@login_required
def set_rfid(user_id):
    user = db.session.get(User, user_id)
    if not user:
        flash('User not found.', 'danger')
        return redirect(url_for('index'))
    if not (getattr(current_user, 'role', None) == 'admin' or current_user.id == user.id):
        flash('Insufficient permissions.', 'danger')
        return redirect(url_for('auth.profile_view', user_id=user_id))
    rfid = request.form.get('rfid', '').strip()
    if rfid:
        # Check if RFID already taken by another user
        existing = db.session.execute(
            db.select(User).where(User.rfid == rfid, User.id != user.id)
        ).scalar_one_or_none()
        if existing:
            flash('RFID card is already registered to another user.', 'danger')
            return redirect(url_for('auth.profile_view', user_id=user_id))
        user.rfid = rfid
    else:
        user.rfid = None
    db.session.commit()
    flash('RFID updated.', 'success')
    return redirect(url_for('auth.profile_view', user_id=user_id))
import csv
import io
from flask_login import login_user, logout_user, login_required, current_user
# ...resten av koden beholdes...
from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from .models import db, User, TimeEntry
from .forms import RegisterForm, LoginForm, ProfileForm
import re
from datetime import datetime, timedelta

auth_bp = Blueprint("auth", __name__)

## Fjernet duplikat/feilplassert set_rfid route. Korrekt definisjon beholdes lenger nede i filen hvis nødvendig.
import csv
import io
from flask_login import login_user, logout_user, login_required, current_user
# ...resten av koden beholdes...
from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from .models import db, User, TimeEntry
from .forms import RegisterForm, LoginForm, ProfileForm
import re
from datetime import datetime, timedelta

auth_bp = Blueprint("auth", __name__)

# Simple email check (bypassing email_validator)
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm(request.form)
    if request.method == "POST" and form.validate():
        email = form.email.data.strip()
        password = form.password.data

        if not EMAIL_RE.match(email):
            flash("Ugyldig e-postadresse.", "danger")
            return render_template("auth_register.html", form=form)

        query = db.select(User).where(User.email == email)
        user = db.session.execute(query).scalar_one_or_none()
        if user:
            flash("Email already registered.", "warning")
            return render_template("auth_register.html", form=form)

        hashed_password = generate_password_hash(password)
        # Determine role from whitelist
        import os
        root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        whitelist_path = os.path.join(root_dir, 'whitelist.txt')
        role = 'user'
        try:
            if os.path.exists(whitelist_path):
                with open(whitelist_path, 'r', encoding='utf-8') as wf:
                    allowed = [l.strip().lower() for l in wf if l.strip()]
                if email.lower() in allowed:
                    role = 'editor'
        except Exception:
            role = 'user'

        user = User(email=email, password=hashed_password, role=role)
        db.session.add(user)
        db.session.commit()
        
        login_user(user)
        flash("Registration successful! Please set your user name and profile.", "success")
        return redirect(url_for("auth.profile_edit"))
    return render_template("auth_register.html", form=form)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm(request.form)
    if request.method == "POST" and form.validate():
        email = form.email.data.strip()
        query = db.select(User).where(User.email == email)
        user = db.session.execute(query).scalar_one_or_none()
        if not user or not check_password_hash(user.password, form.password.data):
            flash("Invalid email or password.", "danger")
            return render_template("auth_login.html", form=form)
        login_user(user)
        return redirect(url_for("main_page"))
    return render_template("auth_login.html", form=form)


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out successfully.", "success")
    return redirect(url_for("index"))


# --- Profilvisning ---
@auth_bp.route("/profile/<int:user_id>")
@login_required
def profile_view(user_id):
    user = db.session.get(User, user_id)
    if not user:
        flash("User not found.", "danger")
        return redirect(url_for("index"))

    # Compute today's total time (UTC) for the profile user
    from datetime import datetime, timedelta
    today = datetime.utcnow().date()
    day_start = datetime(today.year, today.month, today.day)
    day_end = day_start + timedelta(days=1)

    q = db.select(TimeEntry).where(
        TimeEntry.user_id == user.id,
        TimeEntry.start_time < day_end,
        (TimeEntry.end_time == None) | (TimeEntry.end_time >= day_start),
    ).order_by(TimeEntry.start_time.desc())
    entries = db.session.execute(q).scalars().all()

    total_minutes = 0
    running = False
    total_seconds = 0
    for e in entries:
        s = e.start_time
        en = e.end_time or datetime.utcnow()
        # Clip to today
        if s < day_start:
            s = day_start
        if en > day_end:
            en = day_end
        delta = en - s
        secs = int(delta.total_seconds())
        total_seconds += secs
        if e.end_time is None:
            running = True

    import pytz
    oslo = pytz.timezone('Europe/Oslo')
    formatted_entries = []
    for e in entries:
        s_raw = e.start_time
        en_raw = e.end_time
        s = s_raw.isoformat() if s_raw else ''
        en = en_raw.isoformat() if en_raw else ''
        # server-side human readable (Europe/Oslo)
        s_fmt = s_raw.astimezone(oslo).strftime('%Y-%m-%d %H:%M') if s_raw else ''
        en_fmt = en_raw.astimezone(oslo).strftime('%Y-%m-%d %H:%M') if en_raw else 'running'
        secs = e.duration_seconds if getattr(e, 'duration_seconds', None) is not None else int(((en_raw or datetime.utcnow()) - s_raw).total_seconds())
        mins = secs // 60
        formatted_entries.append({
            'start_iso': s,
            'end_iso': en,
            'start_fmt': s_fmt,
            'end_fmt': en_fmt,
            'seconds': secs,
            'minutes': mins,
        })

    return render_template("profile_view.html", user=user, today_seconds=total_seconds, timer_running=running, entries=formatted_entries)



@auth_bp.route("/profile/edit", methods=["GET", "POST"])
@login_required
def profile_edit():
    # Profile editing logic
    form = ProfileForm(request.form if request.method == "POST" else None)
    if request.method == "POST" and form.validate():
        current_user.alias = form.alias.data.strip()
        current_user.description = form.description.data
        
        # Handle RFID card registration
        rfid = request.form.get("rfid", "").strip()
        if rfid:
            # Check if RFID already taken by another user
            existing = db.session.execute(
                db.select(User).where(User.rfid == rfid, User.id != current_user.id)
            ).scalar_one_or_none()
            if existing:
                flash("RFID card is already registered to another user.", "danger")
                return render_template("profile_edit.html", form=form)
        current_user.rfid = rfid if rfid else None
        
        # Handle password change
        new_password = request.form.get("new_password", "").strip()
        confirm_password = request.form.get("confirm_password", "").strip()
        
        if new_password or confirm_password:
            if not new_password:
                flash("Please enter a new password.", "danger")
                return render_template("profile_edit.html", form=form)
            if new_password != confirm_password:
                flash("Passwords do not match.", "danger")
                return render_template("profile_edit.html", form=form)
            if len(new_password) < 6:
                flash("Password must be at least 6 characters long.", "danger")
                return render_template("profile_edit.html", form=form)
            
            # Update password
            current_user.password_hash = generate_password_hash(new_password)
            flash("Profile and password updated.", "success")
        else:
            flash("Profile updated.", "success")
        
        db.session.commit()
        return redirect(url_for("index"))
    
    # Prefill form on GET
    if request.method == "GET":
        form.description.data = current_user.description
        form.alias.data = current_user.alias
    return render_template("profile_edit.html", form=form)


@auth_bp.route('/time/start', methods=['POST', 'GET'])
@login_required
def start_time():
    # Prevent multiple running entries
    running_q = db.select(TimeEntry).where(TimeEntry.user_id == current_user.id, TimeEntry.end_time == None)
    running = db.session.execute(running_q).scalar_one_or_none()
    if running:
        flash('Timer already running.', 'warning')
        return redirect(url_for('auth.profile_view', user_id=current_user.id))

    entry = TimeEntry(user_id=current_user.id)
    db.session.add(entry)
    db.session.commit()
    flash('Timer started.', 'success')
    return redirect(url_for('auth.profile_view', user_id=current_user.id))


@auth_bp.route('/time/stop', methods=['POST', 'GET'])
@login_required
def stop_time():
    running_q = db.select(TimeEntry).where(TimeEntry.user_id == current_user.id, TimeEntry.end_time == None)
    running = db.session.execute(running_q).scalar_one_or_none()
    if not running:
        flash('No running timer found.', 'warning')
        return redirect(url_for('auth.profile_view', user_id=current_user.id))

    from datetime import datetime
    running.end_time = datetime.utcnow()
    delta = running.end_time - running.start_time
    running.duration_seconds = int(delta.total_seconds())
    db.session.commit()
    flash('Timer stopped.', 'success')
    return redirect(url_for('auth.profile_view', user_id=current_user.id))


@auth_bp.route('/profile/<int:user_id>/set_role', methods=['POST'])
@login_required
def set_role(user_id):
    # Role setting logic
    # Only editors/admins may change roles
    if not current_user.is_authenticated or not getattr(current_user, 'role', None) or current_user.role not in ('editor', 'admin'):
        flash('Insufficient permissions.', 'danger')
        return redirect(url_for('auth.profile_view', user_id=user_id))

    target = db.session.get(User, user_id)
    if not target:
        flash('User not found.', 'danger')
        return redirect(url_for('index'))

    new_role = request.form.get('role', 'user')
    if new_role not in ('user', 'editor'):
        flash('Invalid role.', 'danger')
        return redirect(url_for('auth.profile_view', user_id=user_id))

    target.role = new_role
    db.session.commit()
    flash(f"Updated role for {target.email} to {new_role}.", 'success')
    return redirect(url_for('auth.profile_view', user_id=user_id))

@auth_bp.route('/timelogs')
@login_required
def timelogs():
    # Only editors may view the full overview
    if not current_user.is_editor():
        flash('Insufficient permissions.', 'danger')
        return redirect(url_for('index'))

    from .models import DailyAdjustment
    today = datetime.utcnow().date()
    # Finn siste søndag (eller i dag hvis søndag)
    weekday_today = today.weekday()
    last_sunday = today - timedelta(days=(weekday_today + 1) % 7)
    week_start = last_sunday + timedelta(days=1)
    week_end = today
    users = db.session.execute(db.select(User).where(User.role == 'editor')).scalars().all()
    rows = []
    for u in users:
        adjustments = {a.date.isoformat(): a for a in db.session.execute(
            db.select(DailyAdjustment).where(
                DailyAdjustment.user_id == u.id,
                DailyAdjustment.date >= week_start,
                DailyAdjustment.date <= week_end
            )
        ).scalars()}
        q = db.select(TimeEntry).where(
            TimeEntry.user_id == u.id,
            TimeEntry.start_time < week_end + timedelta(days=1),
            (TimeEntry.end_time == None) | (TimeEntry.end_time >= week_start),
        )
        entries = db.session.execute(q).scalars().all()
        per_day = []
        week_total = 0
        days_with_time = 0
        for i in range((week_end - week_start).days + 1):
            d = week_start + timedelta(days=i)
            d_iso = d.isoformat()
            day_start = datetime(d.year, d.month, d.day)
            day_end = day_start + timedelta(days=1)
            if d_iso in adjustments:
                minutes = adjustments[d_iso].total_minutes
            else:
                minutes = 0
                for e in entries:
                    s = e.start_time
                    en = e.end_time or datetime.utcnow()
                    if s < day_start:
                        s = day_start
                    if en > day_end:
                        en = day_end
                    delta = en - s
                    if delta.total_seconds() > 0:
                        minutes += int(delta.total_seconds() // 60)
            if minutes > 0:
                days_with_time += 1
            week_total += max(0, minutes)
        week_total = max(0, week_total)
        avg_minutes = int(week_total / days_with_time) if days_with_time > 0 else 0
        avg_hh = avg_minutes // 60
        avg_mm = avg_minutes % 60
        hh = week_total // 60
        mm = week_total % 60
        rows.append({'user': u, 'hm': f"{hh:02d}:{mm:02d}", 'total_minutes': week_total, 'avg': f"{avg_hh:02d}:{avg_mm:02d}"})

    return render_template('timelogs_main.html', rows=rows)

@auth_bp.route('/timelogs/<int:user_id>', methods=['GET', 'POST'])
@login_required
def timelogs_user(user_id):
    if not current_user.is_editor():
        flash('Insufficient permissions.', 'danger')
        return redirect(url_for('index'))

    
    from .models import DailyAdjustment
    today = datetime.utcnow().date()
    user = db.session.get(User, user_id)
    if not user:
        flash('User not found.', 'danger')
        return redirect(url_for('auth.timelogs'))

    # Håndter innsending av justering
    if request.method == 'POST':
        date_str = request.form.get('date')
        try:
            total_minutes = int(request.form.get('total_minutes', 0))
        except Exception:
            flash('Skriv inn et positivt heltall for minutter.', 'danger')
            return redirect(url_for('auth.timelogs_user', user_id=user.id))
        if total_minutes < 0 or total_minutes > 1440:
            flash('Minutter må være mellom 0 og 1440.', 'danger')
            return redirect(url_for('auth.timelogs_user', user_id=user.id))
        date = datetime.strptime(date_str[:10], '%Y-%m-%d').date()
        adj = db.session.execute(
            db.select(DailyAdjustment).where(DailyAdjustment.user_id == user.id, DailyAdjustment.date == date)
        ).scalar_one_or_none()
        if adj:
            old_minutes = adj.total_minutes
            adj.total_minutes = total_minutes
            adj.edited_by = current_user.id
            adj.updated_at = datetime.utcnow()
            db.session.commit()
            flash(f"Oppdatert justering for {date}: {old_minutes} → {total_minutes} minutter.", 'info')
        else:
            adj = DailyAdjustment(user_id=user.id, date=date, total_minutes=total_minutes, edited_by=current_user.id, updated_at=datetime.utcnow())
            db.session.add(adj)
            db.session.commit()
            flash(f"Lagt til justering for {date}: {total_minutes} minutter.", 'info')
        return redirect(url_for('auth.timelogs_user', user_id=user.id))

    # Finn siste hele uke (søndag passert)
    # Mandag = 0, Søndag = 6
    weekday_today = today.weekday()
    # Finn siste søndag (eller i dag hvis søndag)
    last_sunday = today - timedelta(days=(weekday_today + 1) % 7)
    # Finn første dag vi har data for (første TimeEntry eller DailyAdjustment)
    first_entry = db.session.execute(
        db.select(TimeEntry).where(TimeEntry.user_id == user.id).order_by(TimeEntry.start_time.asc())
    ).scalars().first()
    first_adjustment = db.session.execute(
        db.select(DailyAdjustment).where(DailyAdjustment.user_id == user.id).order_by(DailyAdjustment.date.asc())
    ).scalars().first()
    if first_entry and first_adjustment:
        first_date = min(first_entry.start_time.date(), first_adjustment.date)
    elif first_entry:
        first_date = first_entry.start_time.date()
    elif first_adjustment:
        first_date = first_adjustment.date
    else:
        first_date = today

    # Lag alle hele uker fra siste søndag og bakover til første data
    weeks = []
    week_end = last_sunday
    while week_end - timedelta(days=6) >= first_date:
        week_start = week_end - timedelta(days=6)
        # Hent alle justeringer for denne uken
        adjustments = {a.date.isoformat(): a for a in db.session.execute(
            db.select(DailyAdjustment).where(DailyAdjustment.user_id == user.id, DailyAdjustment.date >= week_start, DailyAdjustment.date <= week_end)
        ).scalars()}
        # Hent alle time entries for denne uken
        q = db.select(TimeEntry).where(
            TimeEntry.user_id == user.id,
            TimeEntry.start_time < week_end + timedelta(days=1),
            (TimeEntry.end_time == None) | (TimeEntry.end_time >= week_start),
        )
        entries = db.session.execute(q).scalars().all()
        per_day = []
        week_total = 0
        for i in range(7):
            d = week_start + timedelta(days=i)
            d_iso = d.isoformat()
            day_start = datetime(d.year, d.month, d.day)
            day_end = day_start + timedelta(days=1)
            if d_iso in adjustments:
                minutes = adjustments[d_iso].total_minutes
                source = 'justert'
            else:
                minutes = 0
                for e in entries:
                    s = e.start_time
                    en = e.end_time or datetime.utcnow()
                    if s < day_start:
                        s = day_start
                    if en > day_end:
                        en = day_end
                    delta = en - s
                    minutes += int(delta.total_seconds() // 60)
                source = 'automatisk'
            hours = minutes // 60
            mins = minutes % 60
            per_day.append({'date': d_iso, 'weekday': d.strftime('%A'), 'hours': hours, 'minutes': mins, 'total_minutes': minutes, 'source': source})
            week_total += minutes
        hh = week_total // 60
        mm = week_total % 60
        week_total_fmt = f"{hh:02d}:{mm:02d}"
        weeks.append({'week_start': week_start, 'week_end': week_end, 'per_day': per_day, 'week_total': week_total_fmt})
        week_end -= timedelta(days=7)

    # Legg til pågående uke hvis den ikke er ferdig (søndag ikke passert)
    # Sjekk om siste uke slutter før i dag
    ongoing_start = last_sunday + timedelta(days=1)
    if ongoing_start <= today:
        ongoing_end = today
        week_start = ongoing_start
        week_end = ongoing_end
        adjustments = {a.date.isoformat(): a for a in db.session.execute(
            db.select(DailyAdjustment).where(DailyAdjustment.user_id == user.id, DailyAdjustment.date >= week_start, DailyAdjustment.date <= week_end)
        ).scalars()}
        q = db.select(TimeEntry).where(
            TimeEntry.user_id == user.id,
            TimeEntry.start_time < week_end + timedelta(days=1),
            (TimeEntry.end_time == None) | (TimeEntry.end_time >= week_start),
        )
        entries = db.session.execute(q).scalars().all()
        per_day = []
        week_total = 0
        for i in range((week_end - week_start).days + 1):
            d = week_start + timedelta(days=i)
            d_iso = d.isoformat()
            day_start = datetime(d.year, d.month, d.day)
            day_end = day_start + timedelta(days=1)
            if d_iso in adjustments:
                minutes = adjustments[d_iso].total_minutes
                source = 'justert'
            else:
                minutes = 0
                for e in entries:
                    s = e.start_time
                    en = e.end_time or datetime.utcnow()
                    if s < day_start:
                        s = day_start
                    if en > day_end:
                        en = day_end
                    delta = en - s
                    minutes += int(delta.total_seconds() // 60)
                source = 'automatisk'
            hours = minutes // 60
            mins = minutes % 60
            per_day.append({'date': d_iso, 'weekday': d.strftime('%A'), 'hours': hours, 'minutes': mins, 'total_minutes': minutes, 'source': source})
            week_total += minutes
        hh = week_total // 60
        mm = week_total % 60
        week_total_fmt = f"{hh:02d}:{mm:02d}"
        weeks.insert(0, {'week_start': week_start, 'week_end': week_end, 'per_day': per_day, 'week_total': week_total_fmt})

    # Vis ukene nyeste først
    return render_template('timelogs_user.html', user=user, weeks=weeks)


@auth_bp.route('/time/start_by_rfid', methods=['POST'])
def start_time_by_rfid():
    """Start timer for user via RFID card scan (from Arduino listener)."""
    data = request.json
    rfid = data.get('rfid', '').strip()
    
    if not rfid:
        return {'error': 'No RFID provided'}, 400
    
    # Find user by RFID
    user = db.session.execute(db.select(User).where(User.rfid == rfid)).scalar_one_or_none()
    if not user:
        return {'error': 'User not found for RFID'}, 404
    
    # Check if already running
    running = db.session.execute(
        db.select(TimeEntry).where(TimeEntry.user_id == user.id, TimeEntry.end_time == None)
    ).scalar_one_or_none()
    if running:
        return {'error': 'Timer already running for user'}, 409
    
    # Start timer
    entry = TimeEntry(user_id=user.id)
    db.session.add(entry)
    db.session.commit()
    return {'status': 'ok', 'user': user.email, 'message': f'Timer started for {user.alias or user.email}'}


@auth_bp.route('/time/stop_by_rfid', methods=['POST'])
def stop_time_by_rfid():
    """Stop timer for user via RFID card scan (from Arduino listener)."""
    data = request.json
    rfid = data.get('rfid', '').strip()
    
    if not rfid:
        return {'error': 'No RFID provided'}, 400
    
    # Find user by RFID
    user = db.session.execute(db.select(User).where(User.rfid == rfid)).scalar_one_or_none()
    if not user:
        return {'error': 'User not found for RFID'}, 404
    
    # Find running entry
    running = db.session.execute(
        db.select(TimeEntry).where(TimeEntry.user_id == user.id, TimeEntry.end_time == None)
    ).scalar_one_or_none()
    if not running:
        return {'error': 'No running timer for user'}, 404
    
    # Stop timer
    running.end_time = datetime.utcnow()
    running.duration_seconds = int((running.end_time - running.start_time).total_seconds())
    db.session.commit()
    return {'status': 'ok', 'user': user.email, 'duration': running.duration_seconds}

