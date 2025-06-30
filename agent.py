import json
import requests
from datetime import datetime, timezone

from collectors.logs import get_event_logs
from collectors.processes import get_processes
from collectors.usb import get_usb_devices
from collectors.network import collect_network_connections
from collectors.browser_history import collect_browser_history
from collectors.installed_apps import collect_installed_apps
from collectors.recent_files import collect_recent_files
#from collectors.skype import collect_skype_activity
from collectors.registry import collect_sensitive_registry_keys
from collectors.logon_sessions import collect_logon_sessions
from collectors.executed_files import collect_executed_files
from collectors.file_hashes import collect_file_hashes
from collectors.services import collect_services


with open("config.json") as f:
    config = json.load(f)

data = {
    "machine_id": config["machine_id"],
    "timestamp": datetime.now(timezone.utc).isoformat(),
    "artefacts": {
        "logs": get_event_logs(),
        "processes": get_processes(),
        "usb": get_usb_devices(),
        "network_connections": collect_network_connections(),
        "browser_history": collect_browser_history(),
        "installed_apps": collect_installed_apps(),
        "recent_files": collect_recent_files(),
        #"skype_activity": collect_skype_activity(),
        "registry_keys": collect_sensitive_registry_keys(),
        "logon_sessions": collect_logon_sessions(),
        "executed_files": collect_executed_files(),
        "file_hashes": collect_file_hashes(["C:\\Users"]),
        "services": collect_services()

    }
}

try:
    response = requests.post(
        url=config["api_url"],
        headers={"Authorization": f"Bearer {config['auth_token']}"},
        json=data,
        timeout=10,
        verify=False
    )
    print("✅ Données envoyées :", response.status_code)
except Exception as e:
    print("❌ Erreur d'envoi :", str(e))
