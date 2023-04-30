from ytmusicapi import YTMusic
import ctypes

from yt_dlp import YoutubeDL
import os
import tkinter as tk

os.add_dll_directory(r'C:\Program Files\VideoLAN\VLC')
name = "Music.mp4"
music_name = ""
import vlc
# start
vlc_instance = None
media_player = None
slider_global = None
root_global = None
song_label_global = None
count = 0

def play_video():
	media_player.play()
	root_global.after(1000, update_slider)


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
		slider_global.config(to=video_length)
		current_time = media_player.get_time()
		slider_global.set(current_time)

	root_global.after(1000, update_slider)


def change_video(song_name):
	global music_name
	song_label_global.config(text=f"Geenie plays...{song_name}")

	ytmusic = YTMusic("oauth.json")

	search_results = ytmusic.search(song_name)
	try:
		os.remove("Music.mp4")
	except:
		pass
	name = f"Music.mp4"
	print(name)
	options = {
		'outtmpl': name,
	}

	URLS = [f'https://www.youtube.com/watch?v={search_results[0]["videoId"]}']
	with YoutubeDL(options) as ydl:
		print(ydl.download(URLS))
	music_name = search_results[0]["title"]
	video_path = name
	media = vlc_instance.media_new(video_path)
	media_player.set_media(media)
	play_video()


def start(slider, root, song_label):
	global vlc_instance, media_player, slider_global, root_global, song_label_global
	vlc_instance = vlc.Instance('--no-xlib')
	media_player = vlc_instance.media_player_new()

	video_file = name
	media = vlc_instance.media_new(video_file)
	media_player.set_media(media)
	hide_root = tk.Tk()
	hide_root.withdraw()

	video_canvas = tk.Canvas(hide_root, bg="black", width=640, height=360)
	video_canvas.pack()

	media_player.set_hwnd(video_canvas.winfo_id())

	slider.config(command=set_video_time)

	slider_global = slider
	root_global = root
	song_label_global = song_label
	#hide_root.mainloop()
