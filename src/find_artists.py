from collections import defaultdict, deque
import pandas as pd
import time
from urllib.parse import quote
import requests
from auth import Token
import pickle


'''Functions for generating a database of artists'''
def build_query(artist):
    return quote(artist)

def get_artist_id(artist):
    '''Takes the encoded artist name from build_query()
       to fetch and return artist id from API'''

    r = requests.get("https://api.spotify.com/v1/search?q={0}&type=artist".format(artist),
                     headers={'Authorization': 'Bearer {}'.format(token['access_token'])})
    if r.status_code == 200:
        return r.json()['artists']['items'][0]['id']
    else:
        raise IOError('Spotify API request unsuccessful. \
                       Status code:{}'.format(r.status_code))

def get_related_artists(artist_id):
    '''Takes the artist_id returned from get_artist_id() and
       returns a dictionary where the keys are the related
       artist ids and the values are the artist names'''

    r = requests.get("https://api.spotify.com/v1/artists/{0}/related-artists".format(artist_id),
                    headers={'Authorization': 'Bearer {}'.format(token['access_token'])})
    if r.status_code == 200:
        related_artists = {}
        for artist_dict in r.json()['artists']:
            related_artists[artist_dict['id']] = artist_dict['name']
        return related_artists
    else:
        raise IOError('Spotify API request unsuccessful. \
                       Status code:{}'.format(r.status_code))

def generate_artists(artist_name, num_artists):
    query = build_query(artist_name)
    artist_id = get_artist_id(query)
    Q = deque()
    visited = []
    Q.append((artist_id, artist_name))
    while len(Q) != 0 and len(visited)<num_artists:
        v = Q.popleft()
        if v not in visited:
            visited.append(v)
            related_artists = get_related_artists(v[0])
            Q.extend(related_artists.items())
        time.sleep(2)
    return visited

if __name__ == "__main__":
    authorization = Token()
    authorization.load_secrets()
    token = authorization.get_token()
    # Pick diverse range of artists that people might work out to
    # and find 99 other related artists to each artist. This step is
    # broken up incase one fails
    df1 = generate_artists('Calvin Harris', 100)
    df2 = generate_artists('Beyonce', 100)
    df3 = generate_artists('2 Chainz', 100)
    df4 = generate_artists('Thirty Seconds To Mars', 100)
    df5 = generate_artists('Disturbed', 100)
    df6 = generate_artists('Macklemore', 100)
    df = list(set(df1+df2+df3+df4+df5+df6))

    # save songs
    with open('artists.p', 'wb') as fp:
        pickle.dump(df, fp)
