import tkinter as tk
import json
import os

from app_themes import THEMES


SETTINGS_FILE = "settings.json"



class Settings:


    def __init__(self, parent, app):

        self.parent = parent
        self.app = app

        self.build()



    def clear(self):

        for widget in self.parent.winfo_children():
            widget.destroy()



    def build(self):

        self.clear()


        tk.Label(
            self.parent,
            text="⚙️ Paramètres",
            bg=self.app.theme["bg"],
            fg=self.app.theme["text"],
            font=(
                "Segoe UI",
                26,
                "bold"
            )
        ).pack(
            pady=30
        )



        tk.Label(
            self.parent,
            text="Choisir un thème",
            bg=self.app.theme["bg"],
            fg=self.app.theme["text"],
            font=(
                "Segoe UI",
                14
            )
        ).pack(
            pady=10
        )



        for theme_name in app_themes:


            tk.Button(
                self.parent,
                text=theme_name,
                command=lambda t=theme_name:self.change_theme(t),
                bg=self.app.theme["button"],
                fg="white",
                relief="flat",
                width=20,
                pady=8
            ).pack(
                pady=5
            )



    def change_theme(self, name):

        self.app.theme = app_themes[name]


        with open(
            SETTINGS_FILE,
            "w",
            encoding="utf8"
        ) as f:

            json.dump(
                {
                    "theme": name
                },
                f,
                indent=4
            )


        self.refresh_all()



    def refresh_all(self):

        self.app.root.configure(
            bg=self.app.theme["bg"]
        )

        self.app.sidebar.configure(
            bg=self.app.theme["panel"]
        )

        self.app.content.configure(
            bg=self.app.theme["bg"]
        )

        self.build()