import tkinter as tk
import ttkbootstrap as tb
from tkinter import messagebox
import requests

API_URL = "http://127.0.0.1:8000"

class RegisterView(tb.Frame):
    def __init__(self, parent, on_register_success):
        super().__init__(parent)
        self.on_register_success = on_register_success
        self.build_ui()

    def build_ui(self):
        frame = tb.Frame(self)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        tb.Label(frame, text="📝 Créer un Compte", font=("Segoe UI", 20, "bold")).pack(pady=10)

        self.email_entry = tb.Entry(frame, width=40)
        self.email_entry.insert(0, "Email")
        self.email_entry.pack(pady=5)

        self.password_entry = tb.Entry(frame, width=40, show="*")
        self.password_entry.insert(0, "Mot de passe")
        self.password_entry.pack(pady=5)

        self.confirm_entry = tb.Entry(frame, width=40, show="*")
        self.confirm_entry.insert(0, "Confirmer le mot de passe")
        self.confirm_entry.pack(pady=5)

        tb.Button(frame, text="Créer", command=self.register, bootstyle="success").pack(pady=10)
        tb.Button(frame, text="Retour", command=self.on_register_success, bootstyle="secondary").pack()

    def register(self):
        email = self.email_entry.get().strip()
        password = self.password_entry.get()
        confirm = self.confirm_entry.get()

        if not email or not password or not confirm:
            messagebox.showwarning("Champs requis", "Veuillez remplir tous les champs.")
            return

        if password != confirm:
            messagebox.showerror("Erreur", "Les mots de passe ne correspondent pas.")
            return

        try:
            response = requests.post(f"{API_URL}/signup", json={"email": email, "password": password})
            if response.status_code == 201:
                messagebox.showinfo("Succès", "Compte créé avec succès.")
                self.on_register_success()
            elif response.status_code == 400:
                error_msg = response.json().get("detail", "Erreur inconnue")
                messagebox.showerror("Erreur", f"Impossible de créer le compte : {error_msg}")
            else:
                messagebox.showerror("Erreur", f"Erreur serveur : {response.status_code}")
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Erreur réseau", f"Impossible de contacter l'API.\n{e}")
