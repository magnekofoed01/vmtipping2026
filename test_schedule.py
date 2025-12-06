grupper = {
    'L': [('England', 'gb-eng'), ('Kroatia', 'hr'), ('Ghana', 'gh'), ('Panama', 'pa')]
}
gruppespill_datoer = {
    'L': ['2026-06-15', '2026-06-15', '2026-06-18', '2026-06-18', '2026-06-27', '2026-06-27']
}

lag = grupper['L']
kamp_index = 0
print("Gruppe L kamper:")
for i in range(len(lag)):
    for j in range(i + 1, len(lag)):
        print(f'Kamp {kamp_index + 1}: {lag[i][0]} vs {lag[j][0]} - {gruppespill_datoer["L"][kamp_index]}')
        kamp_index += 1

# Sjekk Panama sine kamper
print("\nPanama sine kamper:")
for i in range(len(lag)):
    for j in range(i + 1, len(lag)):
        if 'Panama' in [lag[i][0], lag[j][0]]:
            kamp_index_temp = i * (len(lag) - 1) - (i * (i - 1)) // 2 + (j - i - 1)
            # Simplified: just count from start
            count = 0
            for x in range(len(lag)):
                for y in range(x + 1, len(lag)):
                    if x == i and y == j:
                        print(f'{lag[i][0]} vs {lag[j][0]} - {gruppespill_datoer["L"][count]}')
                        break
                    count += 1
