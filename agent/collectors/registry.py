DESCRIPTION = "Clés de registre sensibles (Run, RunOnce utilisateur)"

import winreg

def collect():
    keys = {
        "Run": r"Software\Microsoft\Windows\CurrentVersion\Run",
        "RunOnce": r"Software\Microsoft\Windows\CurrentVersion\RunOnce"
    }

    results = {}
    for name, path in keys.items():
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, path) as key:
                entries = {}
                for i in range(winreg.QueryInfoKey(key)[1]):
                    value_name, value_data, _ = winreg.EnumValue(key, i)
                    entries[value_name] = value_data
                results[name] = entries
        except Exception as e:
            results[name] = str(e)
    return results
