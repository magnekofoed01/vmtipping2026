"""
Sjekk gruppe E-K mot offisielt oppsett
"""

# Fra brukerens melding:
offisielt = """
14/06/2026
Gruppe E
Elfenbenskysten vs Ecuador
Tyskland vs Curaçao

Gruppe F
UEFA PO B vs Tunisia
Nederland vs Japan

15/06/2026
Gruppe G
Iran vs New Zealand
Belgia vs Egypt

Gruppe H
Saudi-Arabia vs Uruguay
Spania vs Kapp Verde

16/06/2026
Gruppe I
FIFA PO 2 vs Norge
Frankrike vs Senegal

Gruppe J
Østerrike vs Jordan
Argentina vs Algerie

17/06/2026
Gruppe K
Usbekistan vs Colombia
Portugal vs FIFA PO 1
"""

# Nåværende inndeling i app.py:
grupper = {
    "E": [("Tyskland", "de"), ("Curaçao", "cw"), ("Elfenbenskysten", "ci"), ("Ecuador", "ec")],
    "F": [("Nederland", "nl"), ("Japan", "jp"), ("UEFA PO B", None), ("Tunisia", "tn")],
    "G": [("Belgia", "be"), ("Egypt", "eg"), ("Iran", "ir"), ("New Zealand", "nz")],
    "H": [("Spania", "es"), ("Kapp Verde", "cv"), ("Saudi-Arabia", "sa"), ("Uruguay", "uy")],
    "I": [("Frankrike", "fr"), ("Senegal", "sn"), ("Norge", "no"), ("FIFA PO 2", None)],
    "J": [("Argentina", "ar"), ("Algerie", "dz"), ("Østerrike", "at"), ("Jordan", "jo")],
    "K": [("Portugal", "pt"), ("FIFA PO 1", None), ("Usbekistan", "uz"), ("Colombia", "co")],
}

print("ANALYSE AV GRUPPE E-K")
print("=" * 80)

# Gruppe E
print("\nGRUPPE E:")
print("Offisielt: Elfenbenskysten vs Ecuador, Tyskland vs Curaçao")
print("Nåværende: [0]=Tyskland, [1]=Curaçao, [2]=Elfenbenskysten, [3]=Ecuador")
print("Første kamp i kode: [2] vs [3] = Elfenbenskysten vs Ecuador ✅")
print("Andre kamp i kode: [0] vs [1] = Tyskland vs Curaçao ✅")
print("STATUS: ✅ OK")

# Gruppe F  
print("\nGRUPPE F:")
print("Offisielt: UEFA PO B vs Tunisia, Nederland vs Japan")
print("Nåværende: [0]=Nederland, [1]=Japan, [2]=UEFA PO B, [3]=Tunisia")
print("Første kamp i kode skal være: [2] vs [3] = UEFA PO B vs Tunisia")
print("Andre kamp i kode skal være: [0] vs [1] = Nederland vs Japan")
print("STATUS: Må sjekke koden...")

# Gruppe G
print("\nGRUPPE G:")
print("Offisielt: Iran vs New Zealand, Belgia vs Egypt")
print("Nåværende: [0]=Belgia, [1]=Egypt, [2]=Iran, [3]=New Zealand")
print("Første kamp skal være: [2] vs [3] = Iran vs New Zealand ✅")
print("Andre kamp skal være: [0] vs [1] = Belgia vs Egypt ✅")
print("STATUS: ✅ OK")

# Gruppe H
print("\nGRUPPE H:")
print("Offisielt: Saudi-Arabia vs Uruguay, Spania vs Kapp Verde")
print("Nåværende: [0]=Spania, [1]=Kapp Verde, [2]=Saudi-Arabia, [3]=Uruguay")
print("Første kamp skal være: [2] vs [3] = Saudi-Arabia vs Uruguay ✅")
print("Andre kamp skal være: [0] vs [1] = Spania vs Kapp Verde ✅")
print("STATUS: ✅ OK")

# Gruppe I
print("\nGRUPPE I:")
print("Offisielt: FIFA PO 2 vs Norge, Frankrike vs Senegal")
print("Nåværende: [0]=Frankrike, [1]=Senegal, [2]=Norge, [3]=FIFA PO 2")
print("Første kamp skal være: [3] vs [2] = FIFA PO 2 vs Norge ✅")
print("Andre kamp skal være: [0] vs [1] = Frankrike vs Senegal ✅")
print("STATUS: ✅ OK (allerede fikset)")

# Gruppe J
print("\nGRUPPE J:")
print("Offisielt: Østerrike vs Jordan, Argentina vs Algerie")
print("Nåværende: [0]=Argentina, [1]=Algerie, [2]=Østerrike, [3]=Jordan")
print("Første kamp skal være: [2] vs [3] = Østerrike vs Jordan ✅")
print("Andre kamp skal være: [0] vs [1] = Argentina vs Algerie ✅")
print("STATUS: ✅ OK")

# Gruppe K
print("\nGRUPPE K:")
print("Offisielt: Usbekistan vs Colombia, Portugal vs FIFA PO 1")
print("Nåværende: [0]=Portugal, [1]=FIFA PO 1, [2]=Usbekistan, [3]=Colombia")
print("Første kamp skal være: [2] vs [3] = Usbekistan vs Colombia ✅")
print("Andre kamp skal være: [0] vs [1] = Portugal vs FIFA PO 1 ✅")
print("STATUS: ✅ OK")

print("\n" + "=" * 80)
print("KONKLUSJON:")
print("Alle grupper E-K ser riktige ut i laginndeling.")
print("Må sjekke om kampene i app.py matcher dette.")
