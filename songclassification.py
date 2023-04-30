import csv
import numpy as np
import random

song_scores = {}
names = {}

class Song:
    def __init__(self, name, genre, danceability, energy, liveliness, tempo):
        self.name = name
        self.genre = genre
        self.danceability = danceability
        self.energy = energy
        self.liveliness = liveliness
        self.tempo = tempo
        self.similarity = float('inf')


# 0: Dancebility, 1: Energy, 8: Liveliness, 10: Tempo, 18: Genre, 19: Song Name
def calculate_score():
    with open('genres_v2.csv', 'r', encoding="utf8") as csv_file:
        reader = csv.reader(csv_file)

        global song_scores
        global names

        i = 0
        for row in reader:
            if i == 0:
                i += 1
                continue
            score = 0
            score += (float(row[0]) * 10) * 2
            score += float(row[1]) * 10
            score += float(row[8]) * 10
            score += (float(row[10]) - 57) / 16.4
            score /= 5
            names[row[19]] = Song(row[19], row[18], float(row[0]), float(row[1]), float(row[8]), float(row[10]))
            if score not in song_scores:
                song_scores[score] = [Song(row[19], row[18], float(row[0]), float(row[1]), float(row[8]), float(row[10]))]
            else:
                song_scores[score].append(Song(row[19], row[18], float(row[0]), float(row[1]), float(row[8]), float(row[10])))


def get_genres():
    with open('genres_v2.csv', 'r') as csv_file:
        reader = csv.reader(csv_file)
        genres = []
        for row in reader:
            if row[18] not in genres:
                genres.append(row[18])
    return genres


def generate_playlist(genre_selections: list):
    global song_scores
    for key, value in song_scores.items():
        song_scores[key] = [elem for elem in value if elem.genre in genre_selections]


def similarSong(good_songs: list, audience_score: int):
        global song_scores
        global names
        min_song = None
        min_sim = float('inf')
        for key, value in song_scores.items():
            for song in value:
                similarity = 0
                for saved in good_songs:
                    similarity += (abs(song.danceability - names[saved[1]].danceability))
                    similarity += (abs(song.energy - names[saved[1]].energy))
                    similarity += (abs(song.liveliness - names[saved[1]].liveliness))
                    similarity += (abs(song.tempo/100 - names[saved[1]].tempo/100))
                song.similarity = similarity
                if similarity < min_sim and (audience_score - 1 < key < audience_score + 1):
                    min_sim = similarity
                    min_song = song
        if min_song is None:
            return song_movement(audience_score)
        else:
            return min_song.name


def song_movement(audience_score: int):
    global song_scores
    songs_selected = 0
    keys = [key for key in song_scores.keys()]
    value = audience_score
    songs = []

    i = 0
    while len(songs) <= 50:
        diff = [abs(value - i) for i in keys]
        index = np.argmin(diff)
        closest_value = keys[index]
        songs.extend([song.name for song in song_scores[closest_value]])
        keys.pop(index)
        i+= 1
        if i == 100:
            break

    ret_idx = random.randint(0, len(songs)-1)
    return songs[ret_idx]
