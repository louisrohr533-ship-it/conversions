import tkinter as tk


class Morpion:


    def __init__(self, parent, theme):

        self.parent = parent
        self.theme = theme

        self.score_x = 0
        self.score_o = 0

        self.new_game()



    def clear(self):

        for widget in self.parent.winfo_children():
            widget.destroy()



    def build(self):

        self.clear()


        title = tk.Label(
            self.parent,
            text="🎮 Morpion",
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


        self.info = tk.Label(
            self.parent,
            text="Tour de X",
            bg=self.theme["bg"],
            fg=self.theme["accent"],
            font=(
                "Segoe UI",
                14
            )
        )

        self.info.pack()



        self.score = tk.Label(
            self.parent,
            text=self.get_score(),
            bg=self.theme["bg"],
            fg=self.theme["text"]
        )

        self.score.pack(
            pady=10
        )


        frame = tk.Frame(
            self.parent,
            bg=self.theme["bg"]
        )

        frame.pack(
            pady=20
        )


        self.buttons = []


        for i in range(3):

            row = []

            for j in range(3):

                button = tk.Button(
                    frame,
                    text="",
                    width=5,
                    height=2,
                    font=(
                        "Segoe UI",
                        25,
                        "bold"
                    ),
                    bg=self.theme["card"],
                    fg=self.theme["text"],
                    relief="flat",
                    command=lambda r=i,c=j:self.play(r,c)
                )

                button.grid(
                    row=i,
                    column=j,
                    padx=5,
                    pady=5
                )


                row.append(button)


            self.buttons.append(row)



        tk.Button(
            self.parent,
            text="🔄 Nouvelle partie",
            command=self.new_game,
            bg=self.theme["button"],
            fg="white",
            relief="flat",
            padx=20,
            pady=8
        ).pack(
            pady=15
        )



    def new_game(self):

        self.board = [
            ["","",""],
            ["","",""],
            ["","",""]
        ]

        self.player = "X"

        if hasattr(self,"buttons"):

            for row in self.buttons:

                for button in row:

                    button.config(
                        text=""
                    )

        self.build()



    def play(self,r,c):

        if self.board[r][c] != "":
            return


        self.board[r][c] = self.player


        self.buttons[r][c].config(
            text=self.player
        )


        result = self.check()


        if result:

            if result == "X":
                self.score_x += 1

            elif result == "O":
                self.score_o += 1


            self.info.config(
                text=f"{result} gagne !"
            )

            self.score.config(
                text=self.get_score()
            )

            return



        self.player = (
            "O"
            if self.player=="X"
            else "X"
        )


        self.info.config(
            text=f"Tour de {self.player}"
        )



    def check(self):

        lines = []


        lines.extend(self.board)


        lines.extend(
            [
                [
                    self.board[0][i],
                    self.board[1][i],
                    self.board[2][i]
                ]

                for i in range(3)
            ]
        )


        lines.append(
            [
                self.board[0][0],
                self.board[1][1],
                self.board[2][2]
            ]
        )


        lines.append(
            [
                self.board[0][2],
                self.board[1][1],
                self.board[2][0]
            ]
        )


        for line in lines:

            if (
                line[0]
                ==
                line[1]
                ==
                line[2]
                != ""
            ):

                return line[0]


        return None



    def get_score(self):

        return (
            f"❌ X : {self.score_x}"
            f"     ⭕ O : {self.score_o}"
        )