from db import get_db

def set_height(height): 
    db = get_db()
    db.execute(
        """INSERT INTO heights (value)
        VALUES (?)""",
        (height,)
    )
    db.commit()

def get_height():
    check = get_db().execute(
        """SELECT *
        FROM heights
        ORDER BY TIMESTAMP DESC
        LIMIT 1"""
    ).fetchone()

    return check
