import sqlite3
import uuid
import requests
import streamlit as st
import random

DB_NAME = "aspect_sa.db"
API_URL = "http://localhost:5000/predict"

# ======================= DATABASE UTILS =======================

def create_connection(db_file=DB_NAME):
    """Tạo kết nối đến SQLite database."""
    try:
        return sqlite3.connect(db_file)
    except sqlite3.Error as e:
        st.error(f"Lỗi kết nối DB: {e}")

def run_sql(conn, sql, params=None, many=False):
    """Thực thi câu lệnh SQL."""
    try:
        cur = conn.cursor()
        if many:
            cur.executemany(sql, params)
        else:
            cur.execute(sql, params or ())
        conn.commit()
    except sqlite3.Error as e:
        st.error(f"Lỗi SQL: {e}")

# ======================= TẠO BẢNG =======================

def create_aspect_table(conn):
    run_sql(conn, """
    CREATE TABLE IF NOT EXISTS Aspect (
        id   INTEGER PRIMARY KEY,
        name TEXT NOT NULL UNIQUE
    );
    """)

def create_sentiment_table(conn):
    run_sql(conn, """
    CREATE TABLE IF NOT EXISTS Sentiment (
        id   INTEGER PRIMARY KEY,
        name TEXT NOT NULL UNIQUE
    );
    """)

def create_semester_table(conn):
    run_sql(conn, """
    CREATE TABLE IF NOT EXISTS Semester (
        id         INTEGER PRIMARY KEY AUTOINCREMENT,
        name       TEXT NOT NULL UNIQUE,
        start_date TEXT,
        end_date   TEXT
    );
    """)

def create_course_table(conn):
    run_sql(conn, """
    CREATE TABLE IF NOT EXISTS Course (
        id   INTEGER PRIMARY KEY AUTOINCREMENT,
        code TEXT NOT NULL UNIQUE,
        name TEXT NOT NULL
    );
    """)

def create_academic_year_table(conn):
    run_sql(conn, """
    CREATE TABLE IF NOT EXISTS AcademicYear (
        id         INTEGER PRIMARY KEY AUTOINCREMENT,
        name       TEXT NOT NULL UNIQUE,
        start_year INTEGER,
        end_year   INTEGER
    );
    """)

def create_class_table(conn):
    run_sql(conn, """
    CREATE TABLE IF NOT EXISTS Class (
        id                 INTEGER PRIMARY KEY AUTOINCREMENT,
        name               TEXT NOT NULL,
        academic_year_id   INTEGER,
        FOREIGN KEY (academic_year_id) REFERENCES AcademicYear(id),
        UNIQUE(name, academic_year_id)
    );
    """)

def create_student_table(conn):
    run_sql(conn, """
    CREATE TABLE IF NOT EXISTS Student (
        id           INTEGER PRIMARY KEY AUTOINCREMENT,
        student_code TEXT NOT NULL UNIQUE,
        name         TEXT NOT NULL,
        class_id     INTEGER,
        FOREIGN KEY (class_id) REFERENCES Class(id)
    );
    """)

def create_sentence_table(conn):
    run_sql(conn, """
    CREATE TABLE IF NOT EXISTS Sentence (
        id                TEXT PRIMARY KEY,
        text              TEXT NOT NULL,
        aspect_id         INTEGER,
        sentiment_id      INTEGER,
        semester_id       INTEGER,
        course_id         INTEGER,
        academic_year_id  INTEGER,
        class_id          INTEGER,
        student_id        INTEGER,
        FOREIGN KEY (aspect_id)        REFERENCES Aspect(id),
        FOREIGN KEY (sentiment_id)     REFERENCES Sentiment(id),
        FOREIGN KEY (semester_id)      REFERENCES Semester(id),
        FOREIGN KEY (course_id)        REFERENCES Course(id),
        FOREIGN KEY (academic_year_id) REFERENCES AcademicYear(id),
        FOREIGN KEY (class_id)         REFERENCES Class(id),
        FOREIGN KEY (student_id)       REFERENCES Student(id)
    );
    """)

