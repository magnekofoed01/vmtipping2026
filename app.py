from flask import Flask, render_template, request, redirect
import sqlite3
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

app = Flask(__name__)
DB_FILE = 'tips.db'

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
grupper = {
    "A": ["USA", "England", "Japan", "Senegal"],
    "B": ["Mexico", "Frankrike", "Sør-Korea", "Marokko"],
    "C": ["Canada", "Spania", "Australia", "Egypt"],
    "D": ["Brasil", "Tyskland", "Iran", "Ghana"],
    "E": ["Argentina", "Nederland", "Qatar", "Tunisia"],
    "F": ["Portugal", "Belgia", "Saudi-Arabia", "Algerie"],
    "G": ["Norge", "Kroatia", "Jordan", "Kapp Verde"],
    "H": ["Uruguay", "Sveits", "Usbekistan", "Elfenbenskysten"],
    "I": ["Colombia", "Østerrike", "New Zealand", "Sør-Afrika"],
    "J": ["Ecuador", "Skottland", "Panama", "Haiti"],
    "K": ["Paraguay", "Curaçao", "Senegal", "Saudi-Arabia"],
    "L": ["Sveits", "Tunisia", "Jordan", "Ghana"]
}

# Generer alle gruppekamper (6 kamper per gruppe = 72 gruppekamper totalt)
# I hver gruppe med 4 lag: Lag1 vs Lag2, Lag1 vs Lag3, Lag1 vs Lag4, Lag2 vs Lag3, Lag2 vs Lag4, Lag3 vs Lag4
kamper = []
kamp_id = 1

for gruppe_navn, lag in grupper.items():
    # Generer alle kombinasjoner av kamper i gruppen
    for i in range(len(lag)):
        for j in range(i + 1, len(lag)):
            kamper.append({
                "id": kamp_id,
                "fase": "Gruppespill",
                "gruppe": gruppe_navn,
                "hjemmelag": lag[i],
                "bortelag": lag[j]
            })
            kamp_id += 1

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

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        navn = request.form['navn']
        telefon = request.form['telefon']
        epost = request.form['epost']
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        for kamp in kamper:
            mål_hjemme = request.form.get(f"home_{kamp['id']}")
            mål_borte = request.form.get(f"away_{kamp['id']}")
            resultat = request.form.get(f"result_{kamp['id']}")
            if mål_hjemme and mål_borte and resultat:
                c.execute('INSERT INTO tips (navn, telefon, epost, kamp_id, hjemmelag, bortelag, mål_hjemme, mål_borte, resultat) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
                          (navn, telefon, epost, kamp['id'], kamp['hjemmelag'], kamp['bortelag'], mål_hjemme, mål_borte, resultat))
        conn.commit()
        conn.close()
        return redirect('/')
    return render_template('index.html', kamper=kamper)

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
    if request.method == 'POST':
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        for kamp in kamper:
            mål_hjemme = request.form.get(f"res_home_{kamp['id']}")
            mål_borte = request.form.get(f"res_away_{kamp['id']}")
            resultat = request.form.get(f"res_result_{kamp['id']}")
            dato = request.form.get(f"res_date_{kamp['id']}")
            if mål_hjemme and mål_borte and resultat:
                c.execute('REPLACE INTO resultater (kamp_id, hjemmelag, bortelag, mål_hjemme, mål_borte, resultat, dato) VALUES (?, ?, ?, ?, ?, ?, ?)',
                          (kamp['id'], kamp['hjemmelag'], kamp['bortelag'], mål_hjemme, mål_borte, resultat, dato))
        conn.commit()
        conn.close()
        return redirect('/resultater')
    return render_template('resultater.html', kamper=kamper)

@app.route('/poeng', methods=['GET', 'POST'])
def poeng():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('SELECT navn, telefon, epost, kamp_id, mål_hjemme, mål_borte, resultat FROM tips')
    tips_data = c.fetchall()
    c.execute('SELECT kamp_id, mål_hjemme, mål_borte, resultat FROM resultater')
    resultater_data = {row[0]: {"mål_hjemme": row[1], "mål_borte": row[2], "resultat": row[3]} for row in c.fetchall()}
    conn.close()

    bruker_poeng = {}
    for navn, telefon, epost, kamp_id, mål_hjemme, mål_borte, resultat in tips_data:
        key = (navn, telefon, epost)
        if key not in bruker_poeng:
            bruker_poeng[key] = 0
        if kamp_id in resultater_data:
            res = resultater_data[kamp_id]
            poeng = 0
            if resultat == res['resultat']:
                poeng += 1
            if int(mål_hjemme) == res['mål_hjemme'] and int(mål_borte) == res['mål_borte']:
                poeng += 2
            elif int(mål_hjemme) == res['mål_hjemme'] or int(mål_borte) == res['mål_borte']:
                poeng += 1
            bruker_poeng[key] += poeng

    rangering = sorted(bruker_poeng.items(), key=lambda x: x[1], reverse=True)

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
            <th>Poeng</th>
        </tr>
'''
    plass = 1
    for (navn, telefon, epost), poeng in rangering:
        html += f'        <tr><td>{plass}</td><td>{navn}</td><td>{poeng}</td></tr>\n'
        plass += 1
    
    html += '''    </table>
    <p><em>Generert: ''' + str(rangering) + '''</em></p>
</body>
</html>'''
    return html

def send_email(rangering):
    sender = 'magne.kofoed@gmail.com'
    password = 'gpnb xbbf jhuk trzl'  # fra Google App-passord
    subject = 'Oppdatert poengoversikt - VM Tipping'

    body = '<h2>Poengoversikt</h2><table border="1"><tr><th>Plass</th><th>Navn</th><th>Poeng</th></tr>'
    plass = 1
    for (navn, telefon, epost), poeng in rangering:
        body += f'<tr><td>{plass}</td><td>{navn}</td><td>{poeng}</td></tr>'
        plass += 1
    body += '</table>'

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