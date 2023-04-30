from songclassification import *

# Random Frequency is per 1 min

"""
Join the Audiance feedback to  the scores of the song
- We check if the audiance have a similar response to the song's expection. 
"""
audianceScore = 0
Movement = None
# Score of the previous song
scoreOfSong = 0
songName = ""
goodSongs = []
scoreToMusic = {}
calculate_score()
bound = 40
def starting(movement, checklist_genres):
    global bound
    global Movement, audianceScore
    Movement = movement
    audianceScore = Movement.avgScore
    generate_playlist(checklist_genres)

def songOver():
    global bound
    Movement.scoresOfThisSong = [0]
    difference = abs(Movement.avgScore - scoreOfSong)
    global goodSongs, audianceScore
    audianceScore = Movement.avgScore

    if (len(goodSongs) < bound + 2):
        goodSongs.append((difference, songName))
    else:
        if goodSongs[bound][0] > difference:
            goodSongs.pop(bound)
            goodSongs.append((difference, songName))
            goodSongs = sorted(goodSongs, key=lambda x: x[0])
    return getSong()


def getSong():
    global bound
    """
    Update the scoreofSong

    """
    if len(goodSongs) == bound + 1:
       return similarSong(goodSongs)
    else:
        return song_movement(audianceScore)



