import tkinter as tk
from tkinter import messagebox
import threading
import server  # Assure-toi que ce fichier est dans le même dossier

def lancer_collecte():
    def collecte():
        try:
            # Charger les collecteurs depuis server.py
            selected_collectors = [c["name"] for c in server.load_collectors()]
            
            # Lancer la collecte et upload vers Drive
            server.collection_worker(selected_collectors)
            
            messagebox.showinfo("Succès", "Collecte et envoi sur Drive terminés.")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur : {e}")

    # Lancer la collecte dans un thread pour ne pas bloquer l’interface
    threading.Thread(target=collecte).start()

# Interface utilisateur
app = tk.Tk()
app.title("Agent Forensique")

tk.Label(app, text="Cliquez sur le bouton pour démarrer la collecte.").pack(pady=10)
tk.Button(app, text="Démarrer la collecte", command=lancer_collecte).pack(pady=10)

app.geometry("300x150")
app.mainloop()
