import sqlite3

# Connect to the database
db_path = '/data/tips.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Hent ut personer som har tippet samme lag flere ganger i Finale
cursor.execute("""
    SELECT navn, lag, COUNT(*) as antall
    FROM sluttspilltips
    WHERE fase = 'Finale'
    GROUP BY navn, lag
    HAVING COUNT(*) >= 2
    ORDER BY antall DESC, navn, lag
""")
duplikate_tips = cursor.fetchall()

if duplikate_tips:
    print("Personer som har tippet samme lag flere ganger i Finale:")
    print("-" * 60)
    for navn, lag, antall in duplikate_tips:
        print(f"{navn}: {lag} ({antall} ganger)")
    
    print(f"\nTotalt antall duplikater: {len(duplikate_tips)}")
    
    # Fjern duplikater ved å blanke ut alle unntatt det første tipset
    for navn, lag, antall in duplikate_tips:
        cursor.execute("""
            UPDATE sluttspilltips
            SET lag = ''
            WHERE rowid IN (
                SELECT rowid
                FROM sluttspilltips
                WHERE fase = 'Finale' AND navn = ? AND lag = ?
                ORDER BY rowid
                LIMIT ? OFFSET 1
            )
        """, (navn, lag, antall - 1))
    
    conn.commit()
    print(f"\n✓ Fjernet {sum(antall - 1 for _, _, antall in duplikate_tips)} duplikater")
else:
    print("Ingen har tippet samme lag flere ganger i Finale.")

conn.close()
