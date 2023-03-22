from matplotlib import artist
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
import spotipy.util as util
from secrets import cid, secret
from functions import *

    

class Spotify():
    """Spotify class that contains plenty of methods to handle your user or retrieve data"""
    
    def __init__(self, cid, secret) -> None:

        self.cid = cid
        self.secret = secret

        scope = 'user-read-private'      
   
        # Get the token so we don't need to access every time
        token = util.prompt_for_user_token(scope, client_id=self.cid, client_secret=self.secret)
        sp = spotipy.Spotify(auth=token)
        
        self.username, self.followers, self.id = try_to_login(sp)       
    
   
    def get_username(self):
        """Returns the username of the profile"""
        return self.username

   
    def get_number_of_followers(self):
        """Returns the numnber of followers that the profile has"""
        return self.followers    
    

    def get_liked_songs_artists(self):
        """Returns all the artitsts of your liked songs"""
        scope = 'user-library-read'
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, client_id=self.cid, client_secret=self.secret))
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


    def print_song_playing_now(self):
        scope = 'user-read-playback-state'
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, client_id=self.cid, client_secret=self.secret))
        
        artists = None


        try:
            artists = sp.current_user_playing_track()['item']['album']['artists'] # A song is playing
        except:
            print('No song is playing now')
        
        if artists:
            # name/s of the/- artist/s
            names = []
            for artist in artists:
                names.append(artist['name'])
        
            # song name 
            song_name  = sp.current_user_playing_track()['item']['name']
        
            print(f'Now is Playing: {song_name}')
            print('Artists: ', *names)  


    def return_top_songs(self, return_ids=False):
            scope = 'user-top-read'
            sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, client_id=self.cid, client_secret=self.secret))

            results = sp.current_user_top_tracks(limit=50, time_range="long_term")
            top_tracks = results['items']

            while results['next']:
                results = sp.next(results)
                top_tracks.extend(results['items']['name'])
            
            tracks_to_return = []
            tracks_to_return_id = []
            for top_track in top_tracks:
                print(top_track['id'])
                tracks_to_return.append(top_track['name'])
            
            if return_ids:
                return tracks_to_return, tracks_to_return_id
            else:
                return tracks_to_return
                                      

    def get_saved_albums(self):
        scope = 'playlist-read-private'
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, client_id=self.cid, client_secret=self.secret))
        
        playlists = sp.current_user_playlists()
        playlist_names = [playlist['name'] for playlist in playlists['items']]
        print(playlist_names)

sp = Spotify(cid, secret)

plot_artists_with_most_songs(sp.get_liked_songs_artists())

sp.get_saved_albums()