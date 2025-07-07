DESCRIPTION = "Fichiers récemment exécutés (.lnk dans Recent)"

def collect():
    import os
    try:
        recent = os.path.expanduser("~\\AppData\\Roaming\\Microsoft\\Windows\\Recent")
        files = [f for f in os.listdir(recent) if f.endswith(".lnk")]
        return files
    except Exception as e:
        return [{"error": str(e)}]
