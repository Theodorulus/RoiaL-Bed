from db import get_db

def get_mode_by_name(mode):
    check = get_db().execute(
        """SELECT id, value, height, temperature
        FROM modes
        WHERE value = ?""",
        (mode,)
    ).fetchone()
    return check

def set_active_mode(mode):
    db = get_db()
    db.execute(
        """UPDATE modes
        SET active = 0
        WHERE active = 1"""
    )
    db.execute(
        """UPDATE modes
        SET active = 1
        WHERE value = ?""",
        (mode,)
    )
    db.commit()

def get_active_mode():
    check = get_db().execute(
        """SELECT id, value, height, temperature
        FROM modes
        WHERE active = 1"""
    ).fetchone()
    return check

def create_mode(mode, height, temp):
    db = get_db()
    db.execute(
        """INSERT INTO modes (value, height, temperature)
        VALUES (?, ?, ?)""",
        (mode, height, temp,)
    )
    db.commit()

def get_last_created_mode():
    check = get_db().execute(
        """SELECT id, value, height, temperature
        FROM modes
        ORDER BY timestamp DESC"""
    ).fetchone()
    return check