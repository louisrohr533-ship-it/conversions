import tkinter as tk
from tkinter import messagebox
import json
import os


USERS_FILE = "users.json"


# =========================
# UTILISATEURS PAR DÉFAUT
# =========================

DEFAULT_USERS = {
    "admin": {
        "password": "admin123",
        "role": "admin"
    },

    "user": {
        "password": "user123",
        "role": "user"
    }
}


def load_users():

    if not os.path.exists(USERS_FILE):

        with open(
            USERS_FILE,
            "w",
            encoding="utf8"
        ) as f:

            json.dump(
                DEFAULT_USERS,
                f,
                indent=4
            )

        return DEFAULT_USERS


    with open(
        USERS_FILE,
        "r",
        encoding="utf8"
    ) as f:

        return json.load(f)



class LoginWindow:


    def __init__(self, root, success):

        self.root = root
        self.success = success

        self.users = load_users()


        self.root.title("MultiDesk Pro - Connexion")
        self.root.geometry("450x500")
        self.root.resizable(False, False)

        self.root.configure(
            bg="#1e1e1e"
        )


        self.create_interface()



    def create_interface(self):


        title = tk.Label(
            self.root,
            text="MultiDesk Pro",
            bg="#1e1e1e",
            fg="white",
            font=(
                "Segoe UI",
                26,
                "bold"
            )
        )

        title.pack(
            pady=40
        )



        box = tk.Frame(
            self.root,
            bg="#252526"
        )

        box.pack(
            padx=40,
            fill="both"
        )



        tk.Label(
            box,
            text="Utilisateur",
            bg="#252526",
            fg="white",
            font=("Segoe UI",11)
        ).pack(
            pady=(25,5)
        )


        self.username = tk.Entry(
            box,
            font=("Segoe UI",13),
            justify="center"
        )

        self.username.pack(
            padx=30
        )



        tk.Label(
            box,
            text="Mot de passe",
            bg="#252526",
            fg="white",
            font=("Segoe UI",11)
        ).pack(
            pady=(20,5)
        )



        self.password = tk.Entry(
            box,
            show="•",
            font=("Segoe UI",13),
            justify="center"
        )

        self.password.pack(
            padx=30
        )



        self.show = tk.BooleanVar()



        tk.Checkbutton(
            box,
            text="Afficher le mot de passe",
            variable=self.show,
            command=self.toggle_password,
            bg="#252526",
            fg="white",
            selectcolor="#252526"
        ).pack(
            pady=10
        )



        tk.Button(
            box,
            text="Connexion",
            command=self.login,
            bg="#3b82f6",
            fg="white",
            relief="flat",
            font=("Segoe UI",12,"bold"),
            padx=40,
            pady=10
        ).pack(
            pady=25
        )



    def toggle_password(self):

        if self.show.get():

            self.password.config(
                show=""
            )

        else:

            self.password.config(
                show="•"
            )



    def login(self):

        user = self.username.get()
        pwd = self.password.get()


        if user in self.users:

            if self.users[user]["password"] == pwd:


                role = self.users[user]["role"]


                messagebox.showinfo(
                    "Connexion",
                    f"Bienvenue {user}\nMode : {role}"
                )


                self.root.destroy()


                self.success(role)


                return



        messagebox.showerror(
            "Erreur",
            "Identifiant ou mot de passe incorrect"
        )