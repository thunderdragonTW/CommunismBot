import sqlite3

def setup_database():
    dbfile = "socialcredit.db"
    conn = sqlite3.connect(dbfile)
    cursor = conn.cursor()

    # Create the scores table if it doesn't exist
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS scores (
        member_id INTEGER PRIMARY KEY,
        score INTEGER NOT NULL,
        xp INTEGER NOT NULL DEFAULT 0,
        level INTEGER NOT NULL DEFAULT 1
    )
    """)

    conn.commit()
    conn.close()

setup_database()

