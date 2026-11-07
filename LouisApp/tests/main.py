import tkinter as tk

from notepad import Notes
from login_screen import LoginWindow
from app_theme import THEMES 
from morpion import Morpion
from admin_panel import AdminPanel
from app_setting import  Settings
from animations import fade_in

class MultiDeskPro:


    def __init__(self, role):

        self.role = role

        self.theme = THEMES["Sombre"]


        self.root = tk.Tk()

        self.root.title(
            "MultiDesk Pro"
        )

        self.root.geometry(
            "1300x750"
        )

        self.root.configure(
            bg=self.theme["bg"]
        )


        self.create_layout()


        self.root.mainloop()



    def create_layout(self):


        # =====================
        # BARRE LATERALE
        # =====================

        self.sidebar = tk.Frame(
            self.root,
            bg=self.theme["panel"],
            width=230
        )

        self.sidebar.pack(
            side="left",
            fill="y"
        )

        self.sidebar.pack_propagate(
            False
        )



        logo = tk.Label(
            self.sidebar,
            text="MultiDesk\nPro",
            bg=self.theme["panel"],
            fg=self.theme["text"],
            font=(
                "Segoe UI",
                24,
                "bold"
            )
        )

        logo.pack(
            pady=30
        )



        self.add_button(
            "🏠 Accueil",
            self.home
        )

        self.add_button(
            "📒 Notes",
            self.notes
        )

        self.add_button(
            "🎮 Morpion",
            self.morpion
        )

        self.add_button(
            "🕒 Horloge",
            self.clock
        )


        if self.role == "admin":

            self.add_button(
                "👨‍💼 Administration",
                self.admin
            )



        self.add_button(
            "⚙️ Paramètres",
            self.settings
        )



        # =====================
        # ZONE PRINCIPALE
        # =====================


        self.content = tk.Frame(
            self.root,
            bg=self.theme["bg"]
        )

        self.content.pack(
            side="right",
            fill="both",
            expand=True
        )


        self.home()



    def add_button(self,text,command):

        b = tk.Button(
            self.sidebar,
            text=text,
            command=command,
            bg=self.theme["panel"],
            fg=self.theme["text"],
            activebackground=self.theme["button"],
            activeforeground="white",
            relief="flat",
            font=(
                "Segoe UI",
                12
            ),
            anchor="w",
            padx=20,
            pady=12
        )

        b.pack(
            fill="x",
            pady=3
        )



    def clear(self):

        for w in self.content.winfo_children():

            w.destroy()



    # =====================
    # PAGES
    # =====================


    def home(self):

        self.clear()


        tk.Label(
            self.content,
            text="Bienvenue dans MultiDesk Pro",
            bg=self.theme["bg"],
            fg=self.theme["text"],
            font=(
                "Segoe UI",
                28,
                "bold"
            )
        ).pack(
            pady=80
        )


        tk.Label(
            self.content,
            text=f"Connecté en mode : {self.role}",
            bg=self.theme["bg"],
            fg=self.theme["accent"],
            font=(
                "Segoe UI",
                15
            )
        ).pack()

        def notes(self):
            Notes(
                self.content,
                self.theme
            )

        self.clear()

        tk.Label(
            self.content,
            text="Bloc-notes",
            bg=self.theme["bg"],
            fg=self.theme["text"],
            font=("Segoe UI",25)
        ).pack(
            pady=50
        )

        def morpion(self):
            Morpion(
                self.content,
                self.theme
            )

        self.clear()

        tk.Label(
            self.content,
            text="Morpion",
            bg=self.theme["bg"],
            fg=self.theme["text"],
            font=("Segoe UI",25)
        ).pack(
            pady=50
        )



    def clock(self):

        self.clear()

        tk.Label(
            self.content,
            text="Horloge",
            bg=self.theme["bg"],
            fg=self.theme["text"],
            font=("Segoe UI",25)
        ).pack(
            pady=50
        )

        def admin(self):
            AdminPanel(
                self.content,
                self.theme
            )

        self.clear()

        tk.Label(
            self.content,
            text="Panneau Administrateur",
            bg=self.theme["bg"],
            fg=self.theme["text"],
            font=("Segoe UI",25)
        ).pack(
            pady=50
        )

        def settings(self):
            Settings(
                self.content,
                self
            )

        self.clear()

        tk.Label(
            self.content,
            text="Paramètres",
            bg=self.theme["bg"],
            fg=self.theme["text"],
            font=("Segoe UI",25)
        ).pack(
            pady=50
        )




# =========================
# LANCEMENT
# =========================


def start(role):

    MultiDeskPro(role)



root = tk.Tk()


LoginWindow(
    root,
    start
)


root.mainloop()