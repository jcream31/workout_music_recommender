import pandas as pd
import time
from urllib.parse import quote
import requests
from auth import Token
import pickle


'''Functions for generating a database of songs'''

def get_top_tracks(artist_id):
    '''Takes the artist_id returned from get_artist_id()
       and returns a dictionary where keys are track ids
       and values are the track name'''

    r = requests.get("https://api.spotify.com/v1/artists/{0}/top-tracks?country=US".format(artist_id),
                    headers={'Authorization': 'Bearer {}'.format(token['access_token'])})
    if r.status_code == 200:
        top_tracks = {}
        for tracks_dict in r.json()['tracks']:
            top_tracks[tracks_dict['id']] = tracks_dict['name']
        return top_tracks
    else:
        raise IOError('Spotify API request unsuccessful. \
                       Status code:{}'.format(r.status_code))

def generate_track_df(artist_list):
    '''Takes the list of artist tuples (artist_id, artist_name),
       fetches top tracks for each artists, and returns df
       of songs with their artists'''
    songs = []
    refresh_token = 0
    for art_id, art_name in artist_list:
        if refresh_token%10 == 0:
            token = authorization.get_token()
        top_tracks = get_top_tracks(art_id)
        if not top_tracks:
            continue
        else:
            for song_id, song_name in top_tracks.items():
                songs.append({'artist':art_name, 'song':song_name,
                              'artist_id':art_id, 'song_id':song_id})
        time.sleep(2)
        refresh_token += 1
    return pd.DataFrame(songs)


def get_track_features(track_id):
    r = requests.get("https://api.spotify.com/v1/audio-features/{0}".format(track_id),
                     headers={'Authorization': 'Bearer {}'.format(token['access_token'])})
    if r.status_code == 200:
        return r.json()
    else:
        raise IOError('Spotify API request unsuccessful. \
                       Status code:{}'.format(r.status_code))

if __name__ == "__main__":
    authorization = Token()
    authorization.load_secrets()
    token = authorization.get_token()
    # artists is a list of tuples: (artist_id, artist_name)
    # with open ('artists.p','rb') as fp:
    #     artists = pickle.load(fp)
    #
    # track_df = generate_track_df(artists)
    # with open ('tracks.p','wb') as fp:
    #     pickle.dump(track_df, fp)

    with open ('tracks.p','rb') as fp:
        track_df = pickle.load(fp)

    error_file = open("error_songs.txt", "w")
    refresh_token = 0
    track_data = []
    for song in track_df['song_id']:
        print (song)
        if refresh_token%10==0:
            token = authorization.get_token()
        try :
            track_data.append(get_track_features(song))
        except ValueError:
            print("problem with song {}".format(song))
            error_file.write(i[0])
            continue
        refresh_token += 1
        time.sleep(2)
    error_file.close()
    song_df = pd.DataFrame(track_data)
    with open('track_data.p', 'wb') as fp:
        pickle.dump(song_df, fp)
