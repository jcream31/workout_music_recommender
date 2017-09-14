import pandas as pd
import requests


class Recommend(object):
    """docstring for Recommend."""
    def __init__(self, song_db):
        self.song_db = song_db
        self.like_pl = []
        self.dont_like_pl = []

    def add_playlist(self, playlist):
        self.playlist = playlist

    def data_as_array(df):
        self.X = df[['acousticness', 'instrumentalness', 'valence',
                     'danceability', 'energy']].values

    def calc_dist_mat(self):
        pass

    def like_song(self, track):
        pass

    def dont_like_song(self, track):
        pass

    def recommend(self):
        pass

    def get_playlist_data(self, track_ids, access_token):
        '''Takes the user's selected playlist and
           returns data for all tracks (up to 100)'''

        r = requests.get("https://api.spotify.com/v1/audio-features/?ids={0}".format(','.join(track_ids)),
                         headers={'Authorization': 'Bearer {}'.format(access_token)})
        if r.status_code == 200:
            track_data = r.json()
            return pd.DataFrame(track_data['audio_features'])
        else:
            raise IOError('Spotify API request unsuccessful. \
                           Status code:{}'.format(r.status_code))
