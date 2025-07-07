# 🕵️‍♂️ Agent Forensics – Desktop Forensic Collector

**Agent Forensics** est une application d'investigation numérique (forensics) pour Windows, avec une interface graphique moderne (Tkinter) permettant :

✅ La **collecte automatisée d’artefacts système**  
✅ Une **authentification utilisateur** (email/mot de passe) via FastAPI  
✅ L’**enregistrement sécurisé** des sessions de collecte dans une base de données  
✅ L’**export et l’upload automatique** des résultats vers **Google Drive**

---

## 🚀 Fonctionnalités principales

- 🔐 Connexion / inscription des utilisateurs
- 🧰 Lancement unitaire ou multiple de collecteurs d’artefacts
- 💾 Export JSON automatique dans `%LOCALAPPDATA%\AgentForensics\uploads\`
- ☁️ Téléversement des artefacts sur Google Drive
- 🗃️ Historisation des sessions dans une base MySQL via FastAPI
- 🖥️ Interface graphique moderne en `ttkbootstrap`

---

## 🧱 Structure du projet

```
.
├── agent/                          # Interface Tkinter (agent desktop)
│   ├── dashboard_view.py          # Vue principale avec collecte et analyse
│   ├── login_view.py              # Vue de connexion
│   ├── register_view.py           # Vue d'inscription
│   ├── app.py                     # Lancement de l'application Tkinter
│   └── server.py                  # Contient load_collectors / run_collector / upload_to_drive
│
├── backend/                       # Backend FastAPI (API REST)
│   ├── main.py                    # API endpoints
│   ├── auth.py                    # Logique de sécurité, hashing, DB
│   ├── database.py                # Connexion SQLAlchemy
│   ├── models.py                  # Modèles ORM SQLAlchemy
│   ├── schemas.py                 # Schémas Pydantic
│   └── requirements.txt
│
├── collectors/                    # Scripts de collecte (ex. usb.py, processes.py)
│
├── drive_uploader.py              # Upload Google Drive (via compte de service)
├── forensicsuploader-xxx.json     # Clé de service Google
└── README.md
```

---

## 🛠️ Installation

### Prérequis

- Python 3.10+
- Accès internet pour l’upload Google Drive

### 1. Installer les dépendances

```bash
# Pour le backend FastAPI
cd backend
pip install -r requirements.txt

# Pour l’interface desktop Tkinter
cd ../agent
pip install -r requirements.txt
```

### 2. Configurer la base de données

Lance ce script SQL dans MySQL :

```sql
CREATE DATABASE agent_forensics CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'forensics_user'@'localhost' IDENTIFIED BY 'Password';
GRANT ALL PRIVILEGES ON agent_forensics.* TO 'forensics_user'@'localhost';
FLUSH PRIVILEGES;

USE agent_forensics;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE collection_sessions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    hostname VARCHAR(255) NOT NULL,
    `system` VARCHAR(100),
    collection_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    file_name VARCHAR(255) NOT NULL,
    file_path TEXT NOT NULL,
    uploaded_to_drive BOOLEAN DEFAULT FALSE,
    drive_url TEXT,
    error_count INT DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
```

---

## 🔐 Lancer le backend FastAPI

```bash
cd backend
uvicorn main:app --reload
```

API disponible sur : http://127.0.0.1:8000

---

## 🖥️ Lancer l’application Desktop

```bash
cd agent
python main.py
```

---

## 🧪 Collecteurs

Chaque script de collecte dans `collectors/` doit contenir :

```python
DESCRIPTION = "Collecte les ports USB montés"
def collect():
    return {"clé": "valeur"}
```

---

## ☁️ Upload Google Drive

1. Crée un compte de service Google Drive
2. Active l’API Drive
3. Télécharge `forensicsuploader-xxx.json`
4. Spécifie l’ID du dossier Drive dans `drive_uploader.py`

---

## 📂 Résultats & Logs

- JSON stockés dans : `%LOCALAPPDATA%\AgentForensics\uploads\`
- Logs dans : `%LOCALAPPDATA%\AgentForensics\agent_forensics.log`

---

## 👥 Auteurs

- Mohammedou Seydi  
- Ngueyanouba Jean  
- Aissatou Camara  
- Donald William Kodjo Evlo 
- Djibril Sanou Gueye  
- Ndack Bouya Diop
---

## 🧭 Roadmap

- [x] Authentification utilisateur
- [x] Historisation sessions
- [x] Upload JSON sur Drive
- [x] Dashboard graphique Tkinter
- [ ] Analyse automatique des artefacts collectés
- [ ] Génération de rapports PDF
- [ ] Création d’un exécutable `.exe` avec Inno Setup
