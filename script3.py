import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
import hashlib
import json
import random
import os

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

USER_FILE = "user.json"

# =========================
# 🔐 HASH PASSWORD
# =========================
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def save_user(password):
    with open(USER_FILE, "w") as f:
        json.dump({"password": hash_password(password)}, f)

def load_user():
    if os.path.exists(USER_FILE):
        with open(USER_FILE, "r") as f:
            return json.load(f)
    return None

# =========================
# APP PRINCIPALE
# =========================
class MultiTachesPro(ctk.CTk):

    def __init__(self):
        super().__init__()
        self.title("Multitâches PRO")
        self.geometry("800x600")
        self.resizable(False, False)
        self.show_login()

    # ================= LOGIN =================
    def show_login(self):
        self.clear()

        ctk.CTkLabel(self, text="🔐 Multitâches PRO", font=("Arial", 30)).pack(pady=30)

        self.password_entry = ctk.CTkEntry(self, placeholder_text="Mot de passe", show="*")
        self.password_entry.pack(pady=20)

        user = load_user()

        if user:
            ctk.CTkButton(self, text="Connexion", command=self.login).pack(pady=10)
        else:
            ctk.CTkButton(self, text="Créer mot de passe", command=self.create_account).pack(pady=10)

    def create_account(self):
        pwd = self.password_entry.get()
        if len(pwd) < 4:
            messagebox.showerror("Erreur", "Minimum 4 caractères")
            return
        save_user(pwd)
        messagebox.showinfo("Succès", "Compte créé !")
        self.show_menu()

    def login(self):
        user = load_user()
        if hash_password(self.password_entry.get()) == user["password"]:
            self.show_menu()
        else:
            messagebox.showerror("Erreur", "Mot de passe incorrect")

    # ================= MENU =================
    def show_menu(self):
        self.clear()

        ctk.CTkLabel(self, text="Menu Principal", font=("Arial", 25)).pack(pady=30)

        ctk.CTkButton(self, text="❌ Morpion IA", width=300, command=self.show_tictactoe).pack(pady=15)
        ctk.CTkButton(self, text="📝 Notes", width=300, command=self.show_notes).pack(pady=15)
        ctk.CTkButton(self, text="🗺️ Plan CTS", width=300, command=self.show_cts).pack(pady=15)
        ctk.CTkButton(self, text="🔒 Déconnexion", width=300, command=self.show_login).pack(pady=30)

    # ================= MORPION MINIMAX =================
    def show_tictactoe(self):
        self.clear()
        self.board = [""] * 9

        frame = ctk.CTkFrame(self)
        frame.pack(pady=20)

        self.buttons = []

        for i in range(9):
            btn = ctk.CTkButton(frame, text="", width=100, height=100,
                                command=lambda i=i: self.player_move(i))
            btn.grid(row=i//3, column=i%3, padx=5, pady=5)
            self.buttons.append(btn)

        ctk.CTkButton(self, text="Retour", command=self.show_menu).pack(pady=20)

    def player_move(self, index):
        if self.board[index] == "":
            self.board[index] = "X"
            self.buttons[index].configure(text="X")
            if not self.check_game("X"):
                self.bot_move()

    def bot_move(self):
        move = self.best_move()
        if move is not None:
            self.board[move] = "O"
            self.buttons[move].configure(text="O")
            self.check_game("O")

    def best_move(self):
        best_score = -999
        move = None
        for i in range(9):
            if self.board[i] == "":
                self.board[i] = "O"
                score = self.minimax(False)
                self.board[i] = ""
                if score > best_score:
                    best_score = score
                    move = i
        return move

    def minimax(self, is_max):
        winner = self.get_winner()
        if winner == "O":
            return 1
        elif winner == "X":
            return -1
        elif "" not in self.board:
            return 0

        if is_max:
            best = -999
            for i in range(9):
                if self.board[i] == "":
                    self.board[i] = "O"
                    score = self.minimax(False)
                    self.board[i] = ""
                    best = max(score, best)
            return best
        else:
            best = 999
            for i in range(9):
                if self.board[i] == "":
                    self.board[i] = "X"
                    score = self.minimax(True)
                    self.board[i] = ""
                    best = min(score, best)
            return best

    def get_winner(self):
        wins = [(0,1,2),(3,4,5),(6,7,8),
                (0,3,6),(1,4,7),(2,5,8),
                (0,4,8),(2,4,6)]
        for a,b,c in wins:
            if self.board[a] == self.board[b] == self.board[c] != "":
                return self.board[a]
        return None

    def check_game(self, player):
        winner = self.get_winner()
        if winner:
            messagebox.showinfo("Fin", f"{winner} gagne !")
            self.show_tictactoe()
            return True
        elif "" not in self.board:
            messagebox.showinfo("Fin", "Match nul")
            self.show_tictactoe()
            return True
        return False

    # ================= NOTES =================
    def show_notes(self):
        self.clear()

        self.text = ctk.CTkTextbox(self, width=700, height=400)
        self.text.pack(pady=20)

        if os.path.exists("notes.txt"):
            with open("notes.txt", "r", encoding="utf-8") as f:
                self.text.insert("1.0", f.read())

        ctk.CTkButton(self, text="Sauvegarder", command=self.save_notes).pack(pady=10)
        ctk.CTkButton(self, text="Retour", command=self.show_menu).pack()

    def save_notes(self):
        with open("notes.txt", "w", encoding="utf-8") as f:
            f.write(self.text.get("1.0", "end"))
        messagebox.showinfo("Succès", "Notes sauvegardées")

    # ================= CTS =================
    def show_cts(self):
        self.clear()

        label = ctk.CTkLabel(self, text="Plan Tram CTS Strasbourg", font=("Arial", 20))
        label.pack(pady=20)

        try:
            img = ctk.CTkImage(Image.open("cts_plan.png"), size=(700, 400))
            panel = ctk.CTkLabel(self, image=img, text="")
            panel.image = img
            panel.pack()
        except:
            ctk.CTkLabel(self, text="Ajoute une image 'cts_plan.png' dans le dossier").pack()

        ctk.CTkButton(self, text="Retour", command=self.show_menu).pack(pady=20)

    def clear(self):
        for widget in self.winfo_children():
            widget.destroy()

# =========================
if __name__ == "__main__":
    app = MultiTachesPro()
    app.mainloop()

