from database import get_connection
import random

# -------------------------
# Swipe / Matching
# -------------------------
def get_random_member(swiper_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM members WHERE id != %s", (swiper_id,))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    if not rows:
        return None
    row = random.choice(rows)
    return dict(zip([desc[0] for desc in cur.description], row))

def record_swipe(swiper_id, swiped_id, action):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO swipes (swiper_id, swiped_id, action)
        VALUES (%s,%s,%s)
    """, (swiper_id, swiped_id, action))
    conn.commit()
    cur.close()
    conn.close()

def check_daily_swipe_limit(swiper_id):
    from datetime import datetime
    conn = get_connection()
    cur = conn.cursor()
    today = datetime.utcnow().date()
    cur.execute("""
        SELECT COUNT(*) FROM swipes
        WHERE swiper_id=%s AND DATE(created_at)=%s
    """, (swiper_id, today))
    count = cur.fetchone()[0]
    cur.close()
    conn.close()
    return count
