from groq import Groq
from flask import Flask, request, jsonify, send_from_directory
import sqlite3
from datetime import datetime
import random

app = Flask(__name__)

# ================= GROQ API =================
# Replace with your Groq API Key
client = Groq(
    api_key="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"
)

# ================= HOME =================
@app.route('/')
def home():
    return send_from_directory('.', 'Peer Collab Hub fixed.html')

# ================= AUTHENTICATION =================
@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.json
        student_id = data.get("student_id")
        password = data.get("password")

        if not student_id or not password:
            return jsonify({"status": "fail", "message": "Missing credentials"})

        conn = sqlite3.connect("students.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students WHERE student_id=?", (student_id,))
        student = cursor.fetchone()
        conn.close()

        if student and student[2] == password:
            return jsonify({
                "status": "success",
                "student": {
                    "student_id": student[1],
                    "name": student[3],
                    "semester": student[4],
                    "subjects": student[5],
                    "fees_total": student[6],
                    "fees_balance": student[7],
                    "gpa": student[8],
                    "attendance": student[9],
                    "quiz_marks": student[10],
                    "test_marks": student[11],
                    "assignment_marks": student[12],
                    "coursework": student[13],
                    "credit_hours": student[14],
                    "next_sem_subjects": student[15],
                    "pass_status": student[16]
                }
            })
        return jsonify({"status": "fail", "message": "Invalid Student ID or Password."})
    except Exception as e:
        print("LOGIN ERROR:", e)
        return jsonify({"status": "fail", "message": "Server error"})

# ================= AI SUPPORT =================
@app.route('/ai-support', methods=['POST'])
def ai_support():
    try:
        data = request.json
        message = data.get("message")
        student_id = data.get("student_id", "1231303288")

        if not message:
            return jsonify({"reply": "Please enter a message."})

        conn = sqlite3.connect("students.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students WHERE student_id=?", (student_id,))
        student = cursor.fetchone()
        conn.close()

        if student:
            student_info = f"""
            Name: {student[3]}
            Semester: {student[4]}
            Subjects: {student[5]}
            CGPA: {student[8]}
            Attendance: {student[9]}%
            """
        else:
            student_info = "Student data unavailable."

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",   # ✅ Correct model name
            max_tokens=120,
            temperature=0.7,
            messages=[
                {"role": "system", "content": f"You are a university AI assistant. Reply briefly and clearly.\n\nStudent:\n{student_info}"},
                {"role": "user", "content": message}
            ]
        )

        reply = response.choices[0].message["content"]  # ✅ Correct parsing
        return jsonify({"reply": reply})

    except Exception as e:
        print("AI SUPPORT ERROR:", e)
        return jsonify({"reply": f"AI Error: {str(e)}"})

# ================= GET POSTS =================
@app.route('/get-posts')
def get_posts():
    try:
        conn = sqlite3.connect("students.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, student_name, message, likes, comments, created_at FROM peer_posts ORDER BY id DESC")
        posts = cursor.fetchall()
        conn.close()

        result = []
        for post in posts:
            result.append({
                "id": post[0],
                "student_name": post[1],
                "message": post[2],
                "likes": post[3],
                "comments": post[4],
                "created_at": post[5]
            })
        return jsonify(result)
    except Exception as e:
        print("GET POSTS ERROR:", e)
        return jsonify([])

# ================= ADD POST =================
@app.route('/add-post', methods=['POST'])
def add_post():
    try:
        data = request.json
        message = data.get("message")
        if not message:
            return jsonify({"status": "fail"})

        names = ["Alex","Sarah","Daniel","Aisyah","Jason","Farah","Amir","Sophia","John","Haziq","Emily","Ryan"]
        student_name = random.choice(names)

        conn = sqlite3.connect("students.db")
        cursor = conn.cursor()
        created_at = datetime.now().strftime("%d %b %Y %I:%M %p")

        cursor.execute("INSERT INTO peer_posts(student_name,message,likes,comments,created_at) VALUES(?,?,?,?,?)",
                       (student_name, message, 0, "", created_at))
        conn.commit()
        post_id = cursor.lastrowid

        # AI comment
        try:
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",   # ✅ Same corrected model
                messages=[
                    {"role": "system", "content": "You are a friendly university student. Reply briefly to the post."},
                    {"role": "user", "content": message}
                ]
            )
            ai_reply = response.choices[0].message["content"]  # ✅ Correct parsing
        except Exception as ai_error:
            print("POST AI ERROR:", ai_error)
            ai_reply = "Nice post! 👍"

        comments = f"<p>💬 {ai_reply}</p>"
        likes = random.randint(1, 5)

        cursor.execute("UPDATE peer_posts SET comments=?, likes=? WHERE id=?", (comments, likes, post_id))
        conn.commit()
        conn.close()

        return jsonify({"status": "success"})
    except Exception as e:
        print("ADD POST ERROR:", e)
        return jsonify({"status": "fail"})

# ================= LIKE POST =================
@app.route('/like-post/<int:post_id>', methods=['POST'])
def like_post(post_id):
    try:
        conn = sqlite3.connect("students.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE peer_posts SET likes = likes + 1 WHERE id=?", (post_id,))
        conn.commit()
        conn.close()
        return jsonify({"status": "liked"})
    except Exception as e:
        print("LIKE ERROR:", e)
        return jsonify({"status": "error"})

# ================= COMMENT POST =================
@app.route('/comment-post/<int:post_id>', methods=['POST'])
def comment_post(post_id):
    try:
        data = request.json
        comment = data.get("comment")
        conn = sqlite3.connect("students.db")
        cursor = conn.cursor()
        cursor.execute("SELECT comments FROM peer_posts WHERE id=?", (post_id,))
        row = cursor.fetchone()
        current = row[0] if row else ""
        updated_comments = current + f"<p>💬 {comment}</p>"
        cursor.execute("UPDATE peer_posts SET comments=? WHERE id=?", (updated_comments, post_id))
        conn.commit()
        conn.close()
        return jsonify({"status": "comment added"})
    except Exception as e:
        print("COMMENT ERROR:", e)
        return jsonify({"status": "error"})

# ================= MAIN =================
if __name__ == '__main__':
    app.run(debug=True)   # ✅ Debug enabled for testing
