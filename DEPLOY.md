# 🚀 Deployment Guide - VM Tipping 2026

## 📋 Innholdsfortegnelse
- [Render.com (Anbefalt)](#rendercom-anbefalt)
- [Vercel](#vercel)
- [Heroku](#heroku)
- [PythonAnywhere](#pythonanywhere)

---

## 🎯 Render.com (Anbefalt)

Render tilbyr gratis hosting for Python Flask-apper med persistent database.

### Steg-for-steg:

1. **Opprett konto**
   - Gå til [render.com](https://render.com)
   - Registrer deg med GitHub

2. **Koble GitHub repository**
   - Klikk "New +" → "Web Service"
   - Velg ditt `vmtipping2026` repository

3. **Konfigurer service:**
   ```
   Name: vmtipping2026
   Environment: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: gunicorn app:app
   ```

4. **Legg til miljøvariabler (hvis nødvendig):**
   - Klikk "Environment"
   - Legg til eventuelle miljøvariabler

5. **Deploy**
   - Klikk "Create Web Service"
   - Vent på deployment (1-3 minutter)

6. **Database persistence:**
   - Render tilbyr gratis persistent disk
   - Gå til "Settings" → "Disks"
   - Legg til disk mounted til `/opt/render/project/src`

✅ **Resultat:** Din app vil være tilgjengelig på `https://vmtipping2026.onrender.com`

---

## ⚡ Vercel

Vercel er optimalisert for serverless deployment.

### Steg-for-steg:

1. **Installer Vercel CLI:**
   ```bash
   npm install -g vercel
   ```

2. **Deploy fra terminal:**
   ```bash
   cd VMTipping2026
   vercel
   ```

3. **Følg instruksjonene:**
   - Login med GitHub
   - Bekreft prosjektinnstillinger
   - Deploy

4. **Produksjonsdeploy:**
   ```bash
   vercel --prod
   ```

⚠️ **NB:** Vercel har serverless-arkitektur, så SQLite database vil bli tilbakestilt ved hver deploy. Vurder å bruke ekstern database som:
- [PlanetScale](https://planetscale.com/) (MySQL)
- [Supabase](https://supabase.com/) (PostgreSQL)
- [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)

---

## 🟣 Heroku

Heroku tilbyr enkel deployment, men krever betalingskort (selv for gratis tier).

### Steg-for-steg:

1. **Installer Heroku CLI:**
   - Last ned fra [heroku.com/cli](https://devcenter.heroku.com/articles/heroku-cli)

2. **Login:**
   ```bash
   heroku login
   ```

3. **Opprett app:**
   ```bash
   heroku create vmtipping2026
   ```

4. **Deploy:**
   ```bash
   git push heroku main
   ```

5. **Åpne app:**
   ```bash
   heroku open
   ```

📝 **Database addon:**
```bash
heroku addons:create heroku-postgresql:mini
```

---

## 🐍 PythonAnywhere

Gratis hosting spesielt for Python-applikasjoner.

### Steg-for-steg:

1. **Opprett konto**
   - Gå til [pythonanywhere.com](https://www.pythonanywhere.com)
   - Registrer gratis konto

2. **Last opp kode:**
   - Gå til "Files"
   - Last opp alle prosjektfiler

3. **Installer dependencies:**
   - Åpne "Bash console"
   ```bash
   pip3 install --user -r requirements.txt
   ```

4. **Konfigurer web app:**
   - Gå til "Web"
   - Legg til ny web app
   - Velg "Flask"
   - Pek til `app.py`

5. **Reload:**
   - Klikk "Reload" knappen

✅ **Resultat:** App tilgjengelig på `https://yourusername.pythonanywhere.com`

---

## 🔧 Feilsøking

### Port-problemer
Hvis appen ikke starter, endre `app.py`:
```python
if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
```

### Database-problemer
Sjekk at `tips.db` har riktige permissions:
```bash
chmod 664 tips.db
```

### Static files ikke lastes
Legg til i `app.py`:
```python
app.static_folder = 'static'
app.template_folder = 'templates'
```

---

## 📊 Sammenligning

| Platform | Gratis? | Database | Custom Domain | Oppsett |
|----------|---------|----------|---------------|---------|
| Render | ✅ Ja | Persistent disk | ✅ Ja | ⭐⭐⭐⭐⭐ |
| Vercel | ✅ Ja | Serverless* | ✅ Ja | ⭐⭐⭐⭐ |
| Heroku | ⚠️ Krever kort | PostgreSQL addon | ✅ Ja | ⭐⭐⭐⭐⭐ |
| PythonAnywhere | ✅ Ja | Persistent | ❌ Nei (gratis) | ⭐⭐⭐ |

*Serverless = Database resettes ved deploy

---

## 🎯 Anbefaling

For **VM Tipping 2026** anbefaler vi **Render.com** fordi:
- ✅ Helt gratis
- ✅ Persistent SQLite database
- ✅ Automatisk deployment fra GitHub
- ✅ Custom domain støtte
- ✅ Enkel oppsett

---

**Lykke til med deployingen! 🚀**
