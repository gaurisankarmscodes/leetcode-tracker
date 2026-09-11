import sqlite3
import csv

conn = sqlite3.connect("tracker.db")
cur = conn.cursor()

with open("leetcode problems dataset.csv", "r", encoding="utf-8") as file:
    reader = csv.reader(file)
    next(reader)  # skip header
    for row in reader:
        cur.execute("INSERT INTO leetcode_questions (id, title) VALUES (?, ?)", (row[0], row[1]))

conn.commit()
print("Import done")

cur.execute("SELECT COUNT(*) FROM leetcode_questions")
print(cur.fetchone())