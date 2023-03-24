from matplotlib import artist
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
import spotipy.util as util
from secrets import cid, secret
from functions import *
from typing import List
import os

    

class Spotify():
    """Spotify class that contains plenty of methods to handle your user or retrieve data"""
    
    def __init__(self, cid, secret) -> None:

        self.cid = cid
        self.secret = secret

        scope = 'user-read-private'     
   
        # Get the token so we don't need to access every time
        token = util.prompt_for_user_token(scope, client_id=self.cid, client_secret=self.secret)
        sp = spotipy.Spotify(auth=token)

        # Its possible to do this way, but we have to define the eniromental variables
        #username = '4qupay5ub5pzp1e6l5fiech73'
        # try:
        #    token = util.prompt_for_user_token(username)

        # except:
        #    os.remove(f".cache-{username}")
        #    token = util.prompt_for_user_token(username)

        self.username, self.followers, self.id = try_to_login(sp)      
   
    def get_username(self) -> str:
        """
        This function returns the username of the account that is used

        Args:
            None

        Returns: 
            str: The username of the linked account
        """
        return self.username

   
    def get_number_of_followers(self) -> int:
        """

        This function returns the number of the followers of the account that is used

        Args:
            None

        Returns:
            int: The number of followers of the linked account
        """
        return int(self.followers)    
    

    def get_liked_songs_artists(self) -> List[str]:
        """
        
        This function returns all the name of the artists that the user has liked
        
        Args:
            None
        
        Returns:
            List[stt]: The name of the artists that the linked account has liked"""
        scope = 'user-library-read'
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, client_id=self.cid, 
                                                       client_secret=self.secret))
        offset = 1
        tracks = sp.current_user_saved_tracks(limit=50)['items']
        singers = []
        
        results = sp.current_user_saved_tracks()
        tracks = results['items']
     
        while results['next']:
            results = sp.next(results)
            tracks.extend(results['items'])

        #for truck in tracks:
        #     for artist in truck['track']['artists']:
        #         singers.append(artist['name'])
        singers = [artist['name'] for track in tracks for artist in track['track']['artists']]

        return singers


    def print_song_playing_now(self) -> None:
        """

        This function prints if a song is playing at the account linked. If yes,
        It print tha name of the song and the artist/s

        Args:
            None

        Returns:
            None
        """
        scope = 'user-read-playback-state'
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, client_id=self.cid, 
                                                       client_secret=self.secret))
        
        artists = None


        try:
            artists = sp.current_user_playing_track()['item']['album']['artists'] # A song is playing
        except:
            print('No song is playing now')
        
        if artists:
            # name/s of the artist/s
            names = []

            names = [artist['name'] for artist in artists]
            #for artist in artists:
            #    names.append(artist['name'])
        
            # song name 
            song_name  = sp.current_user_playing_track()['item']['name']
        
            print(f'Now is Playing: {song_name}')
            print('Artists: ', *names)  


    def return_top_songs(self, return_ids=False) -> List[str]:
            """
            This functions returns the most played songs by the account in long term

            Args:
                None

            Returns:
                List[str]: The most played songs, in long term,  by the linked account 
            """
            scope = 'user-top-read'
            sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, client_id=self.cid, 
                                                           client_secret=self.secret))

            results = sp.current_user_top_tracks(limit=50, time_range="long_term")
            top_tracks = results['items']

            while results['next']:
                results = sp.next(results)
                top_tracks.extend(results['items']['name'])
            
            tracks_to_return_id = [top_track['id'] for top_track in top_tracks]
            tracks_to_return = [top_track['name'] for top_track in top_tracks]
            
            if return_ids:
                return tracks_to_return, tracks_to_return_id
            else:
                return tracks_to_return


    def return_recently_played(self):
        """"""
        scope = 'user-read-recently-played'
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, client_id=self.cid, 
                                                           client_secret=self.secret))

        results = sp.current_user_recently_played(limit=50)
        recent_tracks = results['items']

        print(len(recent_tracks))

        while results['next']:
                results = sp.next(results)
                recent_tracks.extend(results['items'])
        #print(type(results))
        #print(results.keys())
        print(len(recent_tracks))
        print(recent_tracks[1].keys())
        print(recent_tracks[1]['track'].keys())
        print(recent_tracks[1]['track']['id'])

        print("\n\n")
        print(recent_tracks[1]['played_at'])


                                      

    def get_saved_albums(self):
        scope = 'playlist-read-private'
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, client_id=self.cid, 
                                                       client_secret=self.secret))
        
        playlists = sp.current_user_playlists()
        playlist_names = [playlist['name'] for playlist in playlists['items']]
        print(playlist_names)

sp = Spotify(cid, secret)

#plot_artists_with_most_songs(sp.get_liked_songs_artists())

#sp.get_saved_albums()

#print(sp.return_top_songs())

sp.return_recently_played()

#print(sp.get_liked_songs_artists())




