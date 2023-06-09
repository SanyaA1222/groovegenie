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

on_song_end = play_video

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
		if video_length - 3000 < media_player.get_time():
			on_song_end()
			return
		current_time = media_player.get_time()
		slider_global.set(current_time)


	root_global.after(1000, update_slider)


def change_video(song_name):
	global music_name
	media_player.stop()
	slider_global.set(0)

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
	try:
		URLS = [f'https://www.youtube.com/watch?v={search_results[0]["videoId"]}']
	except:
		URLS = ["https://www.youtube.com/watch?v=fJ9rUzIMcZQ"]
		song_label_global.config(text=f"Geenie plays...Bohemian Rhapsody")

	with YoutubeDL(options) as ydl:
		print(ydl.download(URLS))
	music_name = search_results[0]["title"]
	video_path = name
	media = vlc_instance.media_new(video_path)
	media_player.set_media(media)
	slider_global.config()
	play_video()



def start(slider, root, song_label, on_song_end_t):
	global vlc_instance, media_player, slider_global, root_global, song_label_global, on_song_end
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

	on_song_end = on_song_end_t
# hide_root.mainloop()
