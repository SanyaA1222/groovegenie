import threading
import tkinter as tk

import cv2
import MovementDetection as MD
import musicPlayer

import songPlayAlgo

def start_countdown(checklist_genres):
    # create animated text, but hide it initially
    global selected_genres
    selected_genres = checklist_genres

    countdown = tk.StringVar()
    countdown.set("Ready to Groove?")
    countdown_label = tk.Label(root, textvariable=countdown, bg="#e3f3f3",
							   font=("Arial", 12))
    countdown_label.pack()
    root.after(1000, update_countdown, 3, countdown, countdown_label)


def update_countdown(count, countdown, countdown_label):
    if count == 3:
        countdown.set(str(count))
    elif count == 2:
        countdown.set(str(count))
    elif count == 1:
        countdown.set(str(count))
    elif count == 0:
        countdown.set("Selected Genres :" + ",".join(selected_genres))
        # remove countdown_label and show song_label
        countdown_label.place_forget()
        song_label.pack()
        canvas.pack()
        slider.pack(fill=tk.X)
        musicPlayer.change_video("What Do you mean")  # TODO remove this
        logo_label.after(0, animate_logo)
    else:
        return
    root.after(1000, update_countdown, count - 1, countdown, countdown_label)


def animate_logo():
    current_image = logo_label.cget("image")
    if current_image == "pyimage3":
        logo_label.config(image=small_gg2)
    else:
        logo_label.config(image=small_gg1)
    logo_label.after(500, animate_logo)

# set the selected options when the combobox is closed
def show_selected_genres():
    # Get the selected genres
    checklist_genres = []
    for genre_var in genre_vars :
        if len(genre_var.get()) > 1 :
            checklist_genres.append(genre_var.get())
    songPlayAlgo.starting(MD, checklist_genres)

    print("Selected Genres:", checklist_genres)


    # Close the dropdown
    genre_dropdown.destroy()
    genre_dropdown_button.destroy()
    start_countdown(checklist_genres)

def on_song_end():
    out = musicPlayer.change_video(songPlayAlgo.songOver())
    while out == 1:
        out = musicPlayer.change_video(songPlayAlgo.getSong())


def show_genre_dropdown():
    global genre_vars, genre_dropdown
    # Create the dropdown window
    genre_dropdown = tk.Toplevel()
    genre_dropdown.title("Select Genres")
    # Create the genre checkboxes
    genre_vars = []
    for genre in genres:
        var = tk.StringVar(value=genre in default_genres)
        genre_vars.append(var)
        cb = tk.Checkbutton(genre_dropdown, text=genre, variable=var, onvalue=genre, offvalue="",bg="#e3f3f3", fg="#3e4262")
        cb.pack(padx=10, pady=5, anchor="w")
    # Add an OK button to save the selected genres
    ok_button = tk.Button(genre_dropdown, text="OK", command=show_selected_genres,bg="#e3f3f3", fg="#3e4262")
    ok_button.pack(pady=10)
if __name__ == "__main__":
    root = tk.Tk()
    root.state('zoomed')

    gg1 = tk.PhotoImage(file="gg1crop.png")
    gg2 = tk.PhotoImage(file="gg2crop.png")
    small_gg1 = gg1.subsample(2, 2)
    small_gg2 = gg2.subsample(2, 2)
    logo_label = tk.Label(root, image=small_gg1, borderwidth=0, bg="#e3f3f3")
    logo_label.place(relx=0.5, rely=0.2, anchor=tk.CENTER)
    logo_label.pack()

    song = tk.StringVar()
    song.set("Bohemian Rapsody")  # set song name variable here

    # create song label, but hide it initially
    song_label = tk.Label(root, text="Geenie plays...{}".format(song.get()),
                          bg="#e3f3f3", font=("Arial", 12))
    song_label.config(highlightthickness=0)

    # create a list of options for the checklist
    genres = [ 'Dark Trap', 'Underground Rap', 'Trap Metal', 'Emo', 'Rap', 'RnB', 'Pop', 'Hiphop', 'techhouse', 'techno', 'trance', 'psytrance', 'trap', 'dnb', 'hardstyle']
    default_genres = ["Rock", "Pop", "Hip Hop"]
    # Create the genre label and dropdown button

    genre_dropdown_button = tk.Button(root, text="Select Genres",
                                       command=show_genre_dropdown,bg="#e3f3f3", fg="#3e4262")
    genre_dropdown_button.pack(pady=5)


    # create canvas
    canvas = tk.Canvas(root, bg="black", width=480, height=480)

    # slider for duration of music
    slider = tk.Scale(root, from_=0, to=1, orient=tk.HORIZONTAL)
    musicPlayer.start(slider, root, song_label, on_song_end)

    cap = cv2.VideoCapture(0)
    stop_event = threading.Event()

    # Start the frame processing thread
    process_thread = threading.Thread(target=MD.process_frame,
                                      args=(canvas, cap, stop_event))
    process_thread.start()


    def on_closing():
        stop_event.set()
        process_thread.join()
        cap.release()
        root.destroy()


    root.protocol("WM_DELETE_WINDOW", on_closing)

    root.title("groovegeenie")
    root.geometry("400x400")
    root.configure(bg="#e3f3f3")

    root.mainloop()
