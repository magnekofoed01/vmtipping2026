# ⚽ VM Tipping 2026

En Flask-basert tippingsapplikasjon for VM 2026 med kampresultater, poengberegning og rangeringer.

## 🎯 Funksjoner

- 📊 **Live resultater** - Følg alle kampene i VM 2026
- 🏆 **Poengberegning** - Automatisk beregning av poeng basert på tips
- 👥 **Deltakerliste** - Oversikt over alle som tipper
- 📈 **Rangeringsliste** - Se hvem som leder
- 🎖️ **Dagsvinner** - Premie til beste tipper hver dag
- ⚙️ **Administrasjon** - Enkel administrasjon av kamper og resultater

## 🌍 Gruppeoversikt VM 2026

| Gruppe | Lag |
|--------|-----|
| **A** | Mexico, Sør-Afrika, Sør-Korea, Tsjekkia |
| **B** | Canada, Bosnia-Hercegovina, Qatar, Sveits |
| **C** | Brasil, Marokko, Haiti, Skottland |
| **D** | USA, Paraguay, Australia, Tyrkia |
| **E** | Tyskland, Curaçao, Elfenbenskysten, Ecuador |
| **F** | Nederland, Japan, Sverige, Tunisia |
| **G** | Belgia, Egypt, Iran, New Zealand |
| **H** | Spania, Kapp Verde, Saudi-Arabia, Uruguay |
| **I** | Frankrike, Senegal, Irak, Norge |
| **J** | Argentina, Algerie, Østerrike, Jordan |
| **K** | Portugal, DR Kongo, Usbekistan, Colombia |
| **L** | England, Kroatia, Ghana, Panama |

## 🚀 Kom i gang

### Forutsetninger

- Python 3.8 eller nyere
- pip (Python package manager)

### Installasjon

1. **Klon repositoriet:**
```bash
git clone https://github.com/magnekofoed01/vmtipping2026.git
cd vmtipping2026
```

2. **Installer avhengigheter:**
```bash
pip install -r requirements.txt
```

3. **Kjør applikasjonen:**
```bash
python app.py
```

4. **Åpne i nettleser:**
```
http://localhost:5000
```

## 📁 Prosjektstruktur

```
VMTipping2026/
├── app.py                  # Hovedapplikasjon
├── templates/              # HTML-maler
│   ├── index.html         # Forside
│   ├── deltakere.html     # Deltakerside
│   ├── poeng.html         # Poengoversikt
│   ├── resultater.html    # Kampresultater
│   ├── fasit.html         # Fasit/resultater
│   ├── dagsvinner.html    # Daglige vinnere
│   ├── regler.html        # Regler
│   └── administrer.html   # Admin-side
├── tips.db                # SQLite database
├── requirements.txt       # Python-avhengigheter
└── README.md             # Denne filen
```

## 🎮 Bruk

### For deltakere:
1. Gå til forsiden
2. Velg ditt navn fra listen
3. Legg inn dine tips for kommende kamper
4. Følg med på poengstanden

### For administratorer:
1. Gå til `/administrer`
2. Legg inn kampresultater etter hvert som de kommer
3. Systemet beregner automatisk poeng

## 📊 Poengberegning

- **Riktig resultat**: 3 poeng
- **Riktig vinner/uavgjort**: 1 poeng
- **Feil**: 0 poeng

## 🛠️ Teknologi

- **Backend**: Python Flask
- **Database**: SQLite
- **Frontend**: HTML, CSS, JavaScript
- **Styling**: Bootstrap (hvis brukt)

## 🚀 Deploy til produksjon

### Render.com (Gratis)

1. Opprett konto på [Render.com](https://render.com)
2. Koble til GitHub-repositoriet
3. Sett opp som Web Service:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python app.py`

### Vercel

1. Installer Vercel CLI: `npm install -g vercel`
2. Kjør: `vercel`
3. Følg instruksjonene

## 📝 Lisens

Dette prosjektet er laget for privat bruk.

## 👨‍💻 Utvikler

Laget av Magne Kofoed

## 🤝 Bidra

Pull requests er velkomne! For større endringer, vennligst åpne et issue først.

---

**God tipping! ⚽🏆**
