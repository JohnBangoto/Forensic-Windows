DESCRIPTION = "Processus en cours d'exécution (psutil)"

import psutil

def collect():
    processes = []
    for p in psutil.process_iter(['pid', 'name', 'cpu_percent', 'create_time']):
        try:
            processes.append(p.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return processes