# ======================= INSERT DỮ LIỆU MẪU =======================

def insert_aspect_data(conn):
    data = [
        (1, "Teaching quality"),
        (2, "Support from lecturers"),
        (3, "Learning environment"),
        (4, "Course information"),
        (5, "Organization and management"),
        (6, "Workload"),
        (7, "Test and evaluation"),
        (8, "General review")
    ]
    run_sql(conn, "INSERT OR IGNORE INTO Aspect (id, name) VALUES (?, ?)", data, many=True)

def insert_sentiment_data(conn):
    data = [
        (0, "Negative"),
        (1, "Neutral"),
        (2, "Positive")
    ]
    run_sql(conn, "INSERT OR IGNORE INTO Sentiment (id, name) VALUES (?, ?)", data, many=True)

def insert_semester_data(conn):
    data = []
    for year in range(2020, 2026):
        data.append((f"{year}HK1", f"{year}-01-01", f"{year}-05-31"))
        data.append((f"{year}HK2", f"{year}-08-01", f"{year}-12-31"))
    run_sql(conn, "INSERT OR IGNORE INTO Semester (name, start_date, end_date) VALUES (?, ?, ?)", data, many=True)

def insert_course_data(conn):
    data = [
        ("CS101", "Nhập môn Khoa học Máy tính"),
        ("ML202", "Machine Learning nâng cao"),
        ("DB303", "Cơ sở Dữ liệu"),
        ("AI404", "Trí tuệ Nhân tạo"),
        ("WEB505", "Phát triển Ứng dụng Web"),
        ("NET606", "Mạng Máy tính")
    ]
    run_sql(conn, "INSERT OR IGNORE INTO Course (code, name) VALUES (?, ?)", data, many=True)

def insert_academic_year_data(conn):
    data = []
    for start in range(2020, 2025):
        data.append((f"{start}-{start+1}", start, start+1))
    run_sql(conn, "INSERT OR IGNORE INTO AcademicYear (name, start_year, end_year) VALUES (?, ?, ?)", data, many=True)

def insert_class_data(conn):
    # Lấy tất cả năm học để gán class mẫu
    rows = conn.execute("SELECT id, start_year FROM AcademicYear ORDER BY id ASC").fetchall()
    data = []
    for (year_id, start_year) in rows:
        k_number = start_year - 1976
        for i, char in enumerate(['A', 'B']):
            class_name = f"K{k_number}{char}"
            data.append((class_name, year_id))
    run_sql(conn, "INSERT OR IGNORE INTO Class (name, academic_year_id) VALUES (?, ?)", data, many=True)

# ========= DANH SÁCH TÊN VIỆT NAM NGẪU NHIÊN CHO 200 SINH VIÊN ==========

HO_LIST = [
    "Nguyễn", "Trần", "Lê", "Phạm", "Hoàng", "Huỳnh", "Phan", "Vũ", "Võ", "Đặng",
    "Bùi", "Đỗ", "Hồ", "Ngô", "Dương", "Lý", "Đinh", "Trương", "Hà", "Vương"
]

DEM_LIST = [
    "Văn", "Thị", "Hữu", "Ngọc", "Quang", "Minh", "Tuấn", "Thanh", "Thị Thu", "Thái",
    "Gia", "Xuân", "Trung", "Đức", "Thành", "Hồng", "Thị Hồng", "Phương", "Khánh", ""
]

TEN_LIST = [
    "Anh", "Bình", "Châu", "Dũng", "Dung", "Hoa", "Hòa", "Hoàng", "Huy", "Hùng",
    "Kiên", "Lan", "Linh", "Long", "Mai", "Minh", "Nam", "Ngân", "Ngọc", "Nhung",
    "Phúc", "Phương", "Quân", "Quang", "Sơn", "Thảo", "Thành", "Thu", "Thủy", "Trang",
    "Triệu", "Trinh", "Trung", "Tuấn", "Tùng", "Việt", "Vy", "Yến", "Bảo", "Cường"
]

