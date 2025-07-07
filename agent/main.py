import tkinter as tk
import ttkbootstrap as tb

from views.login_view import LoginView
from views.register_view import RegisterView
from views.dashboard_view import DashboardView


class App(tb.Window):
    def __init__(self):
        super().__init__(themename="darkly")
        self.title("Agent Forensics - Connexion")
        self.geometry("1200x800")
        self.resizable(True, True)

        self.container = tb.Frame(self)
        self.container.pack(fill="both", expand=True)

        self.current_view = None
        self.show_login()

    def clear_view(self):
        if self.current_view:
            self.current_view.destroy()

    def show_login(self):
        self.clear_view()
        self.current_view = LoginView(self.container, on_login=self.show_dashboard, on_register=self.show_register)
        self.current_view.pack(fill="both", expand=True)

    def show_register(self):
        self.clear_view()
        self.current_view = RegisterView(self.container, on_register_success=self.show_login)
        self.current_view.pack(fill="both", expand=True)

    def show_dashboard(self, user_email):
        if hasattr(self, "current_view"):
            self.current_view.destroy()
        self.current_view = DashboardView(self.container, user_email=user_email, on_logout=self.show_login)
        self.current_view.pack(fill="both", expand=True)


if __name__ == "__main__":
    app = App()
    app.mainloop()
