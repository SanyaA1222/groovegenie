import threading
import tkinter as tk

import cv2

from MovementDetection import process_frame


def start_countdown():
    # create animated text, but hide it initially
    button2.config(state=tk.DISABLED)
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
        countdown.set("Start Grooving!")
        # remove countdown_label and show song_label
        countdown_label.place_forget()
        song_label.pack()
        canvas.pack()
        slider.pack(fill=tk.X)
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



if __name__ == "__main__":
    root = tk.Tk()
    root.state('zoomed')

    gg1 = tk.PhotoImage(file="gg1crop.png")
    gg2 = tk.PhotoImage(file="gg2crop.png")
    small_gg1 = gg1.subsample(1, 1)
    small_gg2 = gg2.subsample(1, 1)
    logo_label = tk.Label(root, image=small_gg1, borderwidth=0, bg="#e3f3f3")
    logo_label.place(relx=0.5, rely=0.2, anchor=tk.CENTER)
    logo_label.pack()

    song = tk.StringVar()
    song.set("Bohemian Rapsody")  # set song name variable here

    # create song label, but hide it initially
    song_label = tk.Label(root, text="Geenie plays...{}".format(song.get()),
                          bg="#e3f3f3", font=("Arial", 12))
    song_label.config(highlightthickness=0)

    # create start button
    button2 = tk.Button(root, text="Start", command=start_countdown)
    button2.pack()

    # create canvas
    canvas = tk.Canvas(root, bg="black", width=480, height=480)

    #slider for duration of music
    slider = tk.Scale(root, from_=0, to=1, orient=tk.HORIZONTAL)


    cap = cv2.VideoCapture(0)
    stop_event = threading.Event()

    # Start the frame processing thread
    process_thread = threading.Thread(target=process_frame,
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
