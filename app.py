from flask import Flask, render_template, request, redirect, session, url_for
from functools import wraps
from werkzeug.security import check_password_hash
from dotenv import load_dotenv
import sqlite3, smtplib, os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'fallback_nokkel_bytt_meg')
ADMIN_PASSORD_HASH = os.environ.get('ADMIN_PASSORD_HASH', '')
SMTP_PASSORD = os.environ.get('SMTP_PASSORD', '')
SMTP_AVSENDER = os.environ.get('SMTP_AVSENDER', '')
DB_FILE = 'tips.db'

def krever_innlogging(f):
    @wraps(f)
    def dekorert(*args, **kwargs):
        if not session.get('admin_innlogget'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return dekorert

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS tips (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        navn TEXT, telefon TEXT, epost TEXT, kamp_id INTEGER,
        hjemmelag TEXT, bortelag TEXT, mål_hjemme INTEGER, mål_borte INTEGER, resultat TEXT
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS resultater (
        kamp_id INTEGER PRIMARY KEY, hjemmelag TEXT, bortelag TEXT,
        mål_hjemme INTEGER, mål_borte INTEGER, resultat TEXT, dato DATE
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS gruppefasit (
        gruppe TEXT, lag TEXT, plassering INTEGER, PRIMARY KEY (gruppe, lag)
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS gruppetips (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        navn TEXT, telefon TEXT, epost TEXT, gruppe TEXT, lag TEXT, plassering INTEGER
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS sluttspilltips (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        navn TEXT, telefon TEXT, epost TEXT, fase TEXT, lag TEXT
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS sluttspillfasit (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fase TEXT, lag TEXT, UNIQUE(fase, lag)
    )''')
    c.execute("PRAGMA table_info(resultater)")
    columns = [column[1] for column in c.fetchall()]
    if 'dato' not in columns:
        try:
            c.execute('ALTER TABLE resultater ADD COLUMN dato DATE')
        except Exception as e:
            print(f"⚠️ Kunne ikke legge til dato-kolonne: {e}")
    conn.commit()
    conn.close()

init_db()

flagg = {
    "Mexico": "mx", "Sør-Afrika": "za", "Sør-Korea": "kr", "Tsjekkia": "cz",
    "Canada": "ca", "Bosnia-Hercegovina": "ba", "Qatar": "qa", "Sveits": "ch",
    "Brasil": "br", "Marokko": "ma", "Haiti": "ht", "Skottland": "gb-sct",
    "USA": "us", "Paraguay": "py", "Australia": "au", "Tyrkia": "tr",
    "Tyskland": "de", "Curaçao": "cw", "Elfenbenskysten": "ci", "Ecuador": "ec",
    "Nederland": "nl", "Japan": "jp", "Sverige": "se", "Tunisia": "tn",
    "Belgia": "be", "Egypt": "eg", "Iran": "ir", "New Zealand": "nz",
    "Spania": "es", "Kapp Verde": "cv", "Saudi-Arabia": "sa", "Uruguay": "uy",
    "Frankrike": "fr", "Senegal": "sn", "Irak": "iq", "Norge": "no",
    "Argentina": "ar", "Algerie": "dz", "Østerrike": "at", "Jordan": "jo",
    "Portugal": "pt", "DR Kongo": "cd", "Usbekistan": "uz", "Colombia": "co",
    "England": "gb-eng", "Kroatia": "hr", "Ghana": "gh", "Panama": "pa"
}

grupper = {
    "A": ["Mexico", "Sør-Afrika", "Sør-Korea", "Tsjekkia"],
    "B": ["Canada", "Bosnia-Hercegovina", "Qatar", "Sveits"],
    "C": ["Brasil", "Marokko", "Haiti", "Skottland"],
    "D": ["USA", "Paraguay", "Australia", "Tyrkia"],
    "E": ["Tyskland", "Curaçao", "Elfenbenskysten", "Ecuador"],
    "F": ["Nederland", "Japan", "Sverige", "Tunisia"],
    "G": ["Belgia", "Egypt", "Iran", "New Zealand"],
    "H": ["Spania", "Kapp Verde", "Saudi-Arabia", "Uruguay"],
    "I": ["Frankrike", "Senegal", "Irak", "Norge"],
    "J": ["Argentina", "Algerie", "Østerrike", "Jordan"],
    "K": ["Portugal", "DR Kongo", "Usbekistan", "Colombia"],
    "L": ["England", "Kroatia", "Ghana", "Panama"]
}

grupper_med_flagg = {
    gruppe: [(lag, flagg.get(lag, "")) for lag in lag_liste]
    for gruppe, lag_liste in grupper.items()
}

kampdata = {
    ("Mexico", "Sør-Afrika"): "2026-06-11",
    ("Sør-Korea", "Tsjekkia"): "2026-06-12",
    ("Tsjekkia", "Sør-Afrika"): "2026-06-18",
    ("Mexico", "Sør-Korea"): "2026-06-19",
    ("Tsjekkia", "Mexico"): "2026-06-25",
    ("Sør-Afrika", "Sør-Korea"): "2026-06-25",
    ("Canada", "Bosnia-Hercegovina"): "2026-06-12",
    ("Qatar", "Sveits"): "2026-06-13",
    ("Sveits", "Bosnia-Hercegovina"): "2026-06-18",
    ("Canada", "Qatar"): "2026-06-19",
    ("Sveits", "Canada"): "2026-06-24",
    ("Bosnia-Hercegovina", "Qatar"): "2026-06-24",
    ("Brasil", "Marokko"): "2026-06-14",
    ("Haiti", "Skottland"): "2026-06-14",
    ("Skottland", "Marokko"): "2026-06-20",
    ("Brasil", "Haiti"): "2026-06-20",
    ("Skottland", "Brasil"): "2026-06-25",
    ("Marokko", "Haiti"): "2026-06-25",
    ("USA", "Paraguay"): "2026-06-13",
    ("Australia", "Tyrkia"): "2026-06-14",
    ("USA", "Australia"): "2026-06-19",
    ("Tyrkia", "Paraguay"): "2026-06-20",
    ("Tyrkia", "USA"): "2026-06-26",
    ("Paraguay", "Australia"): "2026-06-26",
    ("Tyskland", "Curaçao"): "2026-06-14",
    ("Elfenbenskysten", "Ecuador"): "2026-06-15",
    ("Tyskland", "Elfenbenskysten"): "2026-06-20",
    ("Ecuador", "Curaçao"): "2026-06-21",
    ("Curaçao", "Elfenbenskysten"): "2026-06-25",
    ("Ecuador", "Tyskland"): "2026-06-25",
    ("Nederland", "Japan"): "2026-06-14",
    ("Sverige", "Tunisia"): "2026-06-15",
    ("Nederland", "Sverige"): "2026-06-20",
    ("Tunisia", "Japan"): "2026-06-21",
    ("Japan", "Sverige"): "2026-06-26",
    ("Tunisia", "Nederland"): "2026-06-26",
    ("Belgia", "Egypt"): "2026-06-15",
    ("Iran", "New Zealand"): "2026-06-16",
    ("Belgia", "Iran"): "2026-06-21",
    ("New Zealand", "Egypt"): "2026-06-22",
    ("Egypt", "Iran"): "2026-06-27",
    ("New Zealand", "Belgia"): "2026-06-27",
    ("Spania", "Kapp Verde"): "2026-06-15",
    ("Saudi-Arabia", "Uruguay"): "2026-06-16",
    ("Spania", "Saudi-Arabia"): "2026-06-21",
    ("Uruguay", "Kapp Verde"): "2026-06-22",
    ("Kapp Verde", "Saudi-Arabia"): "2026-06-27",
    ("Uruguay", "Spania"): "2026-06-27",
    ("Frankrike", "Senegal"): "2026-06-16",
    ("Irak", "Norge"): "2026-06-17",
    ("Frankrike", "Irak"): "2026-06-22",
    ("Norge", "Senegal"): "2026-06-23",
    ("Norge", "Frankrike"): "2026-06-26",
    ("Senegal", "Irak"): "2026-06-26",
    ("Argentina", "Algerie"): "2026-06-17",
    ("Østerrike", "Jordan"): "2026-06-17",
    ("Argentina", "Østerrike"): "2026-06-22",
    ("Jordan", "Algerie"): "2026-06-23",
    ("Jordan", "Argentina"): "2026-06-28",
    ("Algerie", "Østerrike"): "2026-06-28",
    ("Portugal", "DR Kongo"): "2026-06-17",
    ("Usbekistan", "Colombia"): "2026-06-18",
    ("Portugal", "Usbekistan"): "2026-06-23",
    ("Colombia", "DR Kongo"): "2026-06-24",
    ("Colombia", "Portugal"): "2026-06-28",
    ("DR Kongo", "Usbekistan"): "2026-06-28",
    ("England", "Kroatia"): "2026-06-17",
    ("Ghana", "Panama"): "2026-06-18",
    ("England", "Ghana"): "2026-06-23",
    ("Panama", "Kroatia"): "2026-06-24",
    ("Panama", "England"): "2026-06-27",
    ("Kroatia", "Ghana"): "2026-06-27",
}

sluttspill_datoer = {
    "8-delsfinale": [
        "2026-07-04",  # Kamp 1: Houston
        "2026-07-04",  # Kamp 2: Philadelphia
        "2026-07-05",  # Kamp 3: New York
        "2026-07-06",  # Kamp 4: Mexico City
        "2026-07-06",  # Kamp 5: Dallas
        "2026-07-07",  # Kamp 6: Seattle
        "2026-07-07",  # Kamp 7: Atlanta
        "2026-07-07",  # Kamp 8: Vancouver
    ],
    "Kvartfinale": ["2026-07-09", "2026-07-10", "2026-07-11", "2026-07-12"],
    "Semifinale": ["2026-07-14", "2026-07-15"],
    "Bronsefinale": ["2026-07-18"],
    "Finale": ["2026-07-19"],
}

sluttspill_datoer_tekst = {
    '8-delsfinale': '4. – 7. jul 2026',
    'Kvartfinale': '9. – 12. jul 2026',
    'Semifinale': '14. – 15. jul 2026 (TV2)',
    'Bronsefinale': '18. jul 2026 (NRK)',
    'Finale': '19. jul 2026 (NRK)',
}

kamper = []
kamp_id = 1

for gruppe_navn, lag in grupper.items():
    for i in range(len(lag)):
        for j in range(i + 1, len(lag)):
            h = lag[i]
            b = lag[j]
            dato = kampdata.get((h, b)) or kampdata.get((b, h))
            kamper.append({
                "id": kamp_id, "fase": "Gruppespill", "gruppe": gruppe_navn,
                "hjemmelag": (h, flagg.get(h, "")), "bortelag": (b, flagg.get(b, "")), "dato": dato
            })
            kamp_id += 1

for i in range(1, 9):
    kamper.append({
        "id": kamp_id, "fase": "8-delsfinale", "gruppe": None,
        "hjemmelag": f"8del_hjemme_{i}", "bortelag": f"8del_borte_{i}",
        "kamp_nr": i, "dato": sluttspill_datoer["8-delsfinale"][i-1]
    })
    kamp_id += 1

for i in range(1, 5):
    kamper.append({
        "id": kamp_id, "fase": "Kvartfinale", "gruppe": None,
        "hjemmelag": f"kvart_hjemme_{i}", "bortelag": f"kvart_borte_{i}",
        "kamp_nr": i, "dato": sluttspill_datoer["Kvartfinale"][i-1]
    })
    kamp_id += 1

for i in range(1, 3):
    kamper.append({
        "id": kamp_id, "fase": "Semifinale", "gruppe": None,
        "hjemmelag": f"semi_hjemme_{i}", "bortelag": f"semi_borte_{i}",
        "kamp_nr": i, "dato": sluttspill_datoer["Semifinale"][i-1]
    })
    kamp_id += 1

kamper.append({
    "id": kamp_id, "fase": "Bronsefinale", "gruppe": None,
    "hjemmelag": "bronse_hjemme", "bortelag": "bronse_borte",
    "kamp_nr": 1, "dato": sluttspill_datoer["Bronsefinale"][0]
})
kamp_id += 1

kamper.append({
    "id": kamp_id, "fase": "Finale", "gruppe": None,
    "hjemmelag": "finale_hjemme", "bortelag": "finale_borte",
    "kamp_nr": 1, "dato": sluttspill_datoer["Finale"][0]
})

# Sorter gruppespill-kamper på dato
kamper_gruppespill = [k for k in kamper if k['fase'] == 'Gruppespill']
kamper_andre = [k for k in kamper if k['fase'] != 'Gruppespill']
kamper_gruppespill.sort(key=lambda k: k.get('dato') or '9999')
kamper = kamper_gruppespill + kamper_andre

alle_lag = []
for lag_liste in grupper.values():
    alle_lag.extend(lag_liste)
sluttspill_alternativer = sorted(alle_lag)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        navn = request.form['navn']
        telefon = request.form['telefon']
        epost = request.form['epost']
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()

        for kamp in kamper:
            if kamp['fase'] != 'Gruppespill':
                continue
            mål_hjemme = request.form.get(f"home_{kamp['id']}")
            mål_borte = request.form.get(f"away_{kamp['id']}")
            resultat = request.form.get(f"result_{kamp['id']}")
            if mål_hjemme and mål_borte and resultat:
                hjemmelag = kamp['hjemmelag'][0] if isinstance(kamp['hjemmelag'], tuple) else kamp['hjemmelag']
                bortelag = kamp['bortelag'][0] if isinstance(kamp['bortelag'], tuple) else kamp['bortelag']
                c.execute('INSERT INTO tips (navn, telefon, epost, kamp_id, hjemmelag, bortelag, mål_hjemme, mål_borte, resultat) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
                          (navn, telefon, epost, kamp['id'], hjemmelag, bortelag, mål_hjemme, mål_borte, resultat))

        for gruppe_navn, lag_liste in grupper.items():
            for lag in lag_liste:
                plassering = request.form.get(f"gruppe_{gruppe_navn}_{lag}")
                if plassering:
                    c.execute('INSERT INTO gruppetips (navn, telefon, epost, gruppe, lag, plassering) VALUES (?, ?, ?, ?, ?, ?)',
                              (navn, telefon, epost, gruppe_navn, lag, int(plassering)))

        fase_antall = {'8-delsfinale': 16, 'Kvartfinale': 8, 'Semifinale': 4, 'Bronsefinale': 2, 'Finale': 2, 'Vinner': 1}
        for fase, antall in fase_antall.items():
            for i in range(antall):
                lag = request.form.get(f"sluttspill_{fase}_{i}")
                if lag:
                    c.execute('INSERT INTO sluttspilltips (navn, telefon, epost, fase, lag) VALUES (?, ?, ?, ?, ?)',
                              (navn, telefon, epost, fase, lag))

        conn.commit()
        conn.close()
        return redirect('/')
    # Beregn foreslåtte 8-delsfinale-kandidater basert på gruppetips
    # VM 2026: De to beste fra hver gruppe (24 lag) + 8 beste tredjeplasser = 32 lag
    forslag_8del = []
    # Hent vinnere og toere fra alle grupper (fra grupper-dict, ingen fasit ennå)
    for g in sorted(grupper.keys()):
        lag = grupper[g]
        if len(lag) >= 2:
            forslag_8del.append(f"Vinner gr. {g} ({lag[0]}?)")
            forslag_8del.append(f"Toer gr. {g} ({lag[1]}?)")
    # Legg til 8 plasser for beste tredjeplasser
    for i in range(1, 9):
        forslag_8del.append(f"Beste 3.plass {i}")
    return render_template('index.html', kamper=kamper, grupper=grupper,
                           sluttspill_alternativer=sluttspill_alternativer,
                           forslag_8del=forslag_8del)


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
        tips_formatert = [{'kamp_id': t[0], 'hjemmelag': t[1], 'bortelag': t[2],
                           'mål_hjemme': t[3], 'mål_borte': t[4], 'resultat': t[5]} for t in tips]

        c.execute('SELECT fase, lag FROM sluttspilltips WHERE navn=? AND telefon=? AND epost=? ORDER BY fase',
                  (navn, telefon, epost))
        sluttspill = {}
        for fase, lag in c.fetchall():
            if fase not in sluttspill:
                sluttspill[fase] = []
            sluttspill[fase].append(lag)

        deltaker_liste.append({'navn': navn, 'telefon': telefon, 'epost': epost,
                               'tips': tips_formatert, 'sluttspilltips': sluttspill})
    conn.close()
    return render_template('deltakere.html', deltakere=deltaker_liste)


@app.route('/fasit')
def fasit():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('SELECT kamp_id, hjemmelag, bortelag, mål_hjemme, mål_borte, resultat, dato FROM resultater ORDER BY dato ASC, kamp_id ASC')
    resultater_data = c.fetchall()
    c.execute('SELECT fase, lag FROM sluttspillfasit ORDER BY fase')
    sluttspill_fasit = {}
    for fase, lag in c.fetchall():
        if fase not in sluttspill_fasit:
            sluttspill_fasit[fase] = []
        sluttspill_fasit[fase].append(lag)
    conn.close()
    fasit_liste = []
    hjemmeseire = uavgjort = borteseire = totalt_mål = 0
    for kamp_id, hjemmelag, bortelag, mål_hjemme, mål_borte, resultat, dato in resultater_data:
        fasit_liste.append({'kamp_id': kamp_id, 'hjemmelag': hjemmelag, 'bortelag': bortelag,
                            'mål_hjemme': mål_hjemme, 'mål_borte': mål_borte, 'resultat': resultat, 'dato': dato})
        if resultat == 'H': hjemmeseire += 1
        elif resultat == 'U': uavgjort += 1
        elif resultat == 'B': borteseire += 1
        totalt_mål += mål_hjemme + mål_borte
    statistikk = {'hjemmeseire': hjemmeseire, 'uavgjort': uavgjort, 'borteseire': borteseire,
                  'totalt_mål': totalt_mål, 'gjennomsnitt_mål': totalt_mål / len(fasit_liste) if fasit_liste else 0}
    return render_template('fasit.html', fasit=fasit_liste, statistikk=statistikk,
                           sluttspill_fasit=sluttspill_fasit,
                           sluttspill_datoer_tekst=sluttspill_datoer_tekst)


@app.route('/dagsvinner')
def dagsvinner():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('SELECT DISTINCT dato FROM resultater WHERE dato IS NOT NULL ORDER BY dato DESC')
    datoer = [row[0] for row in c.fetchall()]
    dagsvinnere = []
    for dato in datoer:
        c.execute('SELECT kamp_id, mål_hjemme, mål_borte, resultat FROM resultater WHERE dato = ?', (dato,))
        dagens_kamper = {row[0]: {"mål_hjemme": row[1], "mål_borte": row[2], "resultat": row[3]} for row in c.fetchall()}
        if not dagens_kamper:
            continue
        c.execute('SELECT navn, telefon, epost, kamp_id, mål_hjemme, mål_borte, resultat FROM tips')
        tips_data = c.fetchall()
        bruker_poeng = {}
        for navn, telefon, epost, kamp_id, mål_hjemme, mål_borte, resultat in tips_data:
            if kamp_id in dagens_kamper:
                key = (navn, telefon, epost)
                if key not in bruker_poeng:
                    bruker_poeng[key] = 0
                res = dagens_kamper[kamp_id]
                poeng = 0
                if resultat == res['resultat']: poeng += 1
                if int(mål_hjemme) == res['mål_hjemme'] and int(mål_borte) == res['mål_borte']: poeng += 2
                elif int(mål_hjemme) == res['mål_hjemme'] or int(mål_borte) == res['mål_borte']: poeng += 1
                bruker_poeng[key] += poeng
        if bruker_poeng:
            max_poeng = max(bruker_poeng.values())
            vinnere = [(n, t, e, p) for (n, t, e), p in bruker_poeng.items() if p == max_poeng]
            dagsvinnere.append({'dato': dato, 'antall_kamper': len(dagens_kamper), 'vinnere': vinnere, 'max_poeng': max_poeng})
    conn.close()
    return render_template('dagsvinner.html', dagsvinnere=dagsvinnere)


@app.route('/administrer', methods=['GET', 'POST'])
@krever_innlogging
def administrer():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    melding = None
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'slett_tips':
            navn = request.form.get('navn')
            telefon = request.form.get('telefon')
            epost = request.form.get('epost')
            if navn and telefon and epost:
                c.execute('DELETE FROM tips WHERE navn=? AND telefon=? AND epost=?', (navn, telefon, epost))
                c.execute('DELETE FROM gruppetips WHERE navn=? AND telefon=? AND epost=?', (navn, telefon, epost))
                c.execute('DELETE FROM sluttspilltips WHERE navn=? AND telefon=? AND epost=?', (navn, telefon, epost))
                conn.commit()
                melding = f"✅ Alle tips for {navn} er slettet!"
            else:
                melding = "❌ Mangler informasjon for å slette tips."
        elif action == 'slett_alle_tips':
            c.execute('DELETE FROM tips')
            c.execute('DELETE FROM gruppetips')
            c.execute('DELETE FROM sluttspilltips')
            conn.commit()
            melding = "✅ Alle tips er slettet!"
        elif action == 'slett_alle_resultater':
            c.execute('DELETE FROM resultater')
            c.execute('DELETE FROM gruppefasit')
            c.execute('DELETE FROM sluttspillfasit')
            conn.commit()
            melding = "✅ Alle resultater er slettet!"
    # Hent alle unike deltakere fra alle tre tabeller
    c.execute('''
        SELECT navn, telefon, epost FROM tips
        UNION
        SELECT navn, telefon, epost FROM gruppetips
        UNION
        SELECT navn, telefon, epost FROM sluttspilltips
        ORDER BY navn
    ''')
    alle = c.fetchall()
    deltakere_med_antall = []
    for navn, telefon, epost in alle:
        c.execute('SELECT COUNT(*) FROM tips WHERE navn=? AND telefon=? AND epost=?', (navn, telefon, epost))
        antall = c.fetchone()[0]
        deltakere_med_antall.append((navn, telefon, epost, antall))
    
    c.execute('SELECT COUNT(*) FROM tips')
    totalt_tips = c.fetchone()[0]
    c.execute('SELECT COUNT(*) FROM resultater')
    totalt_resultater = c.fetchone()[0]
    conn.close()
    return render_template('administrer.html', deltakere=deltakere_med_antall, totalt_tips=totalt_tips,
                           totalt_resultater=totalt_resultater, melding=melding)


@app.route('/resultater', methods=['GET', 'POST'])
@krever_innlogging
def resultater():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    if request.method == 'POST':
        action = request.form.get('action', 'lagre')

        if action == 'slett_sluttspill':
            c.execute('DELETE FROM sluttspillfasit')
            conn.commit()
            conn.close()
            return redirect('/resultater')

        for kamp in kamper:
            mål_hjemme = request.form.get(f"res_home_{kamp['id']}")
            mål_borte = request.form.get(f"res_away_{kamp['id']}")
            resultat = request.form.get(f"res_result_{kamp['id']}")
            if mål_hjemme and mål_borte and resultat:
                hjemmelag = kamp['hjemmelag'][0] if isinstance(kamp['hjemmelag'], tuple) else kamp['hjemmelag']
                bortelag = kamp['bortelag'][0] if isinstance(kamp['bortelag'], tuple) else kamp['bortelag']
                dato = kamp.get('dato', None)
                c.execute('REPLACE INTO resultater (kamp_id, hjemmelag, bortelag, mål_hjemme, mål_borte, resultat, dato) VALUES (?, ?, ?, ?, ?, ?, ?)',
                          (kamp['id'], hjemmelag, bortelag, mål_hjemme, mål_borte, resultat, dato))

        # Sluttspillfasit - slett og sett inn på nytt for å støtte endringer
        fase_antall = {'8-delsfinale': 16, 'Kvartfinale': 8, 'Semifinale': 4, 'Bronsefinale': 2, 'Finale': 2, 'Vinner': 1}
        for fase in fase_antall:
            har_input = any(request.form.get(f"sluttspill_fasit_{fase}_{i}") for i in range(fase_antall[fase]))
            if har_input:
                c.execute('DELETE FROM sluttspillfasit WHERE fase = ?', (fase,))
                for i in range(fase_antall[fase]):
                    lag = request.form.get(f"sluttspill_fasit_{fase}_{i}")
                    if lag:
                        c.execute('INSERT OR IGNORE INTO sluttspillfasit (fase, lag) VALUES (?, ?)', (fase, lag))

        for gruppe_navn, lag_liste in grupper.items():
            for lag in lag_liste:
                plassering = request.form.get(f"fasit_{gruppe_navn}_{lag}")
                if plassering:
                    c.execute('REPLACE INTO gruppefasit (gruppe, lag, plassering) VALUES (?, ?, ?)',
                              (gruppe_navn, lag, int(plassering)))
        conn.commit()
        conn.close()
        return redirect('/resultater')

    c.execute('SELECT kamp_id, mål_hjemme, mål_borte, resultat, dato FROM resultater')
    eksisterende_resultater = {row[0]: {"mål_hjemme": row[1], "mål_borte": row[2], "resultat": row[3], "dato": row[4]} for row in c.fetchall()}
    c.execute('SELECT gruppe, lag, plassering FROM gruppefasit')
    eksisterende_gruppefasit = {}
    for gruppe, lag, plassering in c.fetchall():
        if gruppe not in eksisterende_gruppefasit:
            eksisterende_gruppefasit[gruppe] = {}
        eksisterende_gruppefasit[gruppe][lag] = plassering
    c.execute('SELECT fase, lag FROM sluttspillfasit')
    eksisterende_sluttspillfasit = {}
    for fase, lag in c.fetchall():
        if fase not in eksisterende_sluttspillfasit:
            eksisterende_sluttspillfasit[fase] = []
        eksisterende_sluttspillfasit[fase].append(lag)
    conn.close()
    return render_template('resultater.html', kamper=kamper, grupper=grupper_med_flagg,
                           eksisterende_resultater=eksisterende_resultater,
                           eksisterende_gruppefasit=eksisterende_gruppefasit,
                           eksisterende_sluttspillfasit=eksisterende_sluttspillfasit,
                           sluttspill_alternativer=sluttspill_alternativer)


@app.route('/poeng', methods=['GET', 'POST'])
def poeng():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('SELECT navn, telefon, epost, kamp_id, mål_hjemme, mål_borte, resultat FROM tips')
    tips_data = c.fetchall()
    c.execute('SELECT kamp_id, mål_hjemme, mål_borte, resultat FROM resultater')
    resultater_data = {row[0]: {"mål_hjemme": row[1], "mål_borte": row[2], "resultat": row[3]} for row in c.fetchall()}
    bruker_poeng = {}
    for navn, telefon, epost, kamp_id, mål_hjemme, mål_borte, resultat in tips_data:
        key = (navn, telefon, epost)
        if key not in bruker_poeng: bruker_poeng[key] = 0
        if kamp_id in resultater_data:
            res = resultater_data[kamp_id]
            poeng = 0
            if resultat == res['resultat']: poeng += 1
            if int(mål_hjemme) == res['mål_hjemme'] and int(mål_borte) == res['mål_borte']: poeng += 2
            elif int(mål_hjemme) == res['mål_hjemme'] or int(mål_borte) == res['mål_borte']: poeng += 1
            bruker_poeng[key] += poeng

    # Gruppetips poengberegning
    c.execute('SELECT gruppe, lag, plassering FROM gruppefasit')
    gruppefasit = {}
    for gruppe, lag, plassering in c.fetchall():
        if gruppe not in gruppefasit:
            gruppefasit[gruppe] = {}
        gruppefasit[gruppe][lag] = plassering

    c.execute('SELECT navn, telefon, epost, gruppe, lag, plassering FROM gruppetips')
    for navn, telefon, epost, gruppe, lag, plassering in c.fetchall():
        key = (navn, telefon, epost)
        if key not in bruker_poeng: bruker_poeng[key] = 0
        if gruppe in gruppefasit and lag in gruppefasit[gruppe]:
            fasit_plassering = gruppefasit[gruppe][lag]
            if fasit_plassering == plassering:
                bruker_poeng[key] += 2  # Riktig plassering i gruppe
            elif abs(fasit_plassering - plassering) == 1:
                bruker_poeng[key] += 1  # En plass unna

    c.execute('SELECT fase, lag FROM sluttspillfasit')
    sluttspill_fasit = {}
    for fase, lag in c.fetchall():
        if fase not in sluttspill_fasit: sluttspill_fasit[fase] = set()
        sluttspill_fasit[fase].add(lag)

    c.execute('SELECT navn, telefon, epost, fase, lag FROM sluttspilltips')
    for navn, telefon, epost, fase, lag in c.fetchall():
        key = (navn, telefon, epost)
        if key not in bruker_poeng: bruker_poeng[key] = 0
        if fase in sluttspill_fasit and lag in sluttspill_fasit[fase]:
            fase_poeng = {
                '8-delsfinale': 2,
                'Kvartfinale': 5,
                'Semifinale': 10,
                'Bronsefinale': 10,
                'Finale': 20,
                'Vinner': 25
            }
            bruker_poeng[key] += fase_poeng.get(fase, 2)

    conn.close()
    rangering = sorted(bruker_poeng.items(), key=lambda x: x[1], reverse=True)
    melding = None
    if request.method == 'POST':
        action = request.form.get('action', 'email')
        if action == 'export':
            try:
                filename = 'poengoversikt.html'
                html_content = generate_email_html(rangering)
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(html_content)
                melding = f"✅ Poengoversikt eksportert til {filename}!"
            except Exception as e:
                melding = f"❌ Feil ved eksportering: {str(e)}"
        else:
            status = send_email(rangering)
            melding = "✅ E-post er sendt!" if status else "❌ Kunne ikke sende e-post."
    return render_template('poeng.html', rangering=rangering, melding=melding)


def generate_email_html(rangering):
    html = '<html><body><h2>Poengoversikt - VM Tipping 2026</h2><table border="1"><tr><th>Plass</th><th>Navn</th><th>Poeng</th></tr>'
    for plass, ((navn, telefon, epost), poeng) in enumerate(rangering, 1):
        html += f'<tr><td>{plass}</td><td>{navn}</td><td>{poeng}</td></tr>'
    html += '</table></body></html>'
    return html


def send_email(rangering):
    sender = SMTP_AVSENDER
    password = SMTP_PASSORD
    subject = 'Oppdatert poengoversikt - VM Tipping'
    body = '<h2>Poengoversikt</h2><table border="1"><tr><th>Plass</th><th>Navn</th><th>Poeng</th></tr>'
    for plass, ((navn, telefon, epost), poeng) in enumerate(rangering, 1):
        body += f'<tr><td>{plass}</td><td>{navn}</td><td>{poeng}</td></tr>'
    body += '</table>'
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'html'))
    recipients = [epost for ((_, _, epost), _) in rangering if epost]
    if not recipients: return False
    msg['To'] = ', '.join(recipients)
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, timeout=10) as server:
            server.login(sender, password)
            server.sendmail(sender, recipients, msg.as_string())
        return True
    except:
        try:
            with smtplib.SMTP('smtp.gmail.com', 587, timeout=10) as server:
                server.starttls()
                server.login(sender, password)
                server.sendmail(sender, recipients, msg.as_string())
            return True
        except:
            return False


@app.route('/login', methods=['GET', 'POST'])
def login():  # ← SKAL IKKE ha @krever_innlogging her!
    feil = None
    if request.method == 'POST':
        passord = request.form.get('passord', '')
        if ADMIN_PASSORD_HASH and check_password_hash(ADMIN_PASSORD_HASH, passord):
            session['admin_innlogget'] = True
            return redirect(url_for('administrer'))
        else:
            feil = "❌ Feil passord"
    return render_template('admin_login.html', feil=feil)


@app.route('/logout')
def logout():
    session.pop('admin_innlogget', None)
    return redirect(url_for('index'))


if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)