def gen_vietnamese_names(n):
    names = set()
    while len(names) < n:
        ho = random.choice(HO_LIST)
        dem = random.choice(DEM_LIST)
        ten = random.choice(TEN_LIST)
        if dem:
            name = f"{ho} {dem} {ten}"
        else:
            name = f"{ho} {ten}"
        names.add(name)
    return list(names)

def insert_student_data(conn):
    # Lấy danh sách class_id
    rows = conn.execute("SELECT id, name FROM Class ORDER BY id ASC").fetchall()
    class_ids = [(r[0], r[1]) for r in rows]
    total_students = 200
    students_per_class = total_students // len(class_ids)
    remainder = total_students % len(class_ids)

    # Tạo tên sinh viên
    names = gen_vietnamese_names(total_students)
    random.shuffle(names)

    data = []
    student_idx = 0
    for class_idx, (class_id, class_name) in enumerate(class_ids):
        num_students = students_per_class + (1 if class_idx < remainder else 0)
        for idx in range(num_students):
            code = f"SV{class_name}{idx+1:03d}"
            name = names[student_idx]
            data.append((code, name, class_id))
            student_idx += 1
    run_sql(conn, "INSERT OR IGNORE INTO Student (student_code, name, class_id) VALUES (?, ?, ?)", data, many=True)

# ======================= TẠO DATABASE CHUNG =======================

def create_database(db_file=DB_NAME):
    conn = create_connection(db_file)
    if not conn:
        st.error("Không thể kết nối DB")
        return

    # Tạo bảng theo thứ tự dependencies
    create_aspect_table(conn)
    create_sentiment_table(conn)
    create_semester_table(conn)
    create_course_table(conn)
    create_academic_year_table(conn)
    create_class_table(conn)
    create_student_table(conn)
    create_sentence_table(conn)

    # Insert mẫu
    insert_aspect_data(conn)
    insert_sentiment_data(conn)
    insert_semester_data(conn)
    insert_course_data(conn)
    insert_academic_year_data(conn)
    insert_class_data(conn)
    insert_student_data(conn)

    conn.close()

# ======================= HÀM HỖ TRỢ CHUNG =======================

@st.cache_resource(show_spinner=False)
def get_predictions(text: str, model="PhoBert_CNN_LSTM"):
    try:
        model_api_endpoint = None
        if model == "PhoBert_CNN_LSTM":
            model_api_endpoint = "http://localhost:5000/predict_pho"
        elif model == "CNN_LSTM_ATTENTION":
            model_api_endpoint = "http://localhost:5000/predict_cnn"
        resp = requests.post(model_api_endpoint, json={"text": text})
        resp.raise_for_status()
        data = resp.json()
        return [(it["aspect"], it["sentiment"]) for it in data.get("predictions", [])]
    except Exception as e:
        st.error(f"Lỗi khi gọi API: {e}")
        return []

def get_id(conn, table, key_col, key_val):
    cur = conn.cursor()
    cur.execute(f"SELECT id FROM {table} WHERE {key_col}=?", (key_val,))
    row = cur.fetchone()
    return row[0] if row else None

def get_lists(conn, table):
    cur = conn.cursor()
    cur.execute(f"SELECT name FROM {table}")
    return [r[0] for r in cur.fetchall()]

def insert_sentence(conn, text, aspect, sentiment, semester, course_code, academic_year, class_name, student_code):
    asp_id    = get_id(conn, "Aspect",    "name",         aspect)
    sen_id    = get_id(conn, "Sentiment", "name",         sentiment)
    sem_id    = get_id(conn, "Semester",  "name",         semester)
    course_id = get_id(conn, "Course",    "code",         course_code)
    year_id   = get_id(conn, "AcademicYear","name",       academic_year)
    class_id  = get_id(conn, "Class",     "name",         class_name)
    student_id= get_id(conn, "Student",   "student_code", student_code)

    sql = """
    INSERT INTO Sentence
      (id, text, aspect_id, sentiment_id, semester_id, course_id, academic_year_id, class_id, student_id)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    run_sql(conn, sql, (
        str(uuid.uuid4()), text,
        asp_id, sen_id, sem_id, course_id,
        year_id, class_id, student_id
    ))