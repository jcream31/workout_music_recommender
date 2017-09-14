import pandas as pd
import requests
import numpy as np


class Recommend(object):
    """docstring for Recommend."""
    def __init__(self, song_db):
        self.song_df = song_db
        self.X = song_db[['acousticness', 'instrumentalness', 'valence',
                     'danceability', 'energy']].values
        self.df_dist_mat = np.sqrt(((self.X  - self.X [:, np.newaxis, :])**2).sum(axis=2))
        self.like_pl = []
        self.dont_like_pl = []

    # def add_playlist(self, playlist):
    #     self.playlist = playlist

    def data_as_array(df):
        self.X = df[['acousticness', 'instrumentalness', 'valence',
                     'danceability', 'energy']].values

    def calc_dist_mat(self, songs):
        song_data = data_as_array(songs)
        return np.sqrt(((song_data - self.X[:, np.newaxis, :])**2).sum(axis=2))

    def like_song(self, track):
        self.like_pl.append(self.song_df[self.song_df['id']==track].to_dict())
        return calc_dist_mat(pd.DataFrame(self.like_pl))

    def dont_like_song(self, track):
        self.dont_like_pl.append(self.song_df[self.song_df['id']==track].to_dict())
        return calc_dist_mat(pd.DataFrame(self.dont_like_pl))

    def recommend(self):
        # check if this is first recommendation
        if (not like_pl and not dont_like_pl):
            pl_data = self.data_as_array(self.playlist)
            dist_mat = self.calc_dist_mat(pl_data)
            return self.song_df.iloc[np.argmin(dist_mat, axis=0)]
        else:
            if like_pl:




        # else:

    def get_playlist_data(self, track_ids, access_token):
        '''Takes the user's selected playlist and
           returns data for all tracks (up to 100)'''

        r = requests.get("https://api.spotify.com/v1/audio-features/?ids={0}".format(','.join(track_ids)),
                         headers={'Authorization': 'Bearer {}'.format(access_token)})
        if r.status_code == 200:
            track_data = r.json()
            self.playlist = pd.DataFrame(track_data['audio_features'])
        else:
            raise IOError('Spotify API request unsuccessful. \
                           Status code:{}'.format(r.status_code))
