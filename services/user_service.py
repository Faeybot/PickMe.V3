from database import get_connection

# -------------------------
# CRUD Member
# -------------------------
def create_member(telegram_id, username, age, gender, interest, about_me, photo_path, city=None, province=None, country=None):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO members (telegram_id, username, age, gender, interest, about_me, photo_url, city, province, country)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id
    """, (telegram_id, username, age, gender, interest, about_me, photo_path, city, province, country))
    member_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return member_id

def get_member_by_telegram(telegram_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM members WHERE telegram_id=%s", (telegram_id,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    if row:
        return dict(zip([desc[0] for desc in cur.description], row))
    return None
