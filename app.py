from flask import Flask, jsonify, request
import sqlite3
from datetime import date, timedelta

app = Flask(__name__)

def get_interval_days(difficulty, revision_count):
    intervals = {
        "Hard": [7, 10, 14],
        "Medium": [10, 15, 20],
        "Easy": [14, 21, 28]
    }
    steps = intervals[difficulty]
    if revision_count <= len(steps):
        index = revision_count - 1
    else:
        index = len(steps) - 1
    return steps[index]

@app.route("/")
def home():
    return "Hello, tracker!"

@app.route("/problems", methods=["GET"])
def get_problems():
    conn = sqlite3.connect("tracker.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM problems")
    rows = cur.fetchall()
    conn.close()
    result = [dict(row) for row in rows]
    return jsonify(result)

@app.route("/problems", methods=["POST"])
def add_problem():
    data = request.json
    leetcode_id = data["leetcode_id"]
    pattern = data["pattern"]
    difficulty = data["difficulty"]
    date_completed = data["date_completed"]

    conn = sqlite3.connect("tracker.db")
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO problems (leetcode_id, pattern, difficulty, date_completed) VALUES (?, ?, ?, ?)",
        (leetcode_id, pattern, difficulty, date_completed)
    )
    conn.commit()
    conn.close()
    return jsonify({"message": "Problem added successfully"})

@app.route("/problems/<int:problem_id>/revise", methods=["PUT"])
def revise_problem(problem_id):
    conn = sqlite3.connect("tracker.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute("SELECT * FROM problems WHERE id = ?", (problem_id,))
    problem = cur.fetchone()

    if problem is None:
        conn.close()
        return jsonify({"error": "Problem not found"}), 404

    new_revision_count = problem["revision_count"] + 1
    today_str = str(date.today())
    days_to_add = get_interval_days(problem["difficulty"], new_revision_count)
    next_revisit = str(date.today() + timedelta(days=days_to_add))

    cur.execute(
        "UPDATE problems SET revision_count = ?, last_revised_date = ?, next_revisit_date = ? WHERE id = ?",
        (new_revision_count, today_str, next_revisit, problem_id)
    )
    conn.commit()
    conn.close()

    return jsonify({"message": "Problem revised", "next_revisit_date": next_revisit})

@app.route("/problems/<int:problem_id>", methods=["DELETE"])
def delete_problem(problem_id):
    conn = sqlite3.connect("tracker.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM problems WHERE id = ?", (problem_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Problem deleted"})

if __name__ == "__main__":
    app.run(debug=True)