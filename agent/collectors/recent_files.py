DESCRIPTION = "Fichiers récemment ouverts (raccourcis .lnk dans Recent)"

import os
import glob

def collect():
    recent_files = []
    recent_path = os.path.expanduser("~\\AppData\\Roaming\\Microsoft\\Windows\\Recent")
    for lnk_file in glob.glob(os.path.join(recent_path, "*.lnk")):
        try:
            recent_files.append({
                "file": os.path.basename(lnk_file),
                "full_path": lnk_file
            })
        except Exception:
            continue
    return recent_files
