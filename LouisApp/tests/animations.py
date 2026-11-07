import tkinter as tk


# =========================
# FONDU D'OUVERTURE
# =========================

def fade_in(window, step=0.05):

    try:

        alpha = window.attributes("-alpha")

        if alpha < 1:

            alpha += step

            window.attributes(
                "-alpha",
                alpha
            )

            window.after(
                20,
                lambda: fade_in(window, step)
            )

        else:

            window.attributes(
                "-alpha",
                1
            )

    except:

        pass



# =========================
# FONDU DE FERMETURE
# =========================

def fade_out(window, step=0.05):

    try:

        alpha = window.attributes("-alpha")


        if alpha > 0:

            alpha -= step

            window.attributes(
                "-alpha",
                alpha
            )

            window.after(
                20,
                lambda: fade_out(window, step)
            )

        else:

            window.destroy()


    except:

        window.destroy()



# =========================
# APPARITION D'UN WIDGET
# =========================

def appear(widget, y=0, target=20):

    if y < target:

        y += 2

        widget.place(
            relx=0.5,
            y=y,
            anchor="center"
        )

        widget.after(
            15,
            lambda: appear(
                widget,
                y,
                target
            )
        )



# =========================
# GLISSEMENT D'UN PANNEAU
# =========================

def slide_in(frame, start=-250, end=0):

    if start < end:

        start += 10

        frame.place(
            x=start,
            y=0
        )

        frame.after(
            10,
            lambda: slide_in(
                frame,
                start,
                end
            )
        )



# =========================
# NOTIFICATION
# =========================

def notification(root, message):

    box = tk.Label(
        root,
        text=message,
        bg="#3b82f6",
        fg="white",
        font=(
            "Segoe UI",
            11,
            "bold"
        ),
        padx=20,
        pady=10
    )


    box.place(
        relx=0.5,
        rely=0.05,
        anchor="center"
    )


    root.after(
        2500,
        box.destroy
    )



# =========================
# ANIMATION BOUTON
# =========================

def button_hover(button, normal, hover):

    button.bind(
        "<Enter>",
        lambda e:
        button.config(
            bg=hover
        )
    )


    button.bind(
        "<Leave>",
        lambda e:
        button.config(
            bg=normal
        )
    )



# =========================
# ANIMATION CARTE DASHBOARD
# =========================

def card_animation(card):

    card.place(
        y=-50
    )


    def move(y):

        if y < 0:

            y += 5

            card.place(
                y=y
            )

            card.after(
                15,
                lambda:
                move(y)
            )


    move(-50)



# =========================
# EFFET MORPION
# =========================

def animate_move(button, symbol):

    button.config(
        text=""
    )


    def write(size):

        if size < 28:

            size += 2

            button.config(
                font=(
                    "Segoe UI",
                    size,
                    "bold"
                ),
                text=symbol
            )


            button.after(
                30,
                lambda:
                write(size)
            )


    write(10)