import tkinter as tk
import time
import datetime


class Dashboard:


    def __init__(self, parent, theme, role):

        self.parent = parent
        self.theme = theme
        self.role = role

        self.build()



    def clear(self):

        for widget in self.parent.winfo_children():
            widget.destroy()



    def build(self):

        self.clear()


        title = tk.Label(
            self.parent,
            text="Tableau de bord",
            bg=self.theme["bg"],
            fg=self.theme["text"],
            font=(
                "Segoe UI",
                28,
                "bold"
            )
        )

        title.pack(
            pady=30
        )


        subtitle = tk.Label(
            self.parent,
            text=f"Connecté en tant que : {self.role}",
            bg=self.theme["bg"],
            fg=self.theme["accent"],
            font=(
                "Segoe UI",
                14
            )
        )

        subtitle.pack()



        cards = tk.Frame(
            self.parent,
            bg=self.theme["bg"]
        )

        cards.pack(
            pady=50
        )



        self.card(
            cards,
            "⏰ Heure",
            "--:--:--"
        ).grid(
            row=0,
            column=0,
            padx=20
        )


        self.clock_card = self.card(
            cards,
            "📅 Date",
            ""
        )

        self.clock_card.grid(
            row=0,
            column=1,
            padx=20
        )


        self.card(
            cards,
            "🔐 Niveau",
            self.role
        ).grid(
            row=0,
            column=2,
            padx=20
        )



        self.update_time()



    def card(self, parent, title, value):


        frame = tk.Frame(
            parent,
            bg=self.theme["card"],
            width=220,
            height=130
        )

        frame.pack_propagate(
            False
        )


        tk.Label(
            frame,
            text=title,
            bg=self.theme["card"],
            fg=self.theme["text"],
            font=(
                "Segoe UI",
                12
            )
        ).pack(
            pady=15
        )


        label = tk.Label(
            frame,
            text=value,
            bg=self.theme["card"],
            fg=self.theme["accent"],
            font=(
                "Segoe UI",
                22,
                "bold"
            )
        )

        label.pack()


        frame.value = label


        return frame



    def update_time(self):

        now = time.strftime(
            "%H:%M:%S"
        )

        today = datetime.datetime.now().strftime(
            "%d/%m/%Y"
        )


        # première carte horloge
        for widget in self.parent.winfo_children():

            pass


        self.clock_card.value.config(
            text=today
        )


        self.parent.after(
            1000,
            self.update_time
        )