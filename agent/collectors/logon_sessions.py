DESCRIPTION = "Sessions de connexion utilisateur (commande 'query user')"

import subprocess

def collect():
    try:
        output = subprocess.check_output("query user", shell=True, text=True)
        # Retourne chaque ligne comme un élément de liste
        return [line for line in output.strip().split('\n')]
    except Exception as e:
        return [{"error": f"Erreur lors de la collecte des sessions : {e}"}]
