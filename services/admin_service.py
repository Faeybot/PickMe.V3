from database import get_connection

# -------------------------
# Reports / Admin
# -------------------------
def create_report(reporter_id, reported_id, reason):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO reports (reporter_id, reported_id, reason)
        VALUES (%s,%s,%s)
    """, (reporter_id, reported_id, reason))
    conn.commit()

    # Cek jumlah report untuk ban otomatis
    cur.execute("""
        SELECT COUNT(*) FROM reports
        WHERE reported_id=%s
    """, (reported_id,))
    count = cur.fetchone()[0]

    # Aturan: 3 laporan -> peringatan, 10 laporan -> ban
    if count >= 10:
        cur.execute("DELETE FROM members WHERE id=%s", (reported_id,))
        conn.commit()
    cur.close()
    conn.close()
