import ttkbootstrap as tb
from tkinter import messagebox
import requests

API_URL = "http://127.0.0.1:8000" 

class LoginView(tb.Frame):
    def __init__(self, parent, on_login, on_register):
        super().__init__(parent)
        self.on_login = on_login
        self.on_register = on_register
        self.build_ui()

    def build_ui(self):
        frame = tb.Frame(self)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        tb.Label(frame, text="🔐 Connexion", font=("Segoe UI", 20, "bold")).pack(pady=10)

        self.email_entry = tb.Entry(frame, width=40)
        self.email_entry.insert(0, "Email")
        self.email_entry.pack(pady=5)
        
        self.password_entry = tb.Entry(frame, width=40, show="*")
        self.password_entry.insert(0, "Mot de passe")
        self.password_entry.pack(pady=5)

        tb.Button(frame, text="Se connecter", command=self.login, bootstyle="primary").pack(pady=10)

        tb.Label(frame, text="Pas encore de compte ?").pack()
        tb.Button(frame, text="Créer un compte", command=self.on_register, bootstyle="secondary-link").pack(pady=5)

    def login(self):
        email = self.email_entry.get().strip()
        password = self.password_entry.get()

        if not email or not password:
            messagebox.showwarning("Champs requis", "Veuillez remplir tous les champs.")
            return

        try:
            response = requests.post(
                f"{API_URL}/login",
                json={"email": email, "password": password}
            )

            if response.status_code == 200:
                messagebox.showinfo("Succès", "Connexion réussie !")
                self.on_login(email)  # <-- on passe email ici
            elif response.status_code == 401:
                messagebox.showerror("Erreur", "Identifiants incorrects.")
            else:
                messagebox.showerror("Erreur", f"Erreur serveur : {response.status_code}")
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Erreur réseau", f"Impossible de contacter le serveur.\n{e}")
