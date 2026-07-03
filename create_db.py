import sqlite3

conn = sqlite3.connect("students.db")
cursor = conn.cursor()

# Dropping existing tables to start clean
cursor.execute("DROP TABLE IF EXISTS students")
cursor.execute("DROP TABLE IF EXISTS peer_posts")
cursor.execute("DROP TABLE IF EXISTS study_groups")

# STUDENTS TABLE
cursor.execute("""
CREATE TABLE students(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id TEXT UNIQUE,
    password TEXT,
    name TEXT,
    semester INTEGER,
    subjects TEXT,
    fees_total REAL,
    fees_balance REAL,
    gpa REAL,
    attendance INTEGER,
    quiz_marks TEXT,
    test_marks TEXT,
    assignment_marks TEXT,
    coursework TEXT,
    credit_hours INTEGER,
    next_sem_subjects TEXT,
    pass_status TEXT
)
""")

# Insert 5 sample students
students_data = [
    (
        '123', '123', 'Alex Rivera', 3,
        'Artificial Intelligence, Networking, Web Development',
        3500.0, 500.0, 3.25, 78,
        '85', '72', '88', '80%', 75,
        'Cloud Computing, Cyber Security', 'PASS'
    ),
    (
        '124', '124', 'Sarah Chen', 4,
        'Software Engineering, Database Systems, Cloud Computing',
        4200.0, 0.0, 3.85, 95,
        '92', '90', '95', '93%', 90,
        'Mobile App Development, DevOps', 'PASS'
    ),
    (
        '125', '125', 'Marcus Vance', 2,
        'Data Structures, Object-Oriented Programming, Discrete Mathematics',
        3800.0, 1200.0, 2.90, 65,
        '60', '58', '70', '64%', 45,
        'Operating Systems, Algorithms', 'PASS'
    ),
    (
        '126', '126', 'Haziq Daniel', 3,
        'Web Development, Human Computer Interaction, Networking',
        3500.0, 2000.0, 2.10, 55,
        '45', '38', '50', '46%', 60,
        'Requirements Engineering, System Analysis', 'FAIL'
    ),
    (
        '127', '127', 'Emily Watson', 5,
        'Cyber Security, Mobile App Development, Artificial Intelligence',
        4500.0, 0.0, 3.60, 88,
        '78', '80', '85', '82%', 105,
        'Thesis Project, Professional Ethics', 'PASS'
    ),
    # ----- 4 newly added students -----
    (
        '128', '128', 'Nurul Izzah', 3,
        'Artificial Intelligence, Web Development, Database Systems',
        4000.0, 1500.0, 3.40, 82,
        '80', '76', '84', '80%', 72,
        'Cloud Computing, Mobile App Development', 'PASS'
    ),
    (
        '129', '129', 'Lim Wei Jie', 2,
        'Data Structures, Object-Oriented Programming, Discrete Mathematics',
        3800.0, 0.0, 3.10, 70,
        '68', '65', '74', '69%', 48,
        'Operating Systems, Algorithms', 'PASS'
    ),
    (
        '130', '130', 'Arjun Mehta', 4,
        'Software Engineering, Networking, Cloud Computing',
        4200.0, 800.0, 3.70, 91,
        '88', '86', '90', '88%', 88,
        'DevOps, Cyber Security', 'PASS'
    ),
    (
        '131', '131', 'Chloe Tan', 5,
        'Cyber Security, Human Computer Interaction, Artificial Intelligence',
        4500.0, 2500.0, 2.40, 58,
        '50', '48', '55', '51%', 100,
        'Thesis Project, Professional Ethics', 'FAIL'
    )
]

cursor.executemany("""
INSERT INTO students(
    student_id, password, name, semester, subjects,
    fees_total, fees_balance, gpa, attendance,
    quiz_marks, test_marks, assignment_marks,
    coursework, credit_hours, next_sem_subjects, pass_status
)
VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
""", students_data)

# PEER POSTS TABLE
cursor.execute("""
CREATE TABLE peer_posts(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_name TEXT,
    message TEXT,
    likes INTEGER DEFAULT 0,
    comments TEXT DEFAULT '',
    created_at TEXT
)
""")

# Insert existing 15 posts
existing_posts = [
  (
    "Aisyah",
    "Does anyone have tips for revising Networking?",
    3,
    "<p>💬 Try using Packet Tracer for practice.</p><p>💬 Revise lecture slides weekly.</p>",
    "15 May 2026 10:30 AM"
  ),
  (
    "Daniel",
    "How do you prepare for AI subject quizzes?",
    5,
    "<p>💬 Practice coding exercises.</p><p>💬 Focus on machine learning basics.</p>",
    "15 May 2026 11:00 AM"
  ),
  (
    "Sophia",
    "Anyone going to the career fair tomorrow?",
    1,
    "<p>💬 Yeah, I'm planning to attend! If anyone wants to carpool or meet up for the same companies to check out, I'd be happy to connect and make a list of the booths we're interested in.</p>",
    "21 May 2026 02:56 AM"
  ),
  (
    "Farah",
    "What’s one thing that could make campus life better?",
    2,
    "<p>💬 I think having later library and study hall hours would be amazing! It's not uncommon for students to be working on group projects and studying until late at night, so having a quiet space to work on after the original hours close would really help with productivity and avoiding cramming.</p>",
    "21 May 2026 02:59 AM"
  ),
  (
    "Sarah",
    "Anyone going to the career fair tomorrow?",
    3,
    "<p>💬 Yeah, I'm planning to attend the career fair tomorrow. I'm thinking of reaching out to some companies in my field, especially the ones I've been eyeing for internships. If you're going, I'd love to meet up and discuss some of the opportunities we're interested in.</p>",
    "21 May 2026 02:59 AM"
  ),
  (
    "Haziq",
    "Looking for a group to join for project assignment",
    4,
    "<p>💬 We're actually working on a project too and could use some extra members to make it more collaborative. What's your assignment focused on (e.g., marketing, product development, data analysis)?</p>",
    "21 May 2026 02:59 AM"
  ),
  (
    "Jason",
    "Is the library open until midnight during exam week?",
    3,
    "<p>💬 I just checked the university's schedule, and the library is indeed open 24/7 during exam week. The building will be staffed until midnight on the weekdays, and security will take over after that. If you need any specific resources or help, feel free to ask the librarians at the front desk. Good luck with your exams!</p>",
    "21 May 2026 03:00 AM"
  ),
  (
    "Emily",
    "What’s your favorite chill spot on campus?",
    2,
    "<p>💬 I'm a big fan of the university's student union lounge! They have comfy couches, free coffee, and it's usually pretty quiet during exam season. Plus, it's close to the library, so it's easy to grab a snack or study break. Does anyone else have favorite chill spots on campus?</p>",
    "21 May 2026 03:00 AM"
  ),
  (
    "Sarah",
    "Anyone has past year papers?",
    3,
    "<p>💬 I have a friend who shared last year's exam papers with me. I'd be happy to share them with you, just DM me!</p><p>💬 can open mmu library</p>",
    "21 May 2026 03:00 AM"
  ),
  (
    "Amir",
    "What’s your favorite hangout spot after class?",
    1,
    "<p>💬 I'm really fond of the student lounge at the library - it's super quiet for studying, but they have a nice cafe area with comfy couches and big windows, plus it's open late!</p>",
    "21 May 2026 03:00 AM"
  ),
  (
    "Farah",
    "Any updates on parking availability?",
    1,
    "<p>💬 Hello! I just checked the university's parking website, and it says that lot B-3 has some availability due to recent student absences. However, I'd recommend checking the app or calling the parking office for the most up-to-date info.</p><p>💬 during peak hours no parking inside the campus</p>",
    "21 May 2026 03:00 AM"
  ),
  (
    "Aisyah",
    "Who’s joining the volunteer program this semester?",
    2,
    "<p>💬 That sounds like a great opportunity! I'm planning to join, and I know a few friends from my environmental club are signing up too. Have you decided which cause you're supporting this semester?</p>",
    "21 May 2026 03:00 AM"
  ),
  (
    "Daniel",
    "Is the cafeteria still open after 10PM?",
    5,
    "<p>💬 I'm pretty sure it's not open that late, but I'm double-checking with someone who works in food services. Let me confirm and I'll get back to you!</p><p>💬 to avoid buy them before 8PM</p>",
    "21 May 2026 03:00 AM"
  ),
  (
    "Emily",
    "What’s one thing that could make campus life better?",
    5,
    "<p>💬 Free food Fridays in the library or student lounge would be amazing. Imagine being able to relax and study between lectures without worrying about lunch. It would really help students feel more at home on campus.</p>",
    "21 May 2026 03:14 AM"
  ),
  (
    "Emily",
    "is the library full?",
    6,
    "<p>💬 I just checked the library's floor plan, and it looks like there are open spots in the quiet area on the second floor. You might want to check it out!</p><p>💬 during peak hours</p>",
    "21 May 2026 09:15 AM"
  )
]

cursor.executemany("""
INSERT INTO peer_posts(student_name, message, likes, comments, created_at)
VALUES(?,?,?,?,?)
""", existing_posts)

# STUDY GROUPS TABLE
cursor.execute("""
CREATE TABLE study_groups(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    subject TEXT,
    topic TEXT,
    creator TEXT,
    members_count INTEGER,
    max_members INTEGER,
    status TEXT
)
""")

# Insert initial sample study groups
sample_groups = [
    ("Artificial Intelligence", "Quiz 2 Prep - Machine Learning basics", "Sarah Chen", 3, 5, "OPEN"),
    ("Networking", "Lab Exam 1 - Subnetting practice session", "Alex Rivera", 4, 4, "CLOSED"),
    ("Web Development", "Group Assignment - Glassmorphism UI ideas", "Marcus Vance", 2, 6, "OPEN")
]

cursor.executemany("""
INSERT INTO study_groups(subject, topic, creator, members_count, max_members, status)
VALUES(?,?,?,?,?,?)
""", sample_groups)

conn.commit()
conn.close()
print("students.db created successfully with 9 students, 15 posts, and 3 study groups.")
