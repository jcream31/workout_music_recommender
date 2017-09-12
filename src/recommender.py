class Recommend(object):
    """docstring for Recommend."""
    def __init__(self, arg):
        self.arg = arg

    def playlist_data(self, user, playlist):
        '''Takes the user's selected playlist and
           retursns data for all tracks'''

        r = requests.get("https://api.spotify.com/v1/users/{0}/playlists/{1}/tracks".format(user, playlist),
                         headers={'Authorization': 'Bearer {}'.format(token['access_token'])})
        if r.status_code == 200:
            return r.json()['artists']['items'][0]['id']
        else:
            raise IOError('Spotify API request unsuccessful. \
                           Status code:{}'.format(r.status_code))


    def calc_dist():


    def
