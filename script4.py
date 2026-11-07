import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
import sqlite3
import hashlib
import os
import datetime

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# ================= DATABASE =================
conn = sqlite3.connect("multitaches.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS stats (
    user_id INTEGER,
    wins INTEGER DEFAULT 0,
    losses INTEGER DEFAULT 0,
    draws INTEGER DEFAULT 0
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS notes (
    user_id INTEGER,
    content TEXT
)
""")

conn.commit()

# ================= UTILS =================
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# ================= APP =================
class MultiTachesPro(ctk.CTk):

    def __init__(self):
        super().__init__()
        self.title("Multitâches PRO MAX")
        self.geometry("900x650")
        self.current_user = None
        self.show_login()

    # ================= LOGIN =================
    def show_login(self):
        self.clear()

        ctk.CTkLabel(self, text="🔐 Multitâches PRO MAX", font=("Arial", 30)).pack(pady=30)

        self.username_entry = ctk.CTkEntry(self, placeholder_text="Nom utilisateur")
        self.username_entry.pack(pady=10)

        self.password_entry = ctk.CTkEntry(self, placeholder_text="Mot de passe", show="*")
        self.password_entry.pack(pady=10)

        ctk.CTkButton(self, text="Connexion", command=self.login).pack(pady=10)
        ctk.CTkButton(self, text="Créer compte", command=self.register).pack(pady=5)

    def register(self):
        username = self.username_entry.get()
        password = hash_password(self.password_entry.get())

        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (?,?)",
                           (username, password))
            conn.commit()
            user_id = cursor.lastrowid
            cursor.execute("INSERT INTO stats (user_id) VALUES (?)", (user_id,))
            conn.commit()
            messagebox.showinfo("Succès", "Compte créé !")
        except:
            messagebox.showerror("Erreur", "Utilisateur déjà existant")

    def login(self):
        username = self.username_entry.get()
        password = hash_password(self.password_entry.get())

        cursor.execute("SELECT id FROM users WHERE username=? AND password=?",
                       (username, password))
        result = cursor.fetchone()

        if result:
            self.current_user = result[0]
            self.show_menu()
        else:
            messagebox.showerror("Erreur", "Identifiants incorrects")

    # ================= MENU =================
    def show_menu(self):
        self.clear()

        ctk.CTkLabel(self, text="Menu Principal", font=("Arial", 25)).pack(pady=30)

        ctk.CTkButton(self, text="❌ Morpion IA", width=300, command=self.show_tictactoe).pack(pady=10)
        ctk.CTkButton(self, text="📊 Statistiques", width=300, command=self.show_stats).pack(pady=10)
        ctk.CTkButton(self, text="📝 Notes", width=300, command=self.show_notes).pack(pady=10)
        ctk.CTkButton(self, text="🗺️ Plan CTS", width=300, command=self.show_cts).pack(pady=10)
        ctk.CTkButton(self, text="🔒 Déconnexion", width=300, command=self.show_login).pack(pady=20)

    # ================= MORPION =================
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
            if winner == "X":
                cursor.execute("UPDATE stats SET wins=wins+1 WHERE user_id=?",
                               (self.current_user,))
            else:
                cursor.execute("UPDATE stats SET losses=losses+1 WHERE user_id=?",
                               (self.current_user,))
            conn.commit()
            messagebox.showinfo("Fin", f"{winner} gagne !")
            self.show_tictactoe()
            return True
        elif "" not in self.board:
            cursor.execute("UPDATE stats SET draws=draws+1 WHERE user_id=?",
                           (self.current_user,))
            conn.commit()
            messagebox.showinfo("Fin", "Match nul")
            self.show_tictactoe()
            return True
        return False

    # ================= STATS =================
    def show_stats(self):
        self.clear()
        cursor.execute("SELECT wins, losses, draws FROM stats WHERE user_id=?",
                       (self.current_user,))
        stats = cursor.fetchone()

        ctk.CTkLabel(self, text="📊 Statistiques", font=("Arial", 25)).pack(pady=30)
        ctk.CTkLabel(self, text=f"Victoires : {stats[0]}").pack(pady=10)
        ctk.CTkLabel(self, text=f"Défaites : {stats[1]}").pack(pady=10)
        ctk.CTkLabel(self, text=f"Matchs nuls : {stats[2]}").pack(pady=10)

        ctk.CTkButton(self, text="Retour", command=self.show_menu).pack(pady=20)

    # ================= NOTES =================
    def show_notes(self):
        self.clear()
        self.text = ctk.CTkTextbox(self, width=700, height=400)
        self.text.pack(pady=20)

        cursor.execute("SELECT content FROM notes WHERE user_id=?",
                       (self.current_user,))
        result = cursor.fetchone()
        if result:
            self.text.insert("1.0", result[0])

        ctk.CTkButton(self, text="Sauvegarder", command=self.save_notes).pack(pady=10)
        ctk.CTkButton(self, text="Retour", command=self.show_menu).pack()

    def save_notes(self):
        content = self.text.get("1.0", "end")
        cursor.execute("DELETE FROM notes WHERE user_id=?", (self.current_user,))
        cursor.execute("INSERT INTO notes (user_id, content) VALUES (?,?)",
                       (self.current_user, content))
        conn.commit()
        messagebox.showinfo("Succès", "Notes sauvegardées")

    # ================= CTS =================
    def show_cts(self):
        self.clear()

        ctk.CTkLabel(self, text="Plan CTS Strasbourg", font=("Arial", 20)).pack(pady=20)

        try:
            img = ctk.CTkImage(Image.open("cts_plan.png"), size=(750, 450))
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


