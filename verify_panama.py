grupper = {
    'L': [('England', 'gb-eng'), ('Kroatia', 'hr'), ('Ghana', 'gh'), ('Panama', 'pa')]
}

# Offisielt oppsett fra FIFA
kamper_L = [
    ("England", "Kroatia", "2026-06-17"),
    ("Ghana", "Panama", "2026-06-17"),
    ("England", "Ghana", "2026-06-21"),
    ("Kroatia", "Panama", "2026-06-21"),
    ("England", "Panama", "2026-06-27"),
    ("Kroatia", "Ghana", "2026-06-27"),
]

print("GRUPPE L - KAMPOPPSETT")
print("=" * 60)
for i, (hjemme, borte, dato) in enumerate(kamper_L, 1):
    print(f"Kamp {i}: {hjemme:15} vs {borte:15} - {dato}")

print("\n" + "=" * 60)
print("PANAMA SINE KAMPER:")
print("=" * 60)
for hjemme, borte, dato in kamper_L:
    if "Panama" in [hjemme, borte]:
        motst = borte if hjemme == "Panama" else hjemme
        print(f"  vs {motst:15} - {dato}")

print("\n" + "=" * 60)
print("ALLE LAG - KAMPOVERSIKT:")
print("=" * 60)
for team_name, _ in grupper['L']:
    print(f"\n{team_name}:")
    datoer = []
    for hjemme, borte, dato in kamper_L:
        if team_name in [hjemme, borte]:
            motst = borte if hjemme == team_name else hjemme
            datoer.append(dato)
            print(f"  vs {motst:15} - {dato}")
    
    # Sjekk for duplikater
    if len(datoer) != len(set(datoer)):
        print(f"  ❌ KONFLIKT: Spiller flere kamper samme dag!")
    else:
        print(f"  ✅ OK: Alle kamper på forskjellige dager")
