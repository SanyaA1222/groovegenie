import MovementDetection
import songclassification

# Random Frequency is per 1 min

"""
Join the Audiance feedback to  the scores of the song
- We check if the audiance have a similar response to the song's expection. 
"""

audianceScore = MovementDetection.avgScore
# Score of the previous song
scoreOfSong = 0
songName = ""
goodSongs = []
scoreToMusic = {}


def songOver():
    MovementDetection.scoresOfThisSong = [0]
    difference = abs(MovementDetection.avgScore - scoreOfSong)
    global goodSongs

    if (len(goodSongs) < 11):
        goodSongs.append((difference, songName))
    else:
        if goodSongs[9][0] > difference:
            goodSongs.pop(9)
            goodSongs.append((difference, songName))
            goodSongs = sorted(goodSongs, key=lambda x: x[0])
    getSong()


def getSong():
    """
    Update the scoreofSong

    """
    if len(goodSongs) == 10:
        similarSong(goodSongs)
    else:
        song_movement(audianceScore)

    pass


def playSong():
    # play the song

    songOver()



