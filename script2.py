
import tkinter as tk
from tkinter import messagebox
import random
import os

APP_PASSWORD = "1234"  # Code pour déverrouiller

class MultiTachesApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Multitâches")
        self.root.geometry("600x500")
        self.show_lock_screen()

    # =========================
    # 🔒 LOCK SCREEN
    # =========================
    def show_lock_screen(self):
        self.clear_window()

        tk.Label(self.root, text="Application Multitâches", font=("Arial", 20)).pack(pady=20)
        tk.Label(self.root, text="Entrez le code :").pack()

        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack(pady=10)

        tk.Button(self.root, text="Déverrouiller", command=self.check_password).pack()

    def check_password(self):
        if self.password_entry.get() == APP_PASSWORD:
            self.show_main_menu()
        else:
            messagebox.showerror("Erreur", "Code incorrect")

    # =========================
    # 🏠 MENU PRINCIPAL
    # =========================
    def show_main_menu(self):
        self.clear_window()

        tk.Label(self.root, text="Menu Principal", font=("Arial", 18)).pack(pady=20)

        tk.Button(self.root, text="❌ Morpion vs Bot", width=30, command=self.show_tictactoe).pack(pady=10)
        tk.Button(self.root, text="📝 Notes", width=30, command=self.show_notes).pack(pady=10)
        tk.Button(self.root, text="🗺️ Plan détaillé CTS", width=30, command=self.show_cts_plan).pack(pady=10)
        tk.Button(self.root, text="🔒 Verrouiller", width=30, command=self.show_lock_screen).pack(pady=20)

    # =========================
    # ❌⭕ MORPION
    # =========================
    def show_tictactoe(self):
        self.clear_window()
        tk.Label(self.root, text="Morpion vs Bot", font=("Arial", 16)).pack(pady=10)

        self.board = [""] * 9
        self.buttons = []

        frame = tk.Frame(self.root)
        frame.pack()

        for i in range(9):
            btn = tk.Button(frame, text="", width=5, height=2,
                            font=("Arial", 24),
                            command=lambda i=i: self.player_move(i))
            btn.grid(row=i//3, column=i%3)
            self.buttons.append(btn)

        tk.Button(self.root, text="Retour", command=self.show_main_menu).pack(pady=20)

    def player_move(self, index):
        if self.board[index] == "":
            self.board[index] = "X"
            self.buttons[index].config(text="X")
            if not self.check_winner("X"):
                self.bot_move()

    def bot_move(self):
        empty = [i for i in range(9) if self.board[i] == ""]
        if empty:
            move = random.choice(empty)
            self.board[move] = "O"
            self.buttons[move].config(text="O")
            self.check_winner("O")

    def check_winner(self, player):
        wins = [(0,1,2),(3,4,5),(6,7,8),
                (0,3,6),(1,4,7),(2,5,8),
                (0,4,8),(2,4,6)]

        for combo in wins:
            if all(self.board[i] == player for i in combo):
                messagebox.showinfo("Fin", f"{player} gagne !")
                self.show_tictactoe()
                return True

        if "" not in self.board:
            messagebox.showinfo("Fin", "Match nul !")
            self.show_tictactoe()
            return True

        return False

    # =========================
    # 📝 NOTES
    # =========================
    def show_notes(self):
        self.clear_window()

        tk.Label(self.root, text="Bloc Notes", font=("Arial", 16)).pack(pady=10)

        self.text_area = tk.Text(self.root, wrap="word")
        self.text_area.pack(expand=True, fill="both")

        if os.path.exists("notes.txt"):
            with open("notes.txt", "r", encoding="utf-8") as f:
                self.text_area.insert("1.0", f.read())

        tk.Button(self.root, text="Sauvegarder", command=self.save_notes).pack(pady=5)
        tk.Button(self.root, text="Retour", command=self.show_main_menu).pack(pady=5)

    def save_notes(self):
        with open("notes.txt", "w", encoding="utf-8") as f:
            f.write(self.text_area.get("1.0", "end"))
        messagebox.showinfo("Sauvegarde", "Notes sauvegardées !")

    # =========================
    # 🗺️ PLAN CTS
    # =========================
    def show_cts_plan(self):
        self.clear_window()

        tk.Label(self.root, text="Plan détaillé CTS Strasbourg", font=("Arial", 16)).pack(pady=10)

        plan_text = """
CTS STRASBOURG - PRINCIPALES LIGNES TRAM

Ligne A : Illkirch ↔ Hautepierre Maillon
Ligne B : Lingolsheim ↔ Hoenheim Gare
Ligne C : Neuhof ↔ Gare Centrale
Ligne D : Kehl ↔ Poteries
Ligne E : Robertsau ↔ Campus d'Illkirch
Ligne F : Elsau ↔ Place d'Islande

Principaux arrêts :
- Gare Centrale
- Homme de Fer (correspondance principale)
- République
- Étoile Bourse
- Campus d'Illkirch
        """

        text_widget = tk.Text(self.root, wrap="word")
        text_widget.insert("1.0", plan_text)
        text_widget.config(state="disabled")
        text_widget.pack(expand=True, fill="both")

        tk.Button(self.root, text="Retour", command=self.show_main_menu).pack(pady=10)

    # =========================
    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

# =========================
# LANCEMENT
# =========================
if __name__ == "__main__":
    root = tk.Tk()
    app = MultiTachesApp(root)
    root.mainloop()


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
