from database import get_connection
from datetime import datetime, timedelta

# -------------------------
# CRUD Feed
# -------------------------
def create_feed(member_id, content=None, photo_path=None):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO feed (member_id, content, photo_url)
        VALUES (%s,%s,%s)
    """, (member_id, content, photo_path))
    conn.commit()
    cur.close()
    conn.close()

def check_text_feed_limit(member_id):
    conn = get_connection()
    cur = conn.cursor()
    today = datetime.utcnow().date()
    cur.execute("""
        SELECT COUNT(*) FROM feed
        WHERE member_id=%s AND content IS NOT NULL AND DATE(created_at)=%s
    """, (member_id, today))
    count = cur.fetchone()[0]
    cur.close()
    conn.close()
    return count

def check_photo_feed_limit(member_id):
    conn = get_connection()
    cur = conn.cursor()
    today = datetime.utcnow().date()
    cur.execute("""
        SELECT COUNT(*) FROM feed
        WHERE member_id=%s AND photo_url IS NOT NULL AND DATE(created_at)=%s
    """, (member_id, today))
    count = cur.fetchone()[0]
    cur.close()
    conn.close()
    return count
