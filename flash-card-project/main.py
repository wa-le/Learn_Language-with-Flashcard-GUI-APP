from tkinter import *
import pandas
import random


BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
learn_words = {}

# dealing with the csv file
# get data from the words_to_learn.csv, but if there is no such file yet, use the (original) french_words.csv file
try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    learn_words = original_data.to_dict(orient="records")
else:
    learn_words = data.to_dict(orient="records")


# when the next card button is clicked, the flip_time should stop and recalculate
# new card with a French word is displayed and then the flip_time can start recalculation
# if "next" is clicked before 3seconds is over, the flip_time stops calculating the 3secs for the old card
# and starts calculating the new card
def next_card():
    global current_card, flip_time
    window.after_cancel(flip_time)
    current_card = random.choice(learn_words)
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_text, text=current_card["French"], fill="black")
    canvas.itemconfig(card_background, image=front_image)
    flip_time = window.after(3000, func=flip_card)


# deals with what happens when the card flips
def flip_card():
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_text, text=current_card["English"], fill="white")
    canvas.itemconfig(card_background, image=back_image)


# when the "tick" button is clicked, it means the user is familiar with the word, then the word is removed
# also a new csv file is created(words_to_learn) which now stores all data from the french_words.csv excluding
# the words that the user is already familiar with
# then anytime the user clicks the "tick" button again, the familiar words keep getting deleted from the
# (words_to_learn) file. We do not want to delete from the main csv file(french_words) file because it is the first
# file a new user starts with
# and then next_card() is called
def known_words():
    learn_words.remove(current_card)
    the_data = pandas.DataFrame(learn_words)
    the_data.to_csv("./data/words_to_learn", index=False)

    next_card()


# Configure the window/U.I set_up
window = Tk()
window.title("Learn French With Flashes")
window.config(padx=50, pady=50, background=BACKGROUND_COLOR)

# In 3seconds, the card flips to the translated version
flip_time = window.after(3000, func=flip_card)

# canvas setup
canvas = Canvas(width=800, height=526)
front_image = PhotoImage(file="./images/card_front.png")
back_image = PhotoImage(file="./images/card_back.png")
card_background = canvas.create_image(410, 270, image=front_image)
card_title = canvas.create_text(400, 150, text="", font=("Arial", 40, "italic"))
card_text = canvas.create_text(400, 263, text="", font=("Arial", 60, "bold"))
canvas.config(background=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=2)

# the "X" button setup
image_cross = PhotoImage(file="./images/wrong.png")
wrong_button = Button(image=image_cross, highlightthickness=0, command=next_card)
wrong_button.grid(row=1, column=0)

# the "tick" button setup
image_check = PhotoImage(file="./images/right.png")
right_button = Button(image=image_check, highlightthickness=0, command=known_words)
right_button.grid(row=1, column=1)

# call next card here, so we already start with the first random card selection
# so the text for card_title and card_text in the UI creation does not matter anymore

# aids to immediately display the first card upon app opening
next_card()

window.mainloop()