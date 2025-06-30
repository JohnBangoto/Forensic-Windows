DESCRIPTION = "Historique des messages Skype (10 derniers par utilisateur)"

import os
import sqlite3

def collect():
    skype_data = []
    appdata = os.getenv("APPDATA")
    skype_path = os.path.join(appdata, "Skype")

    if not os.path.exists(skype_path):
        return ["Skype non installé"]

    for user in os.listdir(skype_path):
        db_path = os.path.join(skype_path, user, "main.db")
        if os.path.exists(db_path):
            try:
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()
                cursor.execute("SELECT datetime(timestamp, 'unixepoch'), author, dialog_partner, body_xml FROM Messages ORDER BY timestamp DESC LIMIT 10")
                rows = cursor.fetchall()
                skype_data.append({"user": user, "messages": rows})
                conn.close()
            except Exception as e:
                skype_data.append({"user": user, "error": str(e)})

    return skype_data
