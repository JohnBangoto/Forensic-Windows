# Agent Forensics

**Agent Forensics** est un outil d'investigation numérique (forensics) conçu pour collecter automatiquement des artefacts système Windows via une interface web simple et intuitive.

## Fonctionnalités

* Collecte automatisée d’artefacts système (historique navigateur, processus, clés de registre, fichiers récents, etc.)
* Interface web locale accessible sur `http://localhost:5000`
* Lancement d'un ou de plusieurs collecteurs d'artefacts
* Export des résultats en JSON
* Téléversement automatique des artefacts vers Google Drive
* Journalisation des actions dans un fichier `.log`

## Structure du projet

```
.
├── collectors/                  # Modules de collecte (ex. : usb.py, processes.py, etc.)
├── templates/
│   └── dashboard.html           # Interface web
├── server.py                    # Serveur Flask (API REST)
├── drive_uploader.py            # Upload vers Google Drive
├── config.json                  # Configuration éventuelle
├── forensicsuploader-xxx.json   # Clé d'authentification Google
```

## Lancement

1. Installe les dépendances :

   ```bash
   pip install flask google-api-python-client google-auth google-auth-oauthlib
   ```

2. Lance le serveur :

   ```bash
   python server.py
   ```

3. Accède à l'interface via ton navigateur :

   ```
   http://localhost:5000
   ```

## Collecteurs

Les collecteurs sont placés dans le dossier `collectors/`. Chaque fichier doit contenir une fonction `collect()` qui retourne un dictionnaire d'artefacts. Exemple de nom : `usb.py`, `network.py`, etc.

## Téléversement vers Google Drive

* Configure ton fichier `forensicsuploader-xxx.json` (clé de compte de service Google).
* L'ID du dossier cible sur Drive est défini dans `drive_uploader.py`.

## Résultats

Les fichiers JSON sont stockés dans :

```
%LOCALAPPDATA%\AgentForensics\uploads\
```

Ils sont également automatiquement envoyés sur Google Drive.

## Logs

Un fichier `agent_forensics.log` est généré dans :

```
%LOCALAPPDATA%\AgentForensics\
```

## Auteurs

Aissatou Camara  
Donald William Evlo Kodjo  
Ngueyanouba Jean  
Mohammedou Seydi  
Djibril Sanou Gueye  



## À venir

* Intégration d'une interface graphique complète (`forensics_gui.py`)
* Mise en place de l'installateur (.exe) via Inno Setup

