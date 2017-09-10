import yaml
import os
import requests

class Token(object):
    '''Functions to get access tokens from Spotify API
       yaml_loc will be private location of auth keys'''

    def __init__(self, yaml_loc = '.secrets/spotify_api.yaml', secrets = None):
        self.yaml_loc = yaml_loc
        self.secrets = secrets

    def load_secrets(self):
        '''Load Spotify Client ID and Client Secret '''
        secret_file = os.path.join(os.environ['HOME'], self.yaml_loc)
        with open(secret_file) as f:
            self.secrets = yaml.load(f)

    def get_token(self):
        """Get an access token for the Spotify API."""
        url = "https://accounts.spotify.com/api/token"
        payload = self.secrets.copy()
        payload['grant_type'] = 'client_credentials'

        r = requests.post(url, data=payload)
        return r.json()
