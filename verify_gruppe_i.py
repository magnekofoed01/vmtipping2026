grupper = {
    'I': [("Frankrike", "fr"), ("Senegal", "sn"), ("Norge", "no"), ("FIFA PO 2", None)]
}

kamper_I = [
    ("FIFA PO 2", "Norge", "2026-06-16"),
    ("Frankrike", "Senegal", "2026-06-16"),
    ("Frankrike", "FIFA PO 2", "2026-06-20"),
    ("Senegal", "Norge", "2026-06-20"),
    ("Frankrike", "Norge", "2026-06-25"),
    ("FIFA PO 2", "Senegal", "2026-06-25"),
]

print("GRUPPE I - KAMPOPPSETT")
print("=" * 60)
print("Gruppe I lag:")
for i, (lag, code) in enumerate(grupper['I']):
    print(f"  [{i}] {lag}")

print("\n" + "=" * 60)
print("Kamper:")
for i, (hjemme, borte, dato) in enumerate(kamper_I, 1):
    print(f"Kamp {i}: {hjemme:15} vs {borte:15} - {dato}")

print("\n" + "=" * 60)
print("ALLE LAG - KAMPOVERSIKT:")
print("=" * 60)
for team_name, _ in grupper['I']:
    print(f"\n{team_name}:")
    datoer = []
    for hjemme, borte, dato in kamper_I:
        if team_name in [hjemme, borte]:
            motst = borte if hjemme == team_name else hjemme
            datoer.append(dato)
            print(f"  vs {motst:15} - {dato}")
    
    # Sjekk for duplikater
    if len(datoer) != len(set(datoer)):
        print(f"  ❌ KONFLIKT: Spiller flere kamper samme dag!")
    else:
        print(f"  ✅ OK: Alle kamper på forskjellige dager")
