import MovementDetection

# Random Frequency is per 1 min
songsPlayed = 0
randomFrequency = 1
audianceScore = MovementDetection.avgScore
scoresOfTheNight = [audianceScore]
scoreToMusic = {}


def updateRandomFrequency():
	# Update the random Testing the waters frequency based on the numbers of songs played
	pass


def songOver():
	MovementDetection.scoresOfThisSong = []
	global songsPlayed
	songsPlayed += 1
	updateRandomFrequency()


def getSong():
	# if it is the time to test the waters using the random song play a random song. Use random frequency.
	pass


def playSong():
	# play the song
	songOver()
