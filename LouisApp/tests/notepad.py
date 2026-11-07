import tkinter as tk
from tkinter import filedialog
import os


class Notes:


    def __init__(self, parent, theme):

        self.parent = parent
        self.theme = theme

        self.build()



    def clear(self):

        for widget in self.parent.winfo_children():
            widget.destroy()



    def build(self):

        self.clear()


        title = tk.Label(
            self.parent,
            text="📒 Bloc-notes",
            bg=self.theme["bg"],
            fg=self.theme["text"],
            font=(
                "Segoe UI",
                26,
                "bold"
            )
        )

        title.pack(
            pady=20
        )


        toolbar = tk.Frame(
            self.parent,
            bg=self.theme["bg"]
        )

        toolbar.pack()



        tk.Button(
            toolbar,
            text="💾 Sauvegarder",
            command=self.save,
            bg=self.theme["button"],
            fg="white",
            relief="flat"
        ).pack(
            side="left",
            padx=5
        )


        tk.Button(
            toolbar,
            text="📂 Ouvrir",
            command=self.open_file,
            bg=self.theme["button"],
            fg="white",
            relief="flat"
        ).pack(
            side="left",
            padx=5
        )


        self.counter = tk.Label(
            toolbar,
            text="0 caractères",
            bg=self.theme["bg"],
            fg=self.theme["accent"]
        )

        self.counter.pack(
            side="right",
            padx=20
        )



        self.text = tk.Text(
            self.parent,
            bg="#252526",
            fg="white",
            insertbackground="white",
            font=(
                "Consolas",
                13
            ),
            relief="flat",
            wrap="word"
        )


        self.text.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=20
        )


        self.text.bind(
            "<KeyRelease>",
            self.update_counter
        )


        self.load()



    def update_counter(self,event=None):

        content = self.text.get(
            "1.0",
            "end-1c"
        )

        self.counter.config(
            text=f"{len(content)} caractères"
        )


        self.save()



    def save(self):

        with open(
            "notes.txt",
            "w",
            encoding="utf8"
        ) as f:

            f.write(
                self.text.get(
                    "1.0",
                    "end"
                )
            )



    def load(self):

        if os.path.exists("notes.txt"):

            with open(
                "notes.txt",
                "r",
                encoding="utf8"
            ) as f:

                self.text.insert(
                    "1.0",
                    f.read()
                )



    def open_file(self):

        filename = filedialog.askopenfilename(
            filetypes=[
                (
                    "Fichiers texte",
                    "*.txt"
                )
            ]
        )


        if filename:

            with open(
                filename,
                "r",
                encoding="utf8"
            ) as f:

                self.text.delete(
                    "1.0",
                    "end"
                )

                self.text.insert(
                    "1.0",
                    f.read()
                )
