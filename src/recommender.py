import pandas as pd
import requests
import numpy as np


class Recommend(object):
    """docstring for Recommend."""
    def __init__(self, song_db):
        self.song_df = song_db
        self.X = song_db[['acousticness', 'instrumentalness', 'valence',
                     'danceability', 'energy']].values
        self.dislike_pl = []
        self.dislike_data = []
        self.like_dist = np.zeros((len(song_db), 0))
        self.dislike_dist = np.zeros((len(song_db), 0))

    def get_playlist_data(self, track_ids, access_token):
        '''Takes the user's selected playlist and
           returns data for all tracks (up to 100)'''
        self.like_pl = track_ids
        r = requests.get("https://api.spotify.com/v1/audio-features/?ids={0}".format(','.join(track_ids)),
                         headers={'Authorization': 'Bearer {}'.format(access_token)})
        if r.status_code == 200:
            track_data = r.json()
            self.playlist = pd.DataFrame(track_data['audio_features'])
            self.like_dist = self.calc_dist_mat(self.playlist)
            self.song_df = self.song_df.append(self.playlist, ignore_index=True)
            self.song_df.drop_duplicates(inplace=True)
            self.played = [self.song_df.index[self.song_df['id']==track][0] for track in track_ids]

        else:
            raise IOError('Spotify API request unsuccessful. \
                           Status code:{}'.format(r.status_code))

    def data_as_array(self, df):
        return df[['acousticness', 'instrumentalness', 'valence',
                     'danceability', 'energy']].values

    def calc_dist_mat(self, songs):
        song_data = self.data_as_array(songs)
        return np.sqrt(((song_data - self.X[:, np.newaxis, :])**2).sum(axis=2))

    def like_song(self, track):
        self.played.append(self.song_df.index[self.song_df['id']==track][0])
        self.like_pl.append(track)
        row_data = self.song_df[self.song_df['id']==track]
        self.playlist.append(row_data, ignore_index=True)
        self.like_dist = self.calc_dist_mat(self.playlist)

    def dislike_song(self, track):
        self.played.append(self.song_df.index[self.song_df['id']==track][0])
        self.dislike_pl.append(track)
        self.dislike_data.append(self.song_df[self.song_df['id']==track].to_dict(orient='records')[0])
        self.dislike_df = pd.DataFrame(self.dislike_data)
        self.dislike_dist = self.calc_dist_mat(self.dislike_df)

    def recommend(self, heart_rate=None):
        like_total_dist = self.like_dist.sum(axis=1)
        dislike_total_dist = self.dislike_dist.sum(axis=1)
        total_dist = like_total_dist - dislike_total_dist

        # sorts from smallest to largest dist
        most_similar = np.argsort(total_dist)
        for i in most_similar:
            if i not in self.played:
                self.played.append(i)
                return (self.song_df.iloc[i]['song'],
                        self.song_df.iloc[i]['artist'],
                        self.song_df.iloc[i]['id'])
