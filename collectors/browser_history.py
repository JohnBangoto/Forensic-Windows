DESCRIPTION = "Historique de navigation (Chrome, Firefox, Edge)"

def collect():
    from browser_history.browsers import Chrome, Firefox, Edge
    all_history = []
    for browser in [Chrome(), Firefox(), Edge()]:
        try:
            outputs = browser.history()
            for entry in outputs.histories:
                all_history.append({
                    "browser": browser.name,
                    "url": entry[1],
                    "timestamp": entry[0].isoformat()
                })
        except Exception as e:
            all_history.append({"browser": browser.name, "error": str(e)})
    return all_history
