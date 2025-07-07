from flask import Flask, request, jsonify, send_from_directory, render_template, redirect, url_for
from datetime import datetime
import os
import json
import importlib.util
import threading
import time
from pathlib import Path
from drive_uploader import upload_to_drive
import logging

app = Flask(__name__)

# Répertoire local accessible en écriture
base_dir = Path(os.getenv("LOCALAPPDATA") or Path.home()) / "AgentForensics"
UPLOAD_DIR = base_dir / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# Initialiser le logger
logging.basicConfig(
    filename=base_dir / "agent_forensics.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# État global de la collecte
collection_state = {
    "running": False,
    "progress": 0,
    "total": 0,
    "current_collector": None,
    "start_time": None,
    "results": {},
    "errors": []
}

collection_thread = None
stop_collection = False


def load_collectors():
    collectors = []
    collectors_dir = Path(__file__).parent / "collectors"

    for file in collectors_dir.glob("*.py"):
        if file.stem.startswith("__"):
            continue

        try:
            spec = importlib.util.spec_from_file_location(file.stem, file)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            description = getattr(module, "DESCRIPTION", f"Collecteur pour {file.stem}")
            collectors.append({
                "name": file.stem,
                "description": description
            })
        except Exception as e:
            logging.error(f"Erreur lors du chargement du collecteur {file}: {e}")

    return collectors


def run_collector(collector_name):
    try:
        module_path = Path(__file__).parent / "collectors" / f"{collector_name}.py"
        spec = importlib.util.spec_from_file_location(collector_name, module_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        if hasattr(module, "collect"):
            return module.collect()
        return {"error": f"Fonction collect() non trouvée dans {collector_name}"}
    except Exception as e:
        return {"error": str(e)}


def collection_worker(selected_collectors):
    global collection_state, stop_collection

    collection_state["running"] = True
    collection_state["progress"] = 0
    collection_state["total"] = len(selected_collectors)
    collection_state["start_time"] = time.time()
    collection_state["results"] = {}
    collection_state["errors"] = []

    artifacts = {
        "metadata": {
            "collection_date": datetime.now().isoformat(),
            "hostname": os.environ.get("COMPUTERNAME", "Unknown"),
            "total_artifacts": 0
        },
        "artefacts": {}
    }

    for collector in selected_collectors:
        if stop_collection:
            break

        collection_state["current_collector"] = collector

        try:
            result = run_collector(collector)
            if "error" in result:
                collection_state["errors"].append(f"{collector}: {result['error']}")
                collection_state["results"][collector] = "error"
            else:
                artifacts["artefacts"][collector] = result
                collection_state["results"][collector] = "success"
        except Exception as e:
            collection_state["errors"].append(f"{collector}: {str(e)}")
            collection_state["results"][collector] = "error"

        collection_state["progress"] += 1

    # Sauvegarder les résultats
    if not stop_collection:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"artefacts_{timestamp}.json"
        filepath = UPLOAD_DIR / filename

        artifacts["metadata"]["total_artifacts"] = sum(
            len(data) if isinstance(data, list) else 1
            for data in artifacts["artefacts"].values()
        )

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(artifacts, f, indent=4, ensure_ascii=False)

        logging.info(f"Fichier artefact sauvegardé à {filepath}")
        upload_to_drive(str(filepath))

    collection_state["running"] = False
    collection_state["current_collector"] = None
    stop_collection = False


@app.route("/")
def home():
    return render_template("dashboard.html")


@app.route("/api/collectors")
def get_collectors():
    collectors = load_collectors()
    return jsonify(collectors)


@app.route("/api/collection/start", methods=["POST"])
def start_collection():
    global collection_thread, stop_collection

    if collection_state["running"]:
        return jsonify({"error": "Une collecte est déjà en cours"}), 400

    data = request.get_json()
    if not data or "collectors" not in data:
        return jsonify({"error": "Liste des collecteurs manquante"}), 400

    selected_collectors = data["collectors"]
    if not selected_collectors:
        return jsonify({"error": "Aucun collecteur sélectionné"}), 400

    stop_collection = False
    collection_thread = threading.Thread(
        target=collection_worker,
        args=(selected_collectors,)
    )
    collection_thread.start()

    return jsonify({"status": "started"})


@app.route("/api/collection/stop", methods=["POST"])
def stop_collection_endpoint():
    global stop_collection

    if not collection_state["running"]:
        return jsonify({"error": "Aucune collecte en cours"}), 400

    stop_collection = True
    return jsonify({"status": "stopping"})


@app.route("/api/collection/status")
def get_collection_status():
    status = dict(collection_state)
    if status["start_time"]:
        status["elapsed_time"] = int(time.time() - status["start_time"])
    return jsonify(status)


@app.route("/api/files")
def list_files():
    files = [f.name for f in UPLOAD_DIR.glob("*.json")]
    return jsonify(sorted(files, reverse=True))


@app.route("/uploads/<path:filename>")
def uploaded_file(filename):
    return send_from_directory(UPLOAD_DIR, filename)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
