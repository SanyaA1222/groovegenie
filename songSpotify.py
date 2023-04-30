import spotipy
from spotipy.oauth2 import SpotifyOAuth

username = ''

# set up the authentication credentials
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id='1921a1f598f04490bf1e988e1db55f1f',
                                               client_secret='71b4dceadbed406cbae5f37d0dff2798',
                                               redirect_uri='https://personal-website.karanvirkhanna.repl.co/',
                                               scope='user-read-playback-state,user-modify-playback-state'))

# search for a track
results = sp.search(q='track:Imagine Dragons - Believer', type='track')
track_uri = results['tracks']['items'][0]['uri']

# start playback
sp.start_playback(uris=[track_uri])