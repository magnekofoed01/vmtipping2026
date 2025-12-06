grupper = {
    'B': [("Canada", "ca"), ("Qatar", "qa"), ("Sveits", "ch"), ("UEFA PO A", None)]
}

kamper_B = [
    ("Canada", "UEFA PO A", "2026-06-12"),
    ("Qatar", "Sveits", "2026-06-14"),
    ("Canada", "Qatar", "2026-06-17"),
    ("Sveits", "UEFA PO A", "2026-06-17"),
    ("Canada", "Sveits", "2026-06-22"),
    ("Qatar", "UEFA PO A", "2026-06-22"),
]

print("GRUPPE B - KAMPOPPSETT")
print("=" * 60)
print("Gruppe B lag:")
for i, (lag, code) in enumerate(grupper['B']):
    print(f"  [{i}] {lag}")

print("\n" + "=" * 60)
print("Kamper:")
for i, (hjemme, borte, dato) in enumerate(kamper_B, 1):
    print(f"Kamp {i}: {hjemme:15} vs {borte:15} - {dato}")

print("\n" + "=" * 60)
print("ALLE LAG - KAMPOVERSIKT:")
print("=" * 60)
for team_name, _ in grupper['B']:
    print(f"\n{team_name}:")
    datoer = []
    for hjemme, borte, dato in kamper_B:
        if team_name in [hjemme, borte]:
            motst = borte if hjemme == team_name else hjemme
            datoer.append(dato)
            print(f"  vs {motst:15} - {dato}")
    
    # Sjekk for duplikater
    if len(datoer) != len(set(datoer)):
        print(f"  ❌ KONFLIKT: Spiller flere kamper samme dag!")
    else:
        print(f"  ✅ OK: Alle kamper på forskjellige dager")
