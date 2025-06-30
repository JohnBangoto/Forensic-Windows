DESCRIPTION = "Connexions réseau actives (psutil)"

import psutil

def collect():
    connections = []
    for conn in psutil.net_connections(kind='inet'):
        connections.append({
            "pid": conn.pid,
            "laddr": f"{conn.laddr.ip}:{conn.laddr.port}" if conn.laddr else "",
            "raddr": f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else "",
            "status": conn.status,
            "type": str(conn.type),
            "family": str(conn.family)
        })
    return connections
