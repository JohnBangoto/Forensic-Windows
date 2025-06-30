DESCRIPTION = "Sessions utilisateur actives (commande 'query user')"

import subprocess

def collect():
    try:
        result = subprocess.run(
            "query user",
            shell=True,
            capture_output=True,
            text=True,
            encoding='cp850',
            errors='replace'
        )
        if result.returncode == 0:
            return result.stdout.strip().splitlines()
        else:
            return [f"Erreur : {result.stderr.strip()}"]
    except Exception as e:
        return [f"Erreur lors de la collecte des sessions : {e}"]