import sqlite3

conn=sqlite3.connect("tracker.db")
cur=conn.cursor()

cur.execute("""
    CREATE TABLE IF NOT EXISTS leetcode_questions (
        id INTEGER PRIMARY KEY,
        title TEXT NOT NULL
    )
""")

cur.execute("""
    CREATE TABLE IF NOT EXISTS problems (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        leetcode_id INTEGER NOT NULL,
        pattern TEXT NOT NULL,
        difficulty TEXT NOT NULL,
        time_complexity TEXT,
        date_completed TEXT NOT NULL,
        last_revised_date TEXT,
        revision_count INTEGER DEFAULT 0,
        confidence INTEGER DEFAULT 0,
        next_revisit_date TEXT,
        starred INTEGER DEFAULT 0,
        notes TEXT,
        FOREIGN KEY (leetcode_id) REFERENCES leetcode_questions(id)
    )
""")

conn.commit()

cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
print(cur.fetchall())
