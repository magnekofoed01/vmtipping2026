# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, redirect, session, send_from_directory
import sqlite3
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os

app = Flask(__name__)
app.secret_key = 'vm2026-super-secret-key-change-this-in-production'
DB_FILE = 'tips.db'

# Admin passord (endre dette til et sikkert passord)
ADMIN_PASSWORD = '2026tippingvm'

# ----------------------
# INITIALISER DATABASE
# ----------------------
def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS tips (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        navn TEXT,
        telefon TEXT,
        epost TEXT,
        kamp_id INTEGER,
        hjemmelag TEXT,
        bortelag TEXT,
        mål_hjemme INTEGER,
        mål_borte INTEGER,
        resultat TEXT
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS resultater (
        kamp_id INTEGER PRIMARY KEY,
        hjemmelag TEXT,
        bortelag TEXT,
        mål_hjemme INTEGER,
        mål_borte INTEGER,
        resultat TEXT,
        dato DATE
    )''')
    
    # Ny tabell for gruppetips
    c.execute('''CREATE TABLE IF NOT EXISTS gruppetips (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        navn TEXT,
        telefon TEXT,
        epost TEXT,
        gruppe TEXT,
        lag TEXT,
        plassering INTEGER
    )''')
    
    # Ny tabell for gruppefasit (endelig plassering)
    c.execute('''CREATE TABLE IF NOT EXISTS gruppefasit (
        gruppe TEXT,
        lag TEXT,
        plassering INTEGER,
        PRIMARY KEY (gruppe, lag)
    )''')
    
    # Sjekk om dato-kolonnen eksisterer, hvis ikke legg den til
    c.execute("PRAGMA table_info(resultater)")
    columns = [column[1] for column in c.fetchall()]
    if 'dato' not in columns:
        try:
            c.execute('ALTER TABLE resultater ADD COLUMN dato DATE')
            print("✅ Lagt til 'dato'-kolonne i resultater-tabellen")
        except Exception as e:
            print(f"⚠️ Kunne ikke legge til dato-kolonne: {e}")
    
    conn.commit()
    conn.close()

init_db()

# VM 2026 - 12 Grupper med 4 lag i hver gruppe (48 lag totalt)
# Reelle grupper fra FIFA-trekningen 5. desember 2025
# Format: (landsnavn, landskode for flagg)
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

# Generer alle gruppekamper (6 kamper per gruppe = 72 gruppekamper totalt)
# VM 2026 gruppespill: 12. juni - 27. juni 2026
# Offisielt kampoppsett fra FIFA med spesifikke datoer og rekkefølge
kamper = []
kamp_id = 1

# Definerer alle gruppekamper manuelt basert på offisielt VM-program
# Dette sikrer korrekte datoer og at ingen lag spiller 2 kamper samme dag

# GRUPPE A - 12/06, 16/06, 21/06
kamper.extend([
    {"id": kamp_id, "fase": "Gruppespill", "gruppe": "A", "hjemmelag": grupper["A"][0], "bortelag": grupper["A"][2], "dato": "2026-06-12"},  # Mexico vs Sør-Afrika
    {"id": kamp_id+1, "fase": "Gruppespill", "gruppe": "A", "hjemmelag": grupper["A"][1], "bortelag": grupper["A"][3], "dato": "2026-06-12"},  # Sør-Korea vs Vinner UEFA PO D
    {"id": kamp_id+2, "fase": "Gruppespill", "gruppe": "A", "hjemmelag": grupper["A"][0], "bortelag": grupper["A"][1], "dato": "2026-06-16"},
    {"id": kamp_id+3, "fase": "Gruppespill", "gruppe": "A", "hjemmelag": grupper["A"][2], "bortelag": grupper["A"][3], "dato": "2026-06-16"},
    {"id": kamp_id+4, "fase": "Gruppespill", "gruppe": "A", "hjemmelag": grupper["A"][0], "bortelag": grupper["A"][3], "dato": "2026-06-21"},
    {"id": kamp_id+5, "fase": "Gruppespill", "gruppe": "A", "hjemmelag": grupper["A"][1], "bortelag": grupper["A"][2], "dato": "2026-06-21"},
])
kamp_id += 6

# GRUPPE B - 12/06, 14/06, 17/06, 22/06
kamper.extend([
    {"id": kamp_id, "fase": "Gruppespill", "gruppe": "B", "hjemmelag": grupper["B"][0], "bortelag": grupper["B"][3], "dato": "2026-06-12"},  # Canada vs UEFA PO A
    {"id": kamp_id+1, "fase": "Gruppespill", "gruppe": "B", "hjemmelag": grupper["B"][1], "bortelag": grupper["B"][2], "dato": "2026-06-14"},  # Qatar vs Sveits
    {"id": kamp_id+2, "fase": "Gruppespill", "gruppe": "B", "hjemmelag": grupper["B"][0], "bortelag": grupper["B"][1], "dato": "2026-06-17"},
    {"id": kamp_id+3, "fase": "Gruppespill", "gruppe": "B", "hjemmelag": grupper["B"][2], "bortelag": grupper["B"][3], "dato": "2026-06-17"},
    {"id": kamp_id+4, "fase": "Gruppespill", "gruppe": "B", "hjemmelag": grupper["B"][0], "bortelag": grupper["B"][2], "dato": "2026-06-22"},
    {"id": kamp_id+5, "fase": "Gruppespill", "gruppe": "B", "hjemmelag": grupper["B"][1], "bortelag": grupper["B"][3], "dato": "2026-06-22"},
])
kamp_id += 6

# GRUPPE C - 13/06, 17/06, 22/06
kamper.extend([
    {"id": kamp_id, "fase": "Gruppespill", "gruppe": "C", "hjemmelag": grupper["C"][0], "bortelag": grupper["C"][2], "dato": "2026-06-13"},  # Brasil vs Marokko
    {"id": kamp_id+1, "fase": "Gruppespill", "gruppe": "C", "hjemmelag": grupper["C"][1], "bortelag": grupper["C"][3], "dato": "2026-06-13"},  # Haiti vs Skottland
    {"id": kamp_id+2, "fase": "Gruppespill", "gruppe": "C", "hjemmelag": grupper["C"][0], "bortelag": grupper["C"][1], "dato": "2026-06-17"},
    {"id": kamp_id+3, "fase": "Gruppespill", "gruppe": "C", "hjemmelag": grupper["C"][2], "bortelag": grupper["C"][3], "dato": "2026-06-17"},
    {"id": kamp_id+4, "fase": "Gruppespill", "gruppe": "C", "hjemmelag": grupper["C"][0], "bortelag": grupper["C"][3], "dato": "2026-06-22"},
    {"id": kamp_id+5, "fase": "Gruppespill", "gruppe": "C", "hjemmelag": grupper["C"][1], "bortelag": grupper["C"][2], "dato": "2026-06-22"},
])
kamp_id += 6

# GRUPPE D - 13/06, 14/06, 18/06, 23/06
kamper.extend([
    {"id": kamp_id, "fase": "Gruppespill", "gruppe": "D", "hjemmelag": grupper["D"][0], "bortelag": grupper["D"][2], "dato": "2026-06-13"},  # USA vs Paraguay
    {"id": kamp_id+1, "fase": "Gruppespill", "gruppe": "D", "hjemmelag": grupper["D"][1], "bortelag": grupper["D"][3], "dato": "2026-06-14"},  # Australia vs Vinner UEFA PO C
    {"id": kamp_id+2, "fase": "Gruppespill", "gruppe": "D", "hjemmelag": grupper["D"][0], "bortelag": grupper["D"][1], "dato": "2026-06-18"},
    {"id": kamp_id+3, "fase": "Gruppespill", "gruppe": "D", "hjemmelag": grupper["D"][2], "bortelag": grupper["D"][3], "dato": "2026-06-18"},
    {"id": kamp_id+4, "fase": "Gruppespill", "gruppe": "D", "hjemmelag": grupper["D"][0], "bortelag": grupper["D"][3], "dato": "2026-06-23"},
    {"id": kamp_id+5, "fase": "Gruppespill", "gruppe": "D", "hjemmelag": grupper["D"][1], "bortelag": grupper["D"][2], "dato": "2026-06-23"},
])
kamp_id += 6

# GRUPPE E - 14/06, 18/06, 23/06
kamper.extend([
    {"id": kamp_id, "fase": "Gruppespill", "gruppe": "E", "hjemmelag": grupper["E"][2], "bortelag": grupper["E"][3], "dato": "2026-06-14"},  # Elfenbenskysten vs Ecuador
    {"id": kamp_id+1, "fase": "Gruppespill", "gruppe": "E", "hjemmelag": grupper["E"][0], "bortelag": grupper["E"][1], "dato": "2026-06-14"},  # Tyskland vs Curaçao
    {"id": kamp_id+2, "fase": "Gruppespill", "gruppe": "E", "hjemmelag": grupper["E"][0], "bortelag": grupper["E"][2], "dato": "2026-06-18"},
    {"id": kamp_id+3, "fase": "Gruppespill", "gruppe": "E", "hjemmelag": grupper["E"][1], "bortelag": grupper["E"][3], "dato": "2026-06-18"},
    {"id": kamp_id+4, "fase": "Gruppespill", "gruppe": "E", "hjemmelag": grupper["E"][0], "bortelag": grupper["E"][3], "dato": "2026-06-23"},
    {"id": kamp_id+5, "fase": "Gruppespill", "gruppe": "E", "hjemmelag": grupper["E"][1], "bortelag": grupper["E"][2], "dato": "2026-06-23"},
])
kamp_id += 6

# GRUPPE F - 14/06, 19/06, 24/06
kamper.extend([
    {"id": kamp_id, "fase": "Gruppespill", "gruppe": "F", "hjemmelag": grupper["F"][2], "bortelag": grupper["F"][3], "dato": "2026-06-14"},  # UEFA PO B vs Tunisia
    {"id": kamp_id+1, "fase": "Gruppespill", "gruppe": "F", "hjemmelag": grupper["F"][0], "bortelag": grupper["F"][1], "dato": "2026-06-14"},  # Nederland vs Japan
    {"id": kamp_id+2, "fase": "Gruppespill", "gruppe": "F", "hjemmelag": grupper["F"][0], "bortelag": grupper["F"][1], "dato": "2026-06-19"},
    {"id": kamp_id+3, "fase": "Gruppespill", "gruppe": "F", "hjemmelag": grupper["F"][2], "bortelag": grupper["F"][3], "dato": "2026-06-19"},
    {"id": kamp_id+4, "fase": "Gruppespill", "gruppe": "F", "hjemmelag": grupper["F"][0], "bortelag": grupper["F"][3], "dato": "2026-06-24"},
    {"id": kamp_id+5, "fase": "Gruppespill", "gruppe": "F", "hjemmelag": grupper["F"][1], "bortelag": grupper["F"][2], "dato": "2026-06-24"},
])
kamp_id += 6

# GRUPPE G - 15/06, 19/06, 24/06
kamper.extend([
    {"id": kamp_id, "fase": "Gruppespill", "gruppe": "G", "hjemmelag": grupper["G"][2], "bortelag": grupper["G"][3], "dato": "2026-06-15"},  # Iran vs New Zealand
    {"id": kamp_id+1, "fase": "Gruppespill", "gruppe": "G", "hjemmelag": grupper["G"][0], "bortelag": grupper["G"][1], "dato": "2026-06-15"},  # Belgia vs Egypt
    {"id": kamp_id+2, "fase": "Gruppespill", "gruppe": "G", "hjemmelag": grupper["G"][0], "bortelag": grupper["G"][2], "dato": "2026-06-19"},
    {"id": kamp_id+3, "fase": "Gruppespill", "gruppe": "G", "hjemmelag": grupper["G"][1], "bortelag": grupper["G"][3], "dato": "2026-06-19"},
    {"id": kamp_id+4, "fase": "Gruppespill", "gruppe": "G", "hjemmelag": grupper["G"][0], "bortelag": grupper["G"][3], "dato": "2026-06-24"},
    {"id": kamp_id+5, "fase": "Gruppespill", "gruppe": "G", "hjemmelag": grupper["G"][1], "bortelag": grupper["G"][2], "dato": "2026-06-24"},
])
kamp_id += 6

# GRUPPE H - 15/06, 20/06, 25/06
kamper.extend([
    {"id": kamp_id, "fase": "Gruppespill", "gruppe": "H", "hjemmelag": grupper["H"][2], "bortelag": grupper["H"][3], "dato": "2026-06-15"},  # Saudi-Arabia vs Uruguay
    {"id": kamp_id+1, "fase": "Gruppespill", "gruppe": "H", "hjemmelag": grupper["H"][0], "bortelag": grupper["H"][1], "dato": "2026-06-15"},  # Spania vs Kapp Verde
    {"id": kamp_id+2, "fase": "Gruppespill", "gruppe": "H", "hjemmelag": grupper["H"][0], "bortelag": grupper["H"][1], "dato": "2026-06-20"},
    {"id": kamp_id+3, "fase": "Gruppespill", "gruppe": "H", "hjemmelag": grupper["H"][2], "bortelag": grupper["H"][3], "dato": "2026-06-20"},
    {"id": kamp_id+4, "fase": "Gruppespill", "gruppe": "H", "hjemmelag": grupper["H"][0], "bortelag": grupper["H"][2], "dato": "2026-06-25"},
    {"id": kamp_id+5, "fase": "Gruppespill", "gruppe": "H", "hjemmelag": grupper["H"][1], "bortelag": grupper["H"][3], "dato": "2026-06-25"},
])
kamp_id += 6

# GRUPPE I - 16/06, 20/06, 25/06
kamper.extend([
    {"id": kamp_id, "fase": "Gruppespill", "gruppe": "I", "hjemmelag": grupper["I"][3], "bortelag": grupper["I"][2], "dato": "2026-06-16"},  # FIFA PO 2 vs Norge
    {"id": kamp_id+1, "fase": "Gruppespill", "gruppe": "I", "hjemmelag": grupper["I"][0], "bortelag": grupper["I"][1], "dato": "2026-06-16"},  # Frankrike vs Senegal
    {"id": kamp_id+2, "fase": "Gruppespill", "gruppe": "I", "hjemmelag": grupper["I"][0], "bortelag": grupper["I"][3], "dato": "2026-06-20"},
    {"id": kamp_id+3, "fase": "Gruppespill", "gruppe": "I", "hjemmelag": grupper["I"][1], "bortelag": grupper["I"][2], "dato": "2026-06-20"},
    {"id": kamp_id+4, "fase": "Gruppespill", "gruppe": "I", "hjemmelag": grupper["I"][0], "bortelag": grupper["I"][2], "dato": "2026-06-25"},
    {"id": kamp_id+5, "fase": "Gruppespill", "gruppe": "I", "hjemmelag": grupper["I"][3], "bortelag": grupper["I"][1], "dato": "2026-06-25"},
])
kamp_id += 6

# GRUPPE J - 16/06, 21/06, 26/06
kamper.extend([
    {"id": kamp_id, "fase": "Gruppespill", "gruppe": "J", "hjemmelag": grupper["J"][1], "bortelag": grupper["J"][3], "dato": "2026-06-16"},  # Østerrike vs Jordan
    {"id": kamp_id+1, "fase": "Gruppespill", "gruppe": "J", "hjemmelag": grupper["J"][0], "bortelag": grupper["J"][2], "dato": "2026-06-16"},  # Argentina vs Algerie
    {"id": kamp_id+2, "fase": "Gruppespill", "gruppe": "J", "hjemmelag": grupper["J"][0], "bortelag": grupper["J"][1], "dato": "2026-06-21"},
    {"id": kamp_id+3, "fase": "Gruppespill", "gruppe": "J", "hjemmelag": grupper["J"][2], "bortelag": grupper["J"][3], "dato": "2026-06-21"},
    {"id": kamp_id+4, "fase": "Gruppespill", "gruppe": "J", "hjemmelag": grupper["J"][0], "bortelag": grupper["J"][3], "dato": "2026-06-26"},
    {"id": kamp_id+5, "fase": "Gruppespill", "gruppe": "J", "hjemmelag": grupper["J"][1], "bortelag": grupper["J"][2], "dato": "2026-06-26"},
])
kamp_id += 6

# GRUPPE K - 17/06, 21/06, 26/06
kamper.extend([
    {"id": kamp_id, "fase": "Gruppespill", "gruppe": "K", "hjemmelag": grupper["K"][2], "bortelag": grupper["K"][3], "dato": "2026-06-17"},  # Usbekistan vs Colombia
    {"id": kamp_id+1, "fase": "Gruppespill", "gruppe": "K", "hjemmelag": grupper["K"][0], "bortelag": grupper["K"][1], "dato": "2026-06-17"},  # Portugal vs Vinner FIFA PO 1
    {"id": kamp_id+2, "fase": "Gruppespill", "gruppe": "K", "hjemmelag": grupper["K"][0], "bortelag": grupper["K"][2], "dato": "2026-06-21"},
    {"id": kamp_id+3, "fase": "Gruppespill", "gruppe": "K", "hjemmelag": grupper["K"][1], "bortelag": grupper["K"][3], "dato": "2026-06-21"},
    {"id": kamp_id+4, "fase": "Gruppespill", "gruppe": "K", "hjemmelag": grupper["K"][0], "bortelag": grupper["K"][3], "dato": "2026-06-26"},
    {"id": kamp_id+5, "fase": "Gruppespill", "gruppe": "K", "hjemmelag": grupper["K"][1], "bortelag": grupper["K"][2], "dato": "2026-06-26"},
])
kamp_id += 6

# GRUPPE L - 17/06, 21/06, 27/06
kamper.extend([
    {"id": kamp_id, "fase": "Gruppespill", "gruppe": "L", "hjemmelag": grupper["L"][0], "bortelag": grupper["L"][1], "dato": "2026-06-17"},  # England vs Kroatia
    {"id": kamp_id+1, "fase": "Gruppespill", "gruppe": "L", "hjemmelag": grupper["L"][2], "bortelag": grupper["L"][3], "dato": "2026-06-17"},  # Ghana vs Panama
    {"id": kamp_id+2, "fase": "Gruppespill", "gruppe": "L", "hjemmelag": grupper["L"][0], "bortelag": grupper["L"][2], "dato": "2026-06-21"},
    {"id": kamp_id+3, "fase": "Gruppespill", "gruppe": "L", "hjemmelag": grupper["L"][1], "bortelag": grupper["L"][3], "dato": "2026-06-21"},
    {"id": kamp_id+4, "fase": "Gruppespill", "gruppe": "L", "hjemmelag": grupper["L"][0], "bortelag": grupper["L"][3], "dato": "2026-06-27"},
    {"id": kamp_id+5, "fase": "Gruppespill", "gruppe": "L", "hjemmelag": grupper["L"][1], "bortelag": grupper["L"][2], "dato": "2026-06-27"},
])
kamp_id += 6

# ----------------------
# LOGIN OG SIKKERHET
# ----------------------
def check_admin():
    """Sjekk om brukeren er logget inn som admin"""
    return session.get('admin_logged_in', False)

@app.route('/admin-login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        password = request.form.get('password')
        if password == ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            return redirect(request.args.get('next') or '/administrer')
        else:
            return render_template('admin_login.html', error='Feil passord')
    return render_template('admin_login.html')

@app.route('/admin-logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    return redirect('/')

# SLUTTSPILL - Knockout-runder
# 16-delsfinale (32 lag, 16 kamper)
# De to beste fra hver gruppe (24 lag) + 8 beste tredjeplasser = 32 lag
sluttspill_16delsfinale = [
    "Vinner A", "Toer B", "Vinner C", "Toer D", "Vinner E", "Toer F", "Vinner G", "Toer H",
    "Vinner I", "Toer J", "Vinner K", "Toer L", "Toer A", "Vinner B", "Toer C", "Vinner D",
    "Toer E", "Vinner F", "Toer G", "Vinner H", "Toer I", "Vinner J", "Toer K", "Vinner L",
    "3.plass A/B/C", "3.plass D/E/F", "3.plass G/H/I", "3.plass J/K/L",
    "3.plass A/D/G", "3.plass B/E/H", "3.plass C/F/I", "3.plass best"
]

# 16-delsfinale (16 kamper)
for i in range(0, 32, 2):
    kamper.append({
        "id": kamp_id,
        "fase": "16-delsfinale",
        "gruppe": None,
        "hjemmelag": sluttspill_16delsfinale[i],
        "bortelag": sluttspill_16delsfinale[i + 1]
    })
    kamp_id += 1

# 8-delsfinale / Åttedelsfinale (8 kamper)
for i in range(1, 9):
    kamper.append({
        "id": kamp_id,
        "fase": "8-delsfinale",
        "gruppe": None,
        "hjemmelag": f"Vinner 16-delsfinale {i*2-1}",
        "bortelag": f"Vinner 16-delsfinale {i*2}"
    })
    kamp_id += 1

# Kvartfinale (4 kamper)
for i in range(1, 5):
    kamper.append({
        "id": kamp_id,
        "fase": "Kvartfinale",
        "gruppe": None,
        "hjemmelag": f"Vinner 8-delsfinale {i*2-1}",
        "bortelag": f"Vinner 8-delsfinale {i*2}"
    })
    kamp_id += 1

# Semifinale (2 kamper)
kamper.append({
    "id": kamp_id,
    "fase": "Semifinale",
    "gruppe": None,
    "hjemmelag": "Vinner Kvartfinale 1",
    "bortelag": "Vinner Kvartfinale 2"
})
kamp_id += 1

kamper.append({
    "id": kamp_id,
    "fase": "Semifinale",
    "gruppe": None,
    "hjemmelag": "Vinner Kvartfinale 3",
    "bortelag": "Vinner Kvartfinale 4"
})
kamp_id += 1

# Bronsefinale (3.plass)
kamper.append({
    "id": kamp_id,
    "fase": "Bronsefinale",
    "gruppe": None,
    "hjemmelag": "Taper Semifinale 1",
    "bortelag": "Taper Semifinale 2"
})
kamp_id += 1

# Finale
kamper.append({
    "id": kamp_id,
    "fase": "Finale",
    "gruppe": None,
    "hjemmelag": "Vinner Semifinale 1",
    "bortelag": "Vinner Semifinale 2"
})

# Totalt: 72 gruppekamper + 16 (16-dels) + 8 (8-dels) + 4 (kvart) + 2 (semi) + 1 (bronze) + 1 (finale) = 104 kamper

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        navn = request.form['navn']
        telefon = request.form['telefon']
        epost = request.form['epost']
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        
        # Lagre kamptips
        for kamp in kamper:
            mål_hjemme = request.form.get(f"home_{kamp['id']}")
            mål_borte = request.form.get(f"away_{kamp['id']}")
            resultat = request.form.get(f"result_{kamp['id']}")
            if mål_hjemme and mål_borte and resultat:
                hjemmelag_navn = kamp['hjemmelag'][0] if isinstance(kamp['hjemmelag'], tuple) else kamp['hjemmelag']
                bortelag_navn = kamp['bortelag'][0] if isinstance(kamp['bortelag'], tuple) else kamp['bortelag']
                c.execute('INSERT INTO tips (navn, telefon, epost, kamp_id, hjemmelag, bortelag, mål_hjemme, mål_borte, resultat) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
                          (navn, telefon, epost, kamp['id'], hjemmelag_navn, bortelag_navn, mål_hjemme, mål_borte, resultat))
        
        # Slett eksisterende gruppetips for denne brukeren
        c.execute('DELETE FROM gruppetips WHERE navn=? AND telefon=? AND epost=?', 
                  (navn, telefon, epost))
        
        # Lagre gruppetips
        for gruppe_navn, lag_liste in grupper.items():
            for lag_tuple in lag_liste:
                lag_navn = lag_tuple[0]
                plassering = request.form.get(f"gruppe_{gruppe_navn}_{lag_navn}")
                if plassering:
                    c.execute('INSERT INTO gruppetips (navn, telefon, epost, gruppe, lag, plassering) VALUES (?, ?, ?, ?, ?, ?)',
                              (navn, telefon, epost, gruppe_navn, lag_navn, int(plassering)))
        
        conn.commit()
        conn.close()
        return redirect('/')
    return render_template('index.html', kamper=kamper, grupper=grupper)

@app.route('/regler')
def regler():
    return render_template('regler.html')

@app.route('/deltakere')
def deltakere():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('SELECT DISTINCT navn, telefon, epost FROM tips')
    unike_deltakere = c.fetchall()
    
    deltaker_liste = []
    for navn, telefon, epost in unike_deltakere:
        c.execute('SELECT kamp_id, hjemmelag, bortelag, mål_hjemme, mål_borte, resultat FROM tips WHERE navn=? AND telefon=? AND epost=?', 
                  (navn, telefon, epost))
        tips = c.fetchall()
        
        tips_formatert = []
        for kamp_id, hjemmelag, bortelag, mål_hjemme, mål_borte, resultat in tips:
            tips_formatert.append({
                'kamp_id': kamp_id,
                'hjemmelag': hjemmelag,
                'bortelag': bortelag,
                'mål_hjemme': mål_hjemme,
                'mål_borte': mål_borte,
                'resultat': resultat
            })
        
        deltaker_liste.append({
            'navn': navn,
            'telefon': telefon,
            'epost': epost,
            'tips': tips_formatert
        })
    
    conn.close()
    return render_template('deltakere.html', deltakere=deltaker_liste)

@app.route('/fasit')
def fasit():
    if not check_admin():
        return redirect('/admin-login?next=/fasit')
    
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('SELECT kamp_id, hjemmelag, bortelag, mål_hjemme, mål_borte, resultat FROM resultater ORDER BY kamp_id')
    resultater_data = c.fetchall()
    conn.close()
    
    fasit_liste = []
    hjemmeseire = 0
    uavgjort = 0
    borteseire = 0
    totalt_mål = 0
    
    for kamp_id, hjemmelag, bortelag, mål_hjemme, mål_borte, resultat in resultater_data:
        fasit_liste.append({
            'kamp_id': kamp_id,
            'hjemmelag': hjemmelag,
            'bortelag': bortelag,
            'mål_hjemme': mål_hjemme,
            'mål_borte': mål_borte,
            'resultat': resultat
        })
        
        # Beregn statistikk
        if resultat == 'H':
            hjemmeseire += 1
        elif resultat == 'U':
            uavgjort += 1
        elif resultat == 'B':
            borteseire += 1
        
        totalt_mål += mål_hjemme + mål_borte
    
    statistikk = {
        'hjemmeseire': hjemmeseire,
        'uavgjort': uavgjort,
        'borteseire': borteseire,
        'totalt_mål': totalt_mål,
        'gjennomsnitt_mål': totalt_mål / len(fasit_liste) if fasit_liste else 0
    }
    
    return render_template('fasit.html', fasit=fasit_liste, statistikk=statistikk)

@app.route('/dagsvinner')
def dagsvinner():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    
    # Hent alle unike datoer med resultater
    c.execute('SELECT DISTINCT dato FROM resultater WHERE dato IS NOT NULL ORDER BY dato DESC')
    datoer = [row[0] for row in c.fetchall()]
    
    dagsvinnere = []
    
    for dato in datoer:
        # Hent alle kamper for denne datoen
        c.execute('SELECT kamp_id, mål_hjemme, mål_borte, resultat FROM resultater WHERE dato = ?', (dato,))
        dagens_kamper = {row[0]: {"mål_hjemme": row[1], "mål_borte": row[2], "resultat": row[3]} for row in c.fetchall()}
        
        if not dagens_kamper:
            continue
        
        # Hent alle tips
        c.execute('SELECT navn, telefon, epost, kamp_id, mål_hjemme, mål_borte, resultat FROM tips')
        tips_data = c.fetchall()
        
        # Beregn poeng for hver bruker for dagens kamper
        bruker_poeng = {}
        for navn, telefon, epost, kamp_id, mål_hjemme, mål_borte, resultat in tips_data:
            if kamp_id in dagens_kamper:
                key = (navn, telefon, epost)
                if key not in bruker_poeng:
                    bruker_poeng[key] = 0
                
                res = dagens_kamper[kamp_id]
                poeng = 0
                
                # Poengberegning
                if resultat == res['resultat']:
                    poeng += 1
                if int(mål_hjemme) == res['mål_hjemme'] and int(mål_borte) == res['mål_borte']:
                    poeng += 2
                elif int(mål_hjemme) == res['mål_hjemme'] or int(mål_borte) == res['mål_borte']:
                    poeng += 1
                
                bruker_poeng[key] += poeng
        
        if bruker_poeng:
            # Finn dagsvinner (eller flere ved likt poengantall)
            max_poeng = max(bruker_poeng.values())
            vinnere = [(navn, telefon, epost, poeng) for (navn, telefon, epost), poeng in bruker_poeng.items() if poeng == max_poeng]
            
            dagsvinnere.append({
                'dato': dato,
                'antall_kamper': len(dagens_kamper),
                'vinnere': vinnere,
                'max_poeng': max_poeng
            })
    
    conn.close()
    return render_template('dagsvinner.html', dagsvinnere=dagsvinnere)

@app.route('/administrer', methods=['GET', 'POST'])
def administrer():
    if not check_admin():
        return redirect('/admin-login?next=/administrer')
    
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    
    melding = None
    
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'slett_tips':
            # Slett spesifikke tips basert på navn
            navn = request.form.get('navn')
            telefon = request.form.get('telefon')
            epost = request.form.get('epost')
            
            if navn and telefon and epost:
                c.execute('DELETE FROM tips WHERE navn=? AND telefon=? AND epost=?', (navn, telefon, epost))
                conn.commit()
                melding = f"✅ Alle tips for {navn} er slettet!"
            else:
                melding = "❌ Mangler informasjon for å slette tips."
        
        elif action == 'slett_alle_tips':
            # Slett alle tips
            c.execute('DELETE FROM tips')
            conn.commit()
            melding = "✅ Alle tips er slettet!"
        
        elif action == 'slett_alle_resultater':
            # Slett alle resultater
            c.execute('DELETE FROM resultater')
            conn.commit()
            melding = "✅ Alle resultater er slettet!"
    
    # Hent alle deltakere med antall tips
    c.execute('SELECT navn, telefon, epost, COUNT(*) as antall FROM tips GROUP BY navn, telefon, epost ORDER BY navn')
    deltakere = c.fetchall()
    
    # Hent total statistikk
    c.execute('SELECT COUNT(*) FROM tips')
    totalt_tips = c.fetchone()[0]
    
    c.execute('SELECT COUNT(*) FROM resultater')
    totalt_resultater = c.fetchone()[0]
    
    conn.close()
    
    return render_template('administrer.html', deltakere=deltakere, totalt_tips=totalt_tips, 
                          totalt_resultater=totalt_resultater, melding=melding)

@app.route('/resultater', methods=['GET', 'POST'])
def resultater():
    if not check_admin():
        return redirect('/admin-login?next=/resultater')
    
    if request.method == 'POST':
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        
        # Lagre kampresultater
        for kamp in kamper:
            mål_hjemme = request.form.get(f"res_home_{kamp['id']}")
            mål_borte = request.form.get(f"res_away_{kamp['id']}")
            resultat = request.form.get(f"res_result_{kamp['id']}")
            dato = request.form.get(f"res_date_{kamp['id']}")
            if mål_hjemme and mål_borte and resultat:
                hjemmelag_navn = kamp['hjemmelag'][0] if isinstance(kamp['hjemmelag'], tuple) else kamp['hjemmelag']
                bortelag_navn = kamp['bortelag'][0] if isinstance(kamp['bortelag'], tuple) else kamp['bortelag']
                c.execute('REPLACE INTO resultater (kamp_id, hjemmelag, bortelag, mål_hjemme, mål_borte, resultat, dato) VALUES (?, ?, ?, ?, ?, ?, ?)',
                          (kamp['id'], hjemmelag_navn, bortelag_navn, mål_hjemme, mål_borte, resultat, dato))
        
        # Lagre gruppefasit
        for gruppe_navn, lag_liste in grupper.items():
            for lag_tuple in lag_liste:
                lag_navn = lag_tuple[0]
                plassering = request.form.get(f"fasit_{gruppe_navn}_{lag_navn}")
                if plassering:
                    c.execute('REPLACE INTO gruppefasit (gruppe, lag, plassering) VALUES (?, ?, ?)',
                              (gruppe_navn, lag_navn, int(plassering)))
        
        conn.commit()
        conn.close()
        return redirect('/resultater')
    return render_template('resultater.html', kamper=kamper, grupper=grupper)

@app.route('/poeng', methods=['GET', 'POST'])
def poeng():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('SELECT navn, telefon, epost, kamp_id, mål_hjemme, mål_borte, resultat FROM tips')
    tips_data = c.fetchall()
    c.execute('SELECT kamp_id, mål_hjemme, mål_borte, resultat FROM resultater')
    resultater_data = {row[0]: {"mål_hjemme": row[1], "mål_borte": row[2], "resultat": row[3]} for row in c.fetchall()}
    
    # Hent gruppetips og fasit
    c.execute('SELECT navn, telefon, epost, gruppe, lag, plassering FROM gruppetips')
    gruppetips_data = c.fetchall()
    c.execute('SELECT gruppe, lag, plassering FROM gruppefasit')
    gruppefasit_data = c.fetchall()
    gruppefasit_dict = {(row[0], row[1]): row[2] for row in gruppefasit_data}
    
    conn.close()

    bruker_poeng = {}
    
    # Beregn poeng for kampresultater
    for navn, telefon, epost, kamp_id, mål_hjemme, mål_borte, resultat in tips_data:
        key = (navn, telefon, epost)
        if key not in bruker_poeng:
            bruker_poeng[key] = {"kamper": 0, "grupper": 0, "totalt": 0}
        if kamp_id in resultater_data:
            res = resultater_data[kamp_id]
            poeng = 0
            if resultat == res['resultat']:
                poeng += 1
            if int(mål_hjemme) == res['mål_hjemme'] and int(mål_borte) == res['mål_borte']:
                poeng += 2
            elif int(mål_hjemme) == res['mål_hjemme'] or int(mål_borte) == res['mål_borte']:
                poeng += 1
            bruker_poeng[key]["kamper"] += poeng
    
    # Beregn poeng for gruppetips
    for navn, telefon, epost, gruppe, lag, plassering in gruppetips_data:
        key = (navn, telefon, epost)
        if key not in bruker_poeng:
            bruker_poeng[key] = {"kamper": 0, "grupper": 0, "totalt": 0}
        
        if (gruppe, lag) in gruppefasit_dict:
            riktig_plassering = gruppefasit_dict[(gruppe, lag)]
            if plassering == riktig_plassering:
                # Riktig plassering gir 3 poeng
                bruker_poeng[key]["grupper"] += 3
    
    # Beregn totalt poeng
    for key in bruker_poeng:
        bruker_poeng[key]["totalt"] = bruker_poeng[key]["kamper"] + bruker_poeng[key]["grupper"]

    rangering = sorted(bruker_poeng.items(), key=lambda x: x[1]["totalt"], reverse=True)

    melding = None
    if request.method == 'POST':
        action = request.form.get('action', 'email')
        
        if action == 'export':
            # Eksporter til HTML fil
            try:
                filename = 'poengoversikt.html'
                html_content = generate_email_html(rangering)
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(html_content)
                melding = f"✅ Poengoversikt eksportert til {filename}! Du kan åpne filen og kopiere innholdet."
            except Exception as e:
                melding = f"❌ Feil ved eksportering: {str(e)}"
        else:
            # Prøv å sende e-post
            print("📧 Forsøker å sende e-post...")
            print(f"📊 Antall deltakere: {len(rangering)}")
            status = send_email(rangering)
            if status:
                melding = "✅ E-post er sendt til alle deltakere!"
            else:
                melding = "❌ Kunne ikke sende e-post. Prøv å eksportere i stedet."
    return render_template('poeng.html', rangering=rangering, melding=melding)

@app.route('/gruppetips', methods=['GET', 'POST'])
def gruppetips():
    if request.method == 'POST':
        navn = request.form['navn']
        telefon = request.form['telefon']
        epost = request.form['epost']
        
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        
        # Slett eksisterende gruppetips for denne brukeren
        c.execute('DELETE FROM gruppetips WHERE navn=? AND telefon=? AND epost=?', 
                  (navn, telefon, epost))
        
        # Lagre nye gruppetips
        for gruppe_navn, lag_liste in grupper.items():
            for lag in lag_liste:
                plassering = request.form.get(f"gruppe_{gruppe_navn}_{lag}")
                if plassering:
                    c.execute('INSERT INTO gruppetips (navn, telefon, epost, gruppe, lag, plassering) VALUES (?, ?, ?, ?, ?, ?)',
                              (navn, telefon, epost, gruppe_navn, lag, int(plassering)))
        
        conn.commit()
        conn.close()
        return redirect('/gruppetips')
    
    return render_template('gruppetips.html', grupper=grupper)



def generate_email_html(rangering):
    """Genererer HTML for e-post"""
    html = '''<!DOCTYPE html>
<html lang="no">
<head>
    <meta charset="UTF-8">
    <title>Poengoversikt - VM Tipping</title>
    <style>
        body { font-family: Arial, sans-serif; padding: 20px; }
        table { border-collapse: collapse; width: 100%; max-width: 600px; margin: 20px 0; }
        th, td { border: 1px solid #ddd; padding: 12px; text-align: left; }
        th { background-color: #4CAF50; color: white; }
        tr:nth-child(even) { background-color: #f2f2f2; }
        h2 { color: #333; }
    </style>
</head>
<body>
    <h2>Poengoversikt - VM Tipping 2026</h2>
    <table>
        <tr>
            <th>Plass</th>
            <th>Navn</th>
            <th>Kamper</th>
            <th>Grupper</th>
            <th>Totalt</th>
        </tr>
'''
    plass = 1
    for (navn, telefon, epost), poeng_dict in rangering:
        kamper = poeng_dict.get("kamper", 0)
        grupper_poeng = poeng_dict.get("grupper", 0)
        totalt = poeng_dict.get("totalt", 0)
        html += f'        <tr><td>{plass}</td><td>{navn}</td><td>{kamper}</td><td>{grupper_poeng}</td><td>{totalt}</td></tr>\n'
        plass += 1
    
    html += '''    </table>
    <p><em>Kamper: Poeng fra kampresultater | Grupper: Poeng fra gruppeplasseringer</em></p>
</body>
</html>'''
    return html

def send_email(rangering):
    sender = 'magne.kofoed@gmail.com'
    password = 'gpnb xbbf jhuk trzl'  # fra Google App-passord
    subject = 'Oppdatert poengoversikt - VM Tipping'

    body = '<h2>Poengoversikt</h2><table border="1"><tr><th>Plass</th><th>Navn</th><th>Kamper</th><th>Grupper</th><th>Totalt</th></tr>'
    plass = 1
    for (navn, telefon, epost), poeng_dict in rangering:
        kamper = poeng_dict.get("kamper", 0)
        grupper_poeng = poeng_dict.get("grupper", 0)
        totalt = poeng_dict.get("totalt", 0)
        body += f'<tr><td>{plass}</td><td>{navn}</td><td>{kamper}</td><td>{grupper_poeng}</td><td>{totalt}</td></tr>'
        plass += 1
    body += '</table><p><em>Kamper: Poeng fra kampresultater | Grupper: Poeng fra gruppeplasseringer</em></p>'

    msg = MIMEMultipart()
    msg['From'] = sender
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'html'))

    recipients = [epost for ((_, _, epost), _) in rangering if epost]
    print(f"📧 Mottakere: {recipients}")
    
    if not recipients:
        print("⚠️ Ingen mottakere funnet!")
        return False
    
    msg['To'] = ', '.join(recipients)

    # Prøv først port 465 (SSL)
    try:
        print("🔌 Prøver port 465 (SSL)...")
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, timeout=10) as server:
            print("🔐 Logger inn...")
            server.login(sender, password)
            print("📤 Sender e-post...")
            server.sendmail(sender, recipients, msg.as_string())
        print("✅ E-post sendt til:", recipients)
        return True
    except Exception as e1:
        print(f"❌ Port 465 feilet: {str(e1)}")
        
        # Prøv deretter port 587 (TLS)
        try:
            print("🔌 Prøver port 587 (TLS)...")
            with smtplib.SMTP('smtp.gmail.com', 587, timeout=10) as server:
                print("🔒 Starter TLS...")
                server.starttls()
                print("🔐 Logger inn...")
                server.login(sender, password)
                print("📤 Sender e-post...")
                server.sendmail(sender, recipients, msg.as_string())
            print("✅ E-post sendt til:", recipients)
            return True
        except Exception as e2:
            print(f"❌ Port 587 feilet: {str(e2)}")
            print("❌ Begge porter feilet. Bruk eksporter-funksjonen i stedet.")
            return False

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)