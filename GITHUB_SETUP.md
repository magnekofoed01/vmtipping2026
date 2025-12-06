# 📝 GitHub Repository Setup Guide

## ✅ Lokalt repository er opprettet!

Alle filer er klare og committed lokalt. Nå må du opprette repositoryet på GitHub.

## 🚀 Steg-for-steg instruksjoner:

### 1. Opprett GitHub Repository

1. Gå til [github.com](https://github.com)
2. Logg inn med brukeren `magnekofoed01`
3. Klikk på **"+"** øverst til høyre → **"New repository"**

### 2. Konfigurer repository

Fyll inn følgende:
- **Repository name:** `vmtipping2026`
- **Description:** `⚽ VM Tipping 2026 - Flask-basert tippingsapplikasjon`
- **Visibility:** Public (eller Private hvis du ønsker)
- **⚠️ VIKTIG:** IKKE velg noen av disse:
  - ❌ Add a README file
  - ❌ Add .gitignore
  - ❌ Choose a license

Klikk **"Create repository"**

### 3. Push koden til GitHub

Etter at repositoryet er opprettet på GitHub, kjør denne kommandoen:

```powershell
cd c:\kildekode\VMTipping2026
git push -u origin main
```

### 4. Verifiser opplasting

Gå til: https://github.com/magnekofoed01/vmtipping2026

Du skal se alle filene:
- ✅ README.md (med beskrivelse og emojis)
- ✅ DEPLOY.md (deployment guide)
- ✅ app.py (Flask applikasjon)
- ✅ requirements.txt (dependencies)
- ✅ Procfile (Render/Heroku config)
- ✅ vercel.json (Vercel config)
- ✅ templates/ (HTML filer)
- ✅ tips.db (Database)

## 🎯 Neste steg: Deploy til produksjon

Når repositoryet er pushet til GitHub, følg **DEPLOY.md** for å deploye appen:

### Anbefalt: Render.com

1. Gå til [render.com](https://render.com)
2. Registrer deg med GitHub
3. Klikk "New +" → "Web Service"
4. Velg `vmtipping2026` repositoryet
5. Konfigurer:
   - **Name:** vmtipping2026
   - **Environment:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
6. Klikk "Create Web Service"

⏱️ Vent 2-3 minutter mens Render bygger og deployer appen.

✅ **Din app vil være live på:** `https://vmtipping2026.onrender.com`

## 📊 Hva er allerede gjort:

- ✅ Git repository initialisert
- ✅ Alle filer lagt til
- ✅ Initial commit laget
- ✅ Branch navngitt til `main`
- ✅ Remote origin konfigurert
- ✅ Deployment filer opprettet:
  - `requirements.txt` (Flask, Werkzeug, gunicorn)
  - `Procfile` (for Render/Heroku)
  - `runtime.txt` (Python 3.11.7)
  - `vercel.json` (for Vercel)
  - `.gitignore` (ekskluderer cache, env, etc.)
- ✅ `app.py` oppdatert for production (PORT environment variable)
- ✅ README.md laget med full dokumentasjon
- ✅ DEPLOY.md laget med deployment guider

## ⚠️ Kun ett steg igjen:

**Opprett repositoryet på GitHub** (følg steg 1-2 over), deretter:

```powershell
git push -u origin main
```

---

**Lykke til! 🚀⚽**
