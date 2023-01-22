from tkinter import *
import math
# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
LIGHT_RED = "#FFCAC8"
RED = "#FF9E9E"
MINT = "#C0EEE4"
DARKER_GREEN = "#5AA469"
NAVY = "#2B3A55"
YELLOW = "#F8F988"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
# ---------------------------- GLOBAL VARIABLES ------------------------------- #
reps = 0
timer = None

# ---------------------------- TIMER RESET ------------------------------- #


def reset_timer():
    global reps
    reps = 0
    window.after_cancel(timer)
    canvas.itemconfig(timer_text, text="00:00")
    track_label["text"] = ""

    button["text"] = START_TEXT
    button["command"] = start_timer
    mode_label["text"] = "TIMER"


# ---------------------------- TIMER MECHANISM ------------------------------- #
def start_timer():
    mode_label["text"] = "STUDY"
    button["text"] = STOP_TEXT
    count_down(WORK_MIN*60)
    window.attributes('-topmost', False)
    button["command"] = stop_timer


def stop_timer():
    reset_timer()


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def count_down(count):
    global reps, timer

    if reps >= 8:
        reset_timer()
        window.attributes('-topmost', True)
        return
    mins = math.floor(count/60)
    secs = count % 60

    if secs < 10:
        temp_str = f"0{secs}"
        secs = temp_str
    if mins < 10:
        temp_str = f"0{mins}"
        mins = temp_str

    canvas.itemconfig(timer_text, text=f"{mins}:{secs}")

    # At the end of each session, reps = reps + 1
    if count == 0:
        reps += 1
        if reps == 7:
            count = LONG_BREAK_MIN * 60
            mode_label["text"] = "LONG BREAK"
            mode_label["font"] = (FONT_NAME, 20, "bold")
            change_bg_color(MINT)

        elif reps % 2:  # reps == 1 or reps == 3 or reps == 5:
            count = SHORT_BREAK_MIN * 60
            track_label["text"] += "✔"
            mode_label["text"] = "SHORT BREAK"
            mode_label["font"] = (FONT_NAME, 20, "bold")
            change_bg_color(MINT)
        elif reps % 2 == 0:  # reps == 0 or reps == 2 or reps == 4 or reps == 6:
            count = WORK_MIN * 60
            mode_label["text"] = "STUDY"
            change_bg_color(YELLOW)

    timer = window.after(1, count_down, count - 1)


# ---------------------------- UI SETUP ------------------------------- #
def change_bg_color(color):
    canvas["bg"] = color
    window["bg"] = color
    mode_label["bg"] = color
    track_label["bg"] = color


window = Tk()
window.title("Pomodoro")
window.config(padx=100, pady=50, bg=YELLOW)

canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)  # create canvas
tomato_img = PhotoImage(file="tomato.png")  # read file to get hold of an image of that particular file
canvas.create_image(100, 112, image=tomato_img)  # add image to canvas, 102 so tomato is positioned to the right
# and not cut off on the left
timer_text = canvas.create_text(102, 125, text="00:00", font=(FONT_NAME, 30, "bold"), fill=MINT)
canvas.grid(row=1, column=1)

mode_label = Label(text="TIMER", font=(FONT_NAME, 32, "bold"), fg=RED, bg=YELLOW)
mode_label.grid(row=0, column=1)

START_TEXT = "▶ Start"
STOP_TEXT = "⏹ Stop"
cmd_list = [START_TEXT, STOP_TEXT]

click_val = 0
button = Button(text=cmd_list[click_val], font=(FONT_NAME, 15, "bold"), fg=NAVY, bg=RED)
button.grid(row=3, column=1, pady=20)
button["command"] = start_timer

track_label = Label(font=(FONT_NAME, 15, "bold"), fg=DARKER_GREEN, bg=YELLOW)
track_label.grid(row=4, column=1)


window.mainloop()  # get window to show up
