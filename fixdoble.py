import sqlite3

db_path = '/data/tips.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

for fase in ['8-delsfinale', 'Kvartfinale', 'Semifinale', 'Finale']:
    cursor.execute("""
        SELECT navn, lag, COUNT(*) as antall
        FROM sluttspilltips
        WHERE fase = ?
        GROUP BY navn, lag
        HAVING COUNT(*) >= 2
        ORDER BY antall DESC, navn, lag
    """, (fase,))
    duplikate_tips = cursor.fetchall()

    if duplikate_tips:
        print(f"\nPersoner som har tippet samme lag flere ganger i {fase}:")
        print("-" * 60)
        for navn, lag, antall in duplikate_tips:
            print(f"{navn}: {lag} ({antall} ganger)")

        for navn, lag, antall in duplikate_tips:
            cursor.execute("""
                DELETE FROM sluttspilltips
                WHERE rowid IN (
                    SELECT rowid
                    FROM sluttspilltips
                    WHERE fase = ? AND navn = ? AND lag = ?
                    ORDER BY rowid
                    LIMIT ? OFFSET 1
                )
            """, (fase, navn, lag, antall - 1))

        conn.commit()
        print(f"✓ Fjernet {sum(antall - 1 for _, _, antall in duplikate_tips)} duplikater i {fase}")
    else:
        print(f"\nIngen duplikater i {fase}.")

conn.close()