from ytmusicapi import YTMusic
import vlc
import tkinter as tk
from yt_dlp import YoutubeDL
import os

name= "Music.mp4"

# start

count = 0
def play_video():
	media_player.play()
	root.after(1000, update_slider)


def set_video_time(val):
	global count
	if count == 0:
		time_position = int(val)
		media_player.set_time(time_position)
	else:
		count += -1


def update_slider():
	global count
	count += 1

	video_length = media_player.get_media().get_duration()
	if video_length > 0:
		slider.config(to=video_length)
		current_time = media_player.get_time()
		slider.set(current_time)


	root.after(1000, update_slider)


def change_video():
	ytmusic = YTMusic("oauth.json")

	search_results = ytmusic.search(video_path_entry.get())
	os.remove("Music.mp4")

	name = f"Music.mp4"
	print(name)
	options = {
		'outtmpl': name,
	}

	URLS = [f'https://www.youtube.com/watch?v={search_results[0]["videoId"]}']
	with YoutubeDL(options) as ydl:
		print(ydl.download(URLS))

	video_path = name
	media = vlc_instance.media_new(video_path)
	media_player.set_media(media)
	play_video()


root = tk.Tk()
root.title("MP4 Video Player")
root.geometry("640x480")

video_canvas = tk.Canvas(root, bg="black", width=640, height=360)
video_canvas.pack()

vlc_instance = vlc.Instance()
media_player = vlc_instance.media_player_new()

video_file = name
media = vlc_instance.media_new(video_file)
media_player.set_media(media)

media_player.set_hwnd(video_canvas.winfo_id())

play_button = tk.Button(root, text="Play", command=play_video)
play_button.pack()

slider = tk.Scale(root, from_=0, to=1, orient=tk.HORIZONTAL,
				  command=set_video_time)
slider.pack(fill=tk.X)

video_path_label = tk.Label(root, text="Enter video path:")
video_path_label.pack()

video_path_entry = tk.Entry(root)
video_path_entry.pack(fill=tk.X)

change_video_button = tk.Button(root, text="Change Video", command=change_video)
change_video_button.pack()

root.mainloop()
