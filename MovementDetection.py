import cv2
import numpy as np
import tkinter as tk
from PIL import Image, ImageTk
from collections import deque
import threading


def create_heatmap(movement_map, gamma=1.5):  # Adjust the gamma value as needed
    movement_map_gamma = np.power(movement_map, gamma)
    movement_map_8bit = np.uint8(
        255 * (movement_map_gamma / np.max(movement_map_gamma)))
    heatmap = cv2.applyColorMap(movement_map_8bit, cv2.COLORMAP_JET)
    heatmap[movement_map_8bit < 50] = 0  # Adjust the threshold as needed
    return heatmap


def update_canvas(canvas, frame):
    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()

    # Resize the frame to match the canvas size
    resized_frame = cv2.resize(frame, (canvas_width, canvas_height))
    resized_frame = cv2.cvtColor(resized_frame,
                                 cv2.COLOR_BGR2RGB)  # Convert BGR to RGB

    img = Image.fromarray(resized_frame)
    imgtk = ImageTk.PhotoImage(image=img)
    canvas.create_image(0, 0, anchor=tk.NW, image=imgtk)
    canvas.image = imgtk


def process_frame(canvas, cap, stop_event):

    total_movement = 0
    frame_count = 0
    prev_gray_frame = None
    running_avg_buffer = deque(
        maxlen=30)  # Circular buffer for 30-frame running average

    while not stop_event.is_set():
        ret, frame = cap.read()
        if not ret:
            return

        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray_frame = cv2.GaussianBlur(gray_frame, (21, 21), 0)

        if prev_gray_frame is not None:
            frame_delta = cv2.absdiff(prev_gray_frame, gray_frame)
            thresh = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]
            thresh = cv2.dilate(thresh, None, iterations=2)
            movement = np.sum(thresh) // 255

            movement_map = thresh

            total_movement += movement
            frame_count += 1
            running_avg_buffer.append(
                movement)  # Add the movement to the buffer

            heatmap = create_heatmap(movement_map)
            overlaid_frame = cv2.addWeighted(frame, 0.7, heatmap, 0.3, 0)
            update_canvas(canvas, overlaid_frame)

            # Calculate and print the 30-frame running average of the average movement
            running_avg_movement = np.mean(running_avg_buffer)
            print(
                f"30-frame running average movement for frame {frame_count}: {running_avg_movement}")

        prev_gray_frame = gray_frame.copy()


def temp():
    pass


def main():
    cap = cv2.VideoCapture("walking.mp4")
    ret, frame = cap.read()

    root = tk.Tk()
    canvas = tk.Canvas(root, width=1000, height=1000)
    print(frame.shape, frame.shape)
    canvas.pack()

    stop_event = threading.Event()

    # Start the frame processing thread
    process_thread = threading.Thread(target=process_frame,
                                      args=(canvas, stop_event))
    process_thread.start()

    def on_closing():
        stop_event.set()
        process_thread.join()
        cap.release()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()


if __name__ == "__main__":
    main()
