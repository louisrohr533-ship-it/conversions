import tkinter as tk
from tkinter import messagebox
import json
import os


USERS_FILE = "users.json"



class AdminPanel:


    def __init__(self, parent, theme):

        self.parent = parent
        self.theme = theme

        self.load_users()

        self.build()



    def load_users(self):

        if os.path.exists(USERS_FILE):

            with open(
                USERS_FILE,
                "r",
                encoding="utf8"
            ) as f:

                self.users = json.load(f)

        else:

            self.users = {}



    def save_users(self):

        with open(
            USERS_FILE,
            "w",
            encoding="utf8"
        ) as f:

            json.dump(
                self.users,
                f,
                indent=4
            )



    def clear(self):

        for widget in self.parent.winfo_children():

            widget.destroy()



    def build(self):

        self.clear()


        tk.Label(
            self.parent,
            text="👨‍💼 Panneau Administrateur",
            bg=self.theme["bg"],
            fg=self.theme["text"],
            font=(
                "Segoe UI",
                26,
                "bold"
            )
        ).pack(
            pady=25
        )


        self.listbox = tk.Listbox(
            self.parent,
            font=(
                "Segoe UI",
                12
            ),
            bg=self.theme["card"],
            fg=self.theme["text"],
            height=10
        )

        self.listbox.pack(
            padx=40,
            pady=20,
            fill="x"
        )


        self.refresh()



        form = tk.Frame(
            self.parent,
            bg=self.theme["bg"]
        )

        form.pack(
            pady=20
        )


        self.username = tk.Entry(
            form,
            font=("Segoe UI",12)
        )

        self.username.grid(
            row=0,
            column=0,
            padx=5
        )


        self.password = tk.Entry(
            form,
            show="•",
            font=("Segoe UI",12)
        )

        self.password.grid(
            row=0,
            column=1,
            padx=5
        )



        tk.Button(
            form,
            text="➕ Ajouter",
            command=self.add_user,
            bg=self.theme["button"],
            fg="white",
            relief="flat"
        ).grid(
            row=0,
            column=2,
            padx=5
        )



        tk.Button(
            self.parent,
            text="❌ Supprimer sélection",
            command=self.delete_user,
            bg="#dc2626",
            fg="white",
            relief="flat"
        ).pack(
            pady=10
        )



    def refresh(self):

        self.listbox.delete(
            0,
            "end"
        )


        for user in self.users:

            role = self.users[user]["role"]

            self.listbox.insert(
                "end",
                f"{user}  ({role})"
            )



    def add_user(self):

        name = self.username.get()
        password = self.password.get()


        if name == "" or password == "":

            messagebox.showerror(
                "Erreur",
                "Remplis tous les champs"
            )

            return



        if name in self.users:

            messagebox.showerror(
                "Erreur",
                "Utilisateur déjà existant"
            )

            return



        self.users[name] = {

            "password": password,

            "role": "user"

        }


        self.save_users()

        self.refresh()


        messagebox.showinfo(
            "Succès",
            "Utilisateur ajouté"
        )



    def delete_user(self):

        selection = self.listbox.curselection()


        if not selection:

            return


        item = self.listbox.get(
            selection[0]
        )


        username = item.split()[0]


        if username == "admin":

            messagebox.showerror(
                "Erreur",
                "Impossible de supprimer admin"
            )

            return



        del self.users[username]

        self.save_users()

        self.refresh()