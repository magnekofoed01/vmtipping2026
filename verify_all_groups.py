"""
Verifiser alle 12 grupper mot det offisielle VM 2026 kampoppsettet
"""

grupper = {
    "A": [("Mexico", "mx"), ("Sør-Afrika", "za"), ("Sør-Korea", "kr"), ("UEFA PO D", None)],
    "B": [("Canada", "ca"), ("Qatar", "qa"), ("Sveits", "ch"), ("UEFA PO A", None)],
    "C": [("Brasil", "br"), ("Marokko", "ma"), ("Haiti", "ht"), ("Skottland", "gb-sct")],
    "D": [("USA", "us"), ("Paraguay", "py"), ("Australia", "au"), ("UEFA PO C", None)],
    "E": [("Tyskland", "de"), ("Curaçao", "cw"), ("Elfenbenskysten", "ci"), ("Ecuador", "ec")],
    "F": [("Nederland", "nl"), ("Japan", "jp"), ("UEFA PO B", None), ("Tunisia", "tn")],
    "G": [("Belgia", "be"), ("Egypt", "eg"), ("Iran", "ir"), ("New Zealand", "nz")],
    "H": [("Spania", "es"), ("Kapp Verde", "cv"), ("Saudi-Arabia", "sa"), ("Uruguay", "uy")],
    "I": [("Frankrike", "fr"), ("Senegal", "sn"), ("Norge", "no"), ("FIFA PO 2", None)],
    "J": [("Argentina", "ar"), ("Algerie", "dz"), ("Østerrike", "at"), ("Jordan", "jo")],
    "K": [("Portugal", "pt"), ("FIFA PO 1", None), ("Usbekistan", "uz"), ("Colombia", "co")],
    "L": [("England", "gb-eng"), ("Kroatia", "hr"), ("Ghana", "gh"), ("Panama", "pa")]
}

# Offisielt kampoppsett fra FIFA
offisielle_kamper = {
    "A": [
        ("Mexico", "Sør-Afrika", "2026-06-12"),
        ("Sør-Korea", "UEFA PO D", "2026-06-12"),
    ],
    "B": [
        ("Canada", "UEFA PO A", "2026-06-12"),
        ("Qatar", "Sveits", "2026-06-14"),
    ],
    "C": [
        ("Brasil", "Marokko", "2026-06-13"),
        ("Haiti", "Skottland", "2026-06-13"),
    ],
    "D": [
        ("USA", "Paraguay", "2026-06-13"),
        ("Australia", "UEFA PO C", "2026-06-14"),
    ],
    "E": [
        ("Elfenbenskysten", "Ecuador", "2026-06-14"),
        ("Tyskland", "Curaçao", "2026-06-14"),
    ],
    "F": [
        ("UEFA PO B", "Tunisia", "2026-06-14"),
        ("Nederland", "Japan", "2026-06-14"),
    ],
    "G": [
        ("Iran", "New Zealand", "2026-06-15"),
        ("Belgia", "Egypt", "2026-06-15"),
    ],
    "H": [
        ("Saudi-Arabia", "Uruguay", "2026-06-15"),
        ("Spania", "Kapp Verde", "2026-06-15"),
    ],
    "I": [
        ("FIFA PO 2", "Norge", "2026-06-16"),
        ("Frankrike", "Senegal", "2026-06-16"),
    ],
    "J": [
        ("Østerrike", "Jordan", "2026-06-16"),
        ("Argentina", "Algerie", "2026-06-16"),
    ],
    "K": [
        ("Usbekistan", "Colombia", "2026-06-17"),
        ("Portugal", "FIFA PO 1", "2026-06-17"),
    ],
    "L": [
        ("England", "Kroatia", "2026-06-17"),
        ("Ghana", "Panama", "2026-06-17"),
    ]
}

def finn_lag_index(gruppe_navn, lag_navn):
    """Finn hvilket index et lag har i gruppen"""
    for i, (navn, code) in enumerate(grupper[gruppe_navn]):
        if navn == lag_navn:
            return i
    return None

print("=" * 80)
print("VERIFISERING AV ALLE GRUPPER MOT OFFISIELT VM 2026 KAMPOPPSETT")
print("=" * 80)

alle_ok = True

for gruppe_navn in ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L"]:
    print(f"\n{'='*80}")
    print(f"GRUPPE {gruppe_navn}")
    print(f"{'='*80}")
    
    # Vis laginndeling
    print(f"Laginndeling:")
    for i, (lag, code) in enumerate(grupper[gruppe_navn]):
        print(f"  [{i}] {lag}")
    
    # Sjekk første to kamper mot offisielt oppsett
    print(f"\nFørste kamper (offisielt oppsett):")
    gruppe_ok = True
    
    for kamp_nr, (hjemme_forventet, borte_forventet, dato) in enumerate(offisielle_kamper[gruppe_navn], 1):
        hjemme_idx = finn_lag_index(gruppe_navn, hjemme_forventet)
        borte_idx = finn_lag_index(gruppe_navn, borte_forventet)
        
        print(f"  Kamp {kamp_nr}: {hjemme_forventet:20} vs {borte_forventet:20} ({dato})")
        
        if hjemme_idx is None:
            print(f"    ❌ FEIL: {hjemme_forventet} finnes ikke i gruppe {gruppe_navn}!")
            gruppe_ok = False
            alle_ok = False
        else:
            print(f"    ✓ {hjemme_forventet} er lag [{hjemme_idx}]")
            
        if borte_idx is None:
            print(f"    ❌ FEIL: {borte_forventet} finnes ikke i gruppe {gruppe_navn}!")
            gruppe_ok = False
            alle_ok = False
        else:
            print(f"    ✓ {borte_forventet} er lag [{borte_idx}]")
    
    if gruppe_ok:
        print(f"\n  ✅ Gruppe {gruppe_navn} OK")
    else:
        print(f"\n  ❌ Gruppe {gruppe_navn} HAR FEIL!")

print(f"\n{'='*80}")
if alle_ok:
    print("✅ ALLE GRUPPER ER KORREKTE!")
else:
    print("❌ NOEN GRUPPER HAR FEIL - SE DETALJER OVER")
print(f"{'='*80}")
