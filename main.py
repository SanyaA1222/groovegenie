import tkinter as tk

def update_countdown(count):
    if count == 3:
        countdown.set(str(count))
    elif count == 2:
        countdown.set(str(count))
    elif count == 1:
        countdown.set(str(count))
    elif count == 0:
        countdown.set("Start!")
        # remove countdown_label and show song_label
        countdown_label.place_forget()
        song_label.pack()
        canvas.pack()
        logo_label.after(0, animate_logo)
    else:
        return
    root.after(1000, update_countdown, count-1)

def animate_logo():
    current_image = logo_label.cget("image")
    if current_image == "pyimage3":
        logo_label.config(image=small_gg2)
    else:
        logo_label.config(image=small_gg1)
    logo_label.after(500, animate_logo)

if __name__ == "__main__":
    root = tk.Tk()
    root.attributes('-fullscreen', True)

    gg1 = tk.PhotoImage(file="gg1crop.png")
    gg2 = tk.PhotoImage(file="gg2crop.png")
    small_gg1 = gg1.subsample(1, 1)
    small_gg2 = gg2.subsample(1, 1)
    logo_label = tk.Label(root, image=small_gg1, borderwidth=0, bg="#e3f3f3")
    logo_label.place(relx=0.5, rely=0.2, anchor=tk.CENTER)
    logo_label.pack()

    song = tk.StringVar()
    song.set("Bohemian Rapsody") #set song name variable here

    # create song label, but hide it initially
    song_label = tk.Label(root, text="Geenie plays...{}".format(song.get()), bg="#e3f3f3", font=("Arial", 14))
    song_label.config(highlightthickness=0)

    # create animated text
    countdown = tk.StringVar()
    countdown.set("Ready to Groove?")
    countdown_label = tk.Label(root, textvariable=countdown, bg="#e3f3f3", font=("Arial", 20))
    countdown_label.pack()
    root.after(1000, update_countdown, 3)

    # create canvas
    canvas = tk.Canvas(root, bg="black", width=480, height=480)
    canvas.pack()

    root.title("groovegeenie")
    root.geometry("400x400")
    root.configure(bg="#e3f3f3")

    root.mainloop()
