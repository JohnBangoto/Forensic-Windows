import os
import json
import socket
import platform
import threading
from datetime import datetime
from pathlib import Path
import tkinter as tk
from tkinter import messagebox, filedialog

import requests
import ttkbootstrap as tb
from ttkbootstrap.constants import *

from server import load_collectors, run_collector, upload_to_drive

UPLOAD_DIR = Path(os.getenv("LOCALAPPDATA") or Path.home()) / "AgentForensics" / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


class StatusCard(tb.Frame):
    def __init__(self, parent, icon="", title="", value="", color="primary"):
        super().__init__(parent, bootstyle=color)
        self.configure(padding=10, relief="raised", borderwidth=1)

        self.icon_label = tb.Label(self, text=icon, font=("Segoe UI", 24))
        self.icon_label.pack(side=tk.LEFT, padx=10)

        right = tb.Frame(self)
        right.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        tb.Label(right, text=title, font=("Segoe UI", 10)).pack(anchor="w")
        self.value_label = tb.Label(right, text=value, font=("Segoe UI", 16, "bold"))
        self.value_label.pack(anchor="w")

    def update_value(self, new_value):
        self.value_label.config(text=new_value)


class DashboardView(tb.Frame):
    def __init__(self, parent, user_email, on_logout):
        super().__init__(parent)
        self.on_logout = on_logout
        self.user_email = user_email
        self.collectors = load_collectors()
        self.logs = []

        self.configure_styles()
        self.create_widgets()

    def configure_styles(self):
        style = tb.Style()
        style.configure("Sidebar.TFrame", background="#1e1e1e")
        style.configure("SidebarButton.TButton", font=("Segoe UI", 11))
        style.configure("Sidebar.TLabel", background="#1e1e1e", foreground="white")

    def create_widgets(self):
        container = self

        self.create_sidebar(container)
        self.content_area = tb.Frame(container)
        self.content_area.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.create_dashboard()
        self.create_collect()
        self.create_analysis()

        self.show_dashboard()

    def create_sidebar(self, parent):
        sidebar = tb.Frame(parent, style="Sidebar.TFrame", width=250)
        sidebar.pack(side=tk.LEFT, fill=tk.Y)
        sidebar.pack_propagate(False)

        tb.Label(sidebar, text="🔍", font=("Segoe UI", 32), style="Sidebar.TLabel").pack(pady=(20, 0))
        tb.Label(sidebar, text="Forensics", font=("Segoe UI", 14, "bold"), style="Sidebar.TLabel").pack()
        tb.Label(sidebar, text=self.user_email, font=("Segoe UI", 10), style="Sidebar.TLabel").pack(pady=(10, 0))

        nav = tb.Frame(sidebar, style="Sidebar.TFrame")
        nav.pack(pady=20)

        self.buttons = {}
        for txt, name in [("📊 Dashboard", "dashboard"), ("🚀 Collecte", "collect"), ("📈 Analyse", "analysis")]:
            btn = tb.Button(nav, text=txt, style="SidebarButton.TButton", command=lambda n=name: self.switch(n))
            btn.pack(fill=tk.X, pady=5, padx=10)
            self.buttons[name] = btn

        tb.Button(sidebar, text="🔓 Déconnexion", bootstyle="danger", command=self.logout).pack(side=tk.BOTTOM, pady=20)

    def logout(self):
        self.on_logout()

    def switch(self, name):
        for frame in [self.dashboard_frame, self.collect_frame, self.analysis_frame]:
            frame.pack_forget()
        if name == "dashboard":
            self.show_dashboard()
        elif name == "collect":
            self.show_collect()
        elif name == "analysis":
            self.show_analysis()

    def create_dashboard(self):
        self.dashboard_frame = tb.Frame(self.content_area)

        tb.Label(self.dashboard_frame, text=f"👤 Connecté en tant que : {self.user_email}", font=("Segoe UI", 10, "italic")).pack(anchor="ne", padx=10, pady=(5, 0))

        cards_frame = tb.Frame(self.dashboard_frame)
        cards_frame.pack(fill=tk.X, padx=10, pady=10)

        self.stat_cards = {
            "collectors": StatusCard(cards_frame, "🧰", "Collecteurs", str(len(self.collectors)), color="info"),
            "files": StatusCard(cards_frame, "📂", "Fichiers JSON", "0", color="success"),
            "errors": StatusCard(cards_frame, "⚠️", "Erreurs", "0", color="warning"),
        }

        for card in self.stat_cards.values():
            card.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        tb.Label(self.dashboard_frame, text="📝 Activité récente", font=("Segoe UI", 14, "bold")).pack(anchor="w", padx=10)
        self.activity_list = tb.ScrolledText(self.dashboard_frame, height=18)
        self.activity_list.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def create_collect(self):
        self.collect_frame = tb.Frame(self.content_area)
        tb.Label(self.collect_frame, text="🚀 Collecte d'Artefacts", font=("Segoe UI", 20, "bold")).pack(anchor="w", padx=10, pady=10)

        self.collector_vars = {}
        for c in self.collectors:
            var = tk.BooleanVar()
            cb = tb.Checkbutton(self.collect_frame, text=c["name"], variable=var, bootstyle="success-round-toggle")
            cb.pack(anchor="w", padx=20)
            self.collector_vars[c["name"]] = var

        tb.Button(self.collect_frame, text="Démarrer", bootstyle="primary", command=self.start_collection).pack(pady=10)

        self.log_box = tb.ScrolledText(self.collect_frame, height=12)
        self.log_box.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def create_analysis(self):
        self.analysis_frame = tb.Frame(self.content_area)
        tb.Label(self.analysis_frame, text="📈 Analyse", font=("Segoe UI", 20, "bold")).pack(anchor="w", padx=10, pady=10)

        tb.Button(self.analysis_frame, text="Charger Fichier", command=self.load_file).pack(pady=5)
        self.analysis_text = tk.Text(self.analysis_frame, wrap="none", font=("Consolas", 10))
        self.analysis_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def show_dashboard(self):
        self.dashboard_frame.pack(fill=tk.BOTH, expand=True)
        self.refresh_dashboard()

    def show_collect(self):
        self.collect_frame.pack(fill=tk.BOTH, expand=True)

    def show_analysis(self):
        self.analysis_frame.pack(fill=tk.BOTH, expand=True)

    def refresh_dashboard(self):
        files = list(UPLOAD_DIR.glob("*.json"))
        self.stat_cards["files"].update_value(str(len(files)))

        self.activity_list.delete("1.0", tk.END)
        for log in self.logs[-20:]:
            self.activity_list.insert(tk.END, log + "\n")

    def start_collection(self):
        selected = [name for name, var in self.collector_vars.items() if var.get()]
        if not selected:
            messagebox.showinfo("Info", "Aucun collecteur sélectionné")
            return
        threading.Thread(target=self.run_collection, args=(selected,), daemon=True).start()

    def run_collection(self, names):
        errors = []
        artefacts = {
            "metadata": {
                "date": datetime.now().isoformat(),
                "hostname": socket.gethostname(),
                "system": platform.system()
            },
            "artefacts": {}
        }

        for name in names:
            try:
                result = run_collector(name)
                artefacts["artefacts"][name] = result
                self.log(f"✅ {name}")
            except Exception as e:
                self.log(f"❌ {name}: {e}")
                errors.append(name)

        artefacts["metadata"]["total"] = len(artefacts["artefacts"])
        filename = f"forensics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        path = UPLOAD_DIR / filename
        with open(path, "w", encoding="utf-8") as f:
            json.dump(artefacts, f, indent=4)
        self.log(f"💾 Sauvegardé : {filename}")

        try:
            api_url = "http://127.0.0.1:8000/session"
            payload = {
                "hostname": artefacts["metadata"]["hostname"],
                "system": artefacts["metadata"]["system"],
                "file_name": filename,
                "file_path": str(path),
                "error_count": len(errors),
                "uploaded_to_drive": False,
                "drive_url": None
            }
            response = requests.post(api_url, params={"email": self.user_email}, json=payload)
            if response.status_code == 201:
                self.log("🗂️ Session enregistrée dans le backend.")
            else:
                self.log(f"⚠️ Erreur sauvegarde backend: {response.text}")
        except Exception as e:
            self.log(f"❌ Erreur communication API: {e}")

        try:
            upload_to_drive(path)
            self.log("☁️ Upload Drive réussi")
        except Exception as e:
            self.log(f"Erreur upload Drive: {e}")

        self.stat_cards["errors"].update_value(str(len(errors)))
        self.refresh_dashboard()

    def load_file(self):
        path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if path:
            try:
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                pretty = json.dumps(data, indent=4)
                self.analysis_text.delete("1.0", tk.END)
                self.analysis_text.insert(tk.END, pretty)
                self.log(f"📂 Analyse de : {os.path.basename(path)}")
            except Exception as e:
                messagebox.showerror("Erreur", str(e))

    def log(self, msg):
        t = datetime.now().strftime("%H:%M:%S")
        log_msg = f"[{t}] {msg}"
        self.logs.append(log_msg)
        self.log_box.insert(tk.END, log_msg + "\n")
        self.log_box.see(tk.END)
        self.activity_list.insert(tk.END, log_msg + "\n")
        self.activity_list.see(tk.END)
