DESCRIPTION = "Services Windows (sc query state=all)"

import subprocess

def collect():
    try:
        output = subprocess.check_output(
            "sc query state= all",
            shell=True,
            encoding='utf-8',
            errors='replace'
        )
        return output.splitlines()
    except Exception as e:
        return [str(e)]
