import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
import spotipy.util as util
from secrets import cid, secret
from functions import *
    

class Spotify():
    """Spotify class that contains plenty of methods to handle your user or retrieve data"""
    
    def __init__(self, cid, secret) -> None:
        scope = 'user-read-private'

    
        # Get the token so we don't need to access 
        token = util.prompt_for_user_token(scope, client_id=cid, client_secret=secret)
        sp = spotipy.Spotify(auth=token)
        
        self.username = sp.me()['display_name']
        self.followers = sp.me()['followers']['total']

        print(f"Congratulations! You have been connected to a spotify account with the username {self.username}")
    
   
    def get_username(self):
        """Returns the username of the profile"""
        return self.username

   
    def get_number_of_followers(self):
        """Returns the numnber of followers that the profile has"""
        return self.followers    
    

    def get_likedd_songs_artists(self):
        """Returns all the artitsts of your liked songs"""
        scope = 'user-library-read'
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, client_id=cid, client_secret=secret))
        offset = 1
        tracks = sp.current_user_saved_tracks(limit=50)['items']
        singers = []
        
        results = sp.current_user_saved_tracks()
        tracks = results['items']
        while results['next']:
            results = sp.next(results)
            tracks.extend(results['items'])

        for truck in tracks:
            for artist in truck['track']['artists']:
                singers.append(artist['name'])

        return singers