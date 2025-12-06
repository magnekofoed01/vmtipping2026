grupper = {
    'L': [('England', 'gb-eng'), ('Kroatia', 'hr'), ('Ghana', 'gh'), ('Panama', 'pa')]
}
gruppespill_datoer = {
    'L': ['2026-06-15', '2026-06-15', '2026-06-18', '2026-06-18', '2026-06-27', '2026-06-27']
}

lag = grupper['L']
kamper = []

# Runde 1: Lag1 vs Lag2, Lag3 vs Lag4
kamper.append((lag[0][0], lag[1][0], gruppespill_datoer['L'][0]))
kamper.append((lag[2][0], lag[3][0], gruppespill_datoer['L'][1]))

# Runde 2: Lag1 vs Lag3, Lag2 vs Lag4
kamper.append((lag[0][0], lag[2][0], gruppespill_datoer['L'][2]))
kamper.append((lag[1][0], lag[3][0], gruppespill_datoer['L'][3]))

# Runde 3: Lag1 vs Lag4, Lag2 vs Lag3
kamper.append((lag[0][0], lag[3][0], gruppespill_datoer['L'][4]))
kamper.append((lag[1][0], lag[2][0], gruppespill_datoer['L'][5]))

print("Gruppe L kamper (ny rekkefølge):")
for i, (hjemme, borte, dato) in enumerate(kamper, 1):
    print(f"Kamp {i}: {hjemme} vs {borte} - {dato}")

print("\nHvert lag sine kamper:")
for team in lag:
    team_name = team[0]
    print(f"\n{team_name}:")
    for hjemme, borte, dato in kamper:
        if team_name in [hjemme, borte]:
            motst = borte if hjemme == team_name else hjemme
            print(f"  vs {motst} - {dato}")
