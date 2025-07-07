DESCRIPTION = "Hash SHA256 de fichiers système courants (exemple)"

import hashlib
import os

def hash_file(filepath):
    try:
        with open(filepath, 'rb') as f:
            return hashlib.sha256(f.read()).hexdigest()
    except Exception:
        return None

def collect(paths=None):
    # Par défaut, quelques fichiers système à hasher pour la démo
    if paths is None:
        paths = [
            os.path.expanduser('~/.bashrc'),
            os.path.expanduser('~/.profile'),
            os.path.expanduser('~/.zshrc'),
            os.path.expanduser('~/.gitconfig'),
        ]
    hashes = {}
    for path in paths:
        if os.path.isfile(path):
            hashes[path] = hash_file(path)
    return hashes
