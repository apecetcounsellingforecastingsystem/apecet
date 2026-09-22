"""
Database connection and schema initialization for AP ECET Counselling Forecasting System.
Uses SQLite for robust, portable, zero-configuration local storage.
"""

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'ap_ecet.db')

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # 1. Users table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        phone TEXT,
        password_hash TEXT NOT NULL,
        role TEXT NOT NULL DEFAULT 'student',
        is_active INTEGER NOT NULL DEFAULT 1,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # 2. Student Profiles
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS student_profiles (
        user_id INTEGER PRIMARY KEY,
        rank INTEGER,
        category TEXT DEFAULT 'OC',
        gender TEXT DEFAULT 'BOYS',
        region TEXT DEFAULT 'AU',
        district TEXT,
        preferred_branch TEXT,
        counselling_round TEXT DEFAULT 'Phase 1',
        college_type TEXT DEFAULT 'ALL',
        max_budget INTEGER,
        diploma_branch TEXT,
        alternative_branch TEXT,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    try:
        cursor.execute("ALTER TABLE student_profiles ADD COLUMN diploma_branch TEXT")
    except sqlite3.OperationalError:
        pass
    try:
        cursor.execute("ALTER TABLE student_profiles ADD COLUMN alternative_branch TEXT")
    except sqlite3.OperationalError:
        pass

    # 3. Colleges
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS colleges (
        college_code TEXT PRIMARY KEY,
        college_name TEXT NOT NULL,
        district TEXT,
        place TEXT,
        region TEXT,
        affiliated_to TEXT,
        type TEXT,
        year_of_establishment INTEGER,
        website TEXT,
        college_type TEXT,
        minority_status TEXT,
        hostel_availability TEXT,
        phone TEXT,
        email TEXT,
        address TEXT,
        is_active INTEGER DEFAULT 1
    );
    """)

    # 4. Branches
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS branches (
        branch_code TEXT PRIMARY KEY,
        branch_name TEXT NOT NULL,
        department TEXT
    );
    """)

    # 5. College Branches (Intake and Fees)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS college_branches (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        college_code TEXT NOT NULL,
        branch_code TEXT NOT NULL,
        branch_name TEXT,
        total_intake_seats INTEGER DEFAULT 0,
        fees INTEGER DEFAULT 0
    );
    """)

    # 6. Cutoffs
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cutoffs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        year INTEGER NOT NULL,
        round TEXT NOT NULL,
        college_code TEXT NOT NULL,
        college_name TEXT,
        place TEXT,
        branch_name TEXT NOT NULL,
        branch_code TEXT,
        gender TEXT NOT NULL,
        category TEXT NOT NULL,
        opening_rank INTEGER,
        closing_rank INTEGER,
        is_forecasted INTEGER DEFAULT 0
    );
    """)

    # 7. Predictions Log
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS predictions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        student_rank INTEGER NOT NULL,
        category TEXT NOT NULL,
        gender TEXT NOT NULL,
        region TEXT,
        branch TEXT NOT NULL,
        counselling_round TEXT NOT NULL,
        district TEXT,
        college_type TEXT,
        max_budget INTEGER,
        total_recommended INTEGER DEFAULT 0,
        top_college_name TEXT,
        top_probability REAL,
        top_classification TEXT,
        results_json TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # 8. Saved Colleges
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS saved_colleges (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        college_code TEXT NOT NULL,
        branch_name TEXT,
        notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(user_id, college_code, branch_name)
    );
    """)

    # 9. Preference Lists
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS preference_lists (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        preference_order INTEGER NOT NULL,
        college_code TEXT NOT NULL,
        college_name TEXT,
        branch_name TEXT NOT NULL,
        district TEXT,
        classification TEXT,
        probability REAL,
        closing_rank INTEGER,
        fees INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # 10. Notifications
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS notifications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT NOT NULL,
        alert_type TEXT DEFAULT 'normal',
        publish_date TEXT NOT NULL,
        is_active INTEGER DEFAULT 1,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # 11. Counselling Calendar
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS counselling_calendar (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        stage_order INTEGER NOT NULL,
        stage_name TEXT NOT NULL,
        start_date TEXT,
        end_date TEXT,
        status TEXT DEFAULT 'upcoming',
        description TEXT
    );
    """)

    # 12. OTP verification tokens (email / phone)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS otp_tokens (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        target TEXT NOT NULL,
        channel TEXT NOT NULL,
        otp_code TEXT NOT NULL,
        purpose TEXT DEFAULT 'register',
        is_verified INTEGER DEFAULT 0,
        attempts INTEGER DEFAULT 0,
        expires_at TIMESTAMP NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # 13. Password reset tokens
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS password_reset_tokens (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        token TEXT UNIQUE NOT NULL,
        expires_at TIMESTAMP NOT NULL,
        used INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # 14. Login rate-limit log (simple security)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS login_attempts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        identifier TEXT NOT NULL,
        ip_address TEXT,
        success INTEGER DEFAULT 0,
        attempted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # Indexes
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_cutoffs_lookup ON cutoffs(year, round, category, gender, branch_name);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_cutoffs_college ON cutoffs(college_code);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_cutoffs_closing ON cutoffs(closing_rank);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_college_branches ON college_branches(college_code, branch_name);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_predictions_user ON predictions(user_id);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_otp_target ON otp_tokens(target, channel);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_login_attempts ON login_attempts(identifier, attempted_at);")

    conn.commit()
    conn.close()
    print("Database tables & indexes initialized successfully.")

if __name__ == '__main__':
    init_db()
