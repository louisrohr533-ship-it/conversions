import tkinter as tk
from tkinter import ttk
import time
import os
import json

# =========================
# THÈMES
# =========================

THEMES = {
    "dark": {
        "bg": "#1e1e1e",
        "panel": "#252526",
        "card": "#2d2d30",
        "button": "#3b82f6",
        "hover": "#2563eb",
        "text": "#ffffff",
        "accent": "#4ade80"
    },
    "light": {
        "bg": "#f4f4f4",
        "panel": "#ffffff",
        "card": "#ececec",
        "button": "#2563eb",
        "hover": "#1d4ed8",
        "text": "#222222",
        "accent": "#16a34a"
    }
}


class SidebarButton(tk.Frame):

    def __init__(self, master, icon, text, command):

        super().__init__(
            master,
            bg=master["bg"],
            height=55
        )

        self.command = command

        self.pack_propagate(False)

        self.button = tk.Label(
            self,
            text=f"{icon}   {text}",
            bg=master["bg"],
            fg="white",
            anchor="w",
            padx=18,
            font=("Segoe UI", 11)
        )

        self.button.pack(fill="both", expand=True)

        self.button.bind("<Enter>", self.enter)
        self.button.bind("<Leave>", self.leave)
        self.button.bind("<Button-1>", self.click)

    def enter(self, event):
        self.button.config(bg="#3b82f6")

    def leave(self, event):
        self.button.config(bg=self["bg"])

    def click(self, event):
        self.command()


class DashboardCard(tk.Frame):

    def __init__(self, master, title, value, color):

        super().__init__(
            master,
            bg=color,
            width=220,
            height=140
        )

        self.pack_propagate(False)

        tk.Label(
            self,
            text=title,
            bg=color,
            fg="white",
            font=("Segoe UI", 12)
        ).pack(pady=(20, 5))

        self.value = tk.Label(
            self,
            text=value,
            bg=color,
            fg="white",
            font=("Segoe UI", 28, "bold")
        )

        self.value.pack()


class MultiDesk:

    def __init__(self):

        self.theme = THEMES["dark"]

        self.root = tk.Tk()

        self.root.title("MultiDesk Pro")

        self.root.geometry("1350x760")

        self.root.configure(bg=self.theme["bg"])

        self.root.minsize(1100, 650)

        self.sidebar = tk.Frame(
            self.root,
            width=230,
            bg=self.theme["panel"]
        )

        self.sidebar.pack(side="left", fill="y")

        self.sidebar.pack_propagate(False)

        self.content = tk.Frame(
            self.root,
            bg=self.theme["bg"]
        )

        self.content.pack(
            side="right",
            fill="both",
            expand=True
        )

        tk.Label(
            self.sidebar,
            text="MultiDesk",
            bg=self.theme["panel"],
            fg="white",
            font=("Segoe UI", 22, "bold")
        ).pack(pady=25)

        SidebarButton(
            self.sidebar,
            "🏠",
            "Accueil",
            self.dashboard
        ).pack(fill="x")

        SidebarButton(
            self.sidebar,
            "📒",
            "Bloc-notes",
            self.notes
        ).pack(fill="x")

        SidebarButton(
            self.sidebar,
            "🎮",
            "Morpion",
            self.morpion
        ).pack(fill="x")

        SidebarButton(
            self.sidebar,
            "🕒",
            "Horloge",
            self.clock
        ).pack(fill="x")

        SidebarButton(
            self.sidebar,
            "⚙️",
            "Paramètres",
            self.settings
        ).pack(fill="x")

        SidebarButton(
            self.sidebar,
            "ℹ️",
            "À propos",
            self.about
        ).pack(fill="x")

        self.status = tk.Label(
            self.sidebar,
            text="Prêt",
            bg=self.theme["panel"],
            fg=self.theme["accent"],
            font=("Segoe UI", 10)
        )

        self.status.pack(side="bottom", pady=20)

        self.dashboard()

        self.root.mainloop()

    def clear(self):

        for widget in self.content.winfo_children():
            widget.destroy()