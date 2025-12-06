# -*- coding: utf-8 -*-
# Test for å verifisere Curaçao matching

# Simuler hva som skjer i JavaScript
teams = ["Tyskland", "Curaçao", "Elfenbenskysten", "Ecuador"]

# Test cases - hva browser returnerer fra textContent
test_cases = [
    "Curaçao",
    "Curacao",
    " Curaçao ",
    "Curaçao ",
]

print("=== Testing Curaçao matching ===\n")

for test_input in test_cases:
    # Simuler JavaScript normalization
    normalized = test_input.replace('\xa0', ' ').strip()
    
    print(f"Input: '{test_input}' (len={len(test_input)})")
    print(f"Normalized: '{normalized}' (len={len(normalized)})")
    
    # Test exact match
    exact_match = normalized in teams
    print(f"Exact match: {exact_match}")
    
    # Test substring match
    substring_matches = []
    for team in teams:
        if normalized == team or normalized.lower().includes(team.lower()) or team.lower() in normalized.lower():
            substring_matches.append(team)
    
    print(f"Substring matches: {substring_matches}")
    print()

# Sjekk encoding
print("\n=== Character encoding check ===")
for team in teams:
    print(f"{team}: {[ord(c) for c in team]}")
