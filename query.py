import sqlite3

c = sqlite3.connect(r"c:\kildekode\VMTipping2026\tips_backup.db")

print("=== Tabeller ===")
for r in c.execute("SELECT name FROM sqlite_master WHERE type='table'"):
    print(f"  {r[0]}")

print("\n=== Topp VM-vinner tips ===")
for r in c.execute("SELECT lag, COUNT(*) as antall FROM sluttspilltips WHERE fase='Vinner' GROUP BY lag ORDER BY antall DESC LIMIT 50"):
    print(f"  {r[0]}: {r[1]} tips")

print("\n=== Hvem tipset hva ===")
for r in c.execute("SELECT navn, lag FROM sluttspilltips WHERE fase='Vinner' ORDER BY lag, navn"):
    print(f"  {r[0]} -> {r[1]}")

print("=== Navn, tlf,  epost ===")
for r in c.execute("SELECT DISTINCT navn, telefon, epost FROM tips"):
    print(f"  {r[0]} - {r[1]} - {r[2]}")

print("=== epost ===")
for r in c.execute("SELECT DISTINCT epost FROM tips"):
    print(f"  {r[0]}")

c.close()
