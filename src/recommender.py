import pandas as pd
import requests
import numpy as np


class Recommend(object):
    """docstring for Recommend."""
    def __init__(self, song_db):
        self.song_df = song_db
        self.X = song_db[['acousticness', 'instrumentalness', 'valence',
                     'danceability', 'energy']].values
        # self.df_dist_mat = np.sqrt(((self.X  - self.X [:, np.newaxis, :])**2).sum(axis=2))
        self.like_pl = []
        self.dont_like_pl = []
        self.like_indices = []
        self.dislike_indices = []
        self.like_dist = np.zeros((len(song_db), 0))
        self.dont_like_dist = np.zeros((len(song_db), 0))

    def get_playlist_data(self, track_ids, access_token):
        '''Takes the user's selected playlist and
           returns data for all tracks (up to 100)'''
        self.playlist_ids = track_ids
        r = requests.get("https://api.spotify.com/v1/audio-features/?ids={0}".format(','.join(track_ids)),
                         headers={'Authorization': 'Bearer {}'.format(access_token)})
        if r.status_code == 200:
            track_data = r.json()
            self.playlist = pd.DataFrame(track_data['audio_features'])
        else:
            raise IOError('Spotify API request unsuccessful. \
                           Status code:{}'.format(r.status_code))

    # def add_playlist(self, playlist):
    #     self.playlist = playlist

    def data_as_array(self, df):
        return df[['acousticness', 'instrumentalness', 'valence',
                     'danceability', 'energy']].values

    def calc_dist_mat(self, songs):
        song_data = self.data_as_array(songs)
        return np.sqrt(((song_data - self.X[:, np.newaxis, :])**2).sum(axis=2))

    def like_song(self, track):
        self.like_pl.append(self.song_df[self.song_df['id']==track].to_dict(orient='records')[0])
        self.like_df = pd.DataFrame(self.like_pl)
        self.like_dist = self.calc_dist_mat(self.like_df)

    def dont_like_song(self, track):
        self.dont_like_pl.append(self.song_df[self.song_df['id']==track].to_dict(orient='records')[0])
        self.dont_like_df = pd.DataFrame(self.dont_like_pl)
        self.dont_like_dist = self.calc_dist_mat(self.dont_like_df)

    def recommend(self):

        # check if this is first recommendation
        if (not self.like_pl and not self.dont_like_pl):
            dist_mat = self.calc_dist_mat(self.playlist)
            total_dist = dist_mat.sum(axis=1)
        else:
            like_total_dist = self.like_dist.sum(axis=1)
            dont_like_total_dist = self.dont_like_dist.sum(axis=1)
            total_dist = like_total_dist - dont_like_total_dist

        # sorts from smallest to largest dist
        most_similar = np.argsort(total_dist)
        pl_indices = []
        for song in self.playlist_ids:
            try:
                pl_indices.append(self.song_df.index[self.song_df['id']==song].tolist()[0])
            except:
                continue

        try:
            self.like_indices = [self.song_df.index[self.song_df['id']==track_id][0] for track_id in self.like_df.id.values]
        except:
            pass
        try:
            self.dislike_indices = [self.song_df.index[self.song_df['id']==track_id][0] for track_id in self.dont_like_df.id.values]
        except:
            pass

        try:
            return (most_similar[0], self.like_indices[0], 1)
        except:
            for i in most_similar:
                if i not in pl_indices+self.like_indices+self.dislike_indices:
                    return (self.song_df.iloc[i]['song'],
                            self.song_df.iloc[i]['artist'],
                            self.song_df.iloc[i]['id'])
