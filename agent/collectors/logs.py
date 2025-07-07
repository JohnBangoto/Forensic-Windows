DESCRIPTION = "Logs d'événements Windows (Security, derniers 50)"

import win32evtlog

def collect(limit=50):
    logs = []
    server = 'localhost'
    logtype = 'Security'
    try:
        hand = win32evtlog.OpenEventLog(server, logtype)
        total = win32evtlog.GetNumberOfEventLogRecords(hand)
        events = win32evtlog.ReadEventLog(hand, win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ, 0)
        for i, event in enumerate(events):
            if i >= limit:
                break
            logs.append({
                'TimeGenerated': event.TimeGenerated.Format(),
                'SourceName': event.SourceName,
                'EventID': event.EventID,
                'EventType': event.EventType
            })
    except Exception as e:
        logs.append({"error": str(e)})
    return logs
