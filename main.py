from tkinter import *
import pandas
import random

# Create empty dictionaries
current_card = {}
to_learn = {}

try:
    data = pandas.read_csv("data/words_to_learn.csv")  # If words_to_learn.csv does not exist, then read org csv
    # i.e. french_words.csv
except FileNotFoundError:
    # print("2.....................*****************")
    original_data = pandas.read_csv("data/french_words.csv")
    to_learn = original_data.to_dict(orient="records")  # Convert to dictionary {key : value}
else:
    to_learn = data.to_dict(orient="records")

BACKGROUND_COLOR = "#B1DDC6"


# --------------------------------------- Call Next Card ------------------------------------------------- #
def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_text, text=current_card["French"], fill="black")
    canvas.itemconfig(card_background, image=card_front_img)
    flip_timer = window.after(3000, func=flip_card)


# -------------------------------------- Flip the card ---------------------------------------------------#
def flip_card():
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_text, text=current_card["English"], fill="white")
    canvas.itemconfig(card_background, image=card_back_img)


# -------------------------------------- Remove known words, so that they don't repeat ------------------#
def is_known():
    to_learn.remove(current_card)
    data_csv = pandas.DataFrame(to_learn)
    data_csv.to_csv("data/words_to_learn.csv", index=False)
    next_card()


# ------------------------------------ UI SETUP ------------------------------------------------ #
window = Tk()
window.title("Flash Cards")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip_card)  # Flip the card after 3 secs.

# The Canvas is a rectangular area intended for drawing pictures or other complex layouts.
# You can place graphics, text, widgets or frames on a Canvas.
canvas = Canvas(width=800, height=526)
card_front_img = PhotoImage(file="images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")
card_background = canvas.create_image(400, 263, image=card_front_img)  # Create an image on canvas.
canvas.grid(column=0, row=0, columnspan=2)
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
card_title = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"))
card_text = canvas.create_text(400, 263, text="", font=("Ariel", 60, "bold"))

# Create [Unknown] Button
cross_image = PhotoImage(file="images/wrong.png")
unknown_button = Button(image=cross_image, highlightthickness=0, command=next_card)  # See next word.
unknown_button.grid(row=1, column=0)

# Create [Known] Button
check_image = PhotoImage(file="images/right.png")
known_button = Button(image=check_image, highlightthickness=0, command=is_known)  # Remove the known word from list.
known_button.grid(row=1, column=1)

next_card()

window.mainloop()
