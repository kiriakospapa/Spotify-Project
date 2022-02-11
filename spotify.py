import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
import spotipy.util as util
import sys
from secrets import cid, secret
from functions import *
    

class Spotify():
    """Spotify class that contains plenty of methods to handle your user or retrieve data"""
    
    def __init__(self, cid, secret) -> None:
        scope = 'user-read-private'

    

        token = util.prompt_for_user_token(scope, client_id=cid, client_secret=secret)
        sp = spotipy.Spotify(auth=token)
        
        self.username = sp.me()['display_name']
        print(sp.me())
        self.followers = sp.me()['followers']['total']

        
        print(f"Congratulations! You have been connected to a spotify account with the username {self.username}")
    
   
    def get_username(self):
        return self.username

   
    def get_number_of_followers(self):
        return self.followers    
    

    def get_all_the_saved_tracks(self):
        scope = 'user-library-read'
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, client_id=cid, client_secret=secret))
        tracks = sp.current_user_saved_tracks(limit=50)['items']
        singers = []
        for truck in tracks:
            for artist in truck['track']['artists']:
                singers.append(artist['name'])
        
        return singers

ex = Spotify(cid, secret)
singers = ex.get_all_the_saved_tracks()

plot_artists_with_most_songs(singers=singers, n=6)



