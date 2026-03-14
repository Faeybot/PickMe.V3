import psycopg2
from psycopg2.extras import RealDictCursor
from config import DATABASE_URL

conn = psycopg2.connect(DATABASE_URL, sslmode='require')
cursor = conn.cursor(cursor_factory=RealDictCursor)

def init_db():
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS members (
        id SERIAL PRIMARY KEY,
        telegram_id BIGINT UNIQUE,
        username TEXT
    );
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS feeds (
        id SERIAL PRIMARY KEY,
        user_id BIGINT,
        text TEXT,
        photos TEXT[],
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS swipes (
        id SERIAL PRIMARY KEY,
        swiper_id BIGINT,
        member_id BIGINT,
        action TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)
    conn.commit()
    print("Database initialized")
