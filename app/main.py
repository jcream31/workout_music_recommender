### THIS CURRENTLY ONLY WORKS FOR PYTHON 2 ###

import json
from flask import Flask, request, redirect, g, render_template, session, jsonify
from flask_session import Session
import requests
import base64
import urllib
import sys
sys.path.append("../src")
from auth import Token
from recommender import Recommend
from plots import build_histograms


#  Client Keys
authorization = Token()
authorization.load_secrets()
CLIENT_ID = authorization.secrets['client_id']
CLIENT_SECRET = authorization.secrets['client_secret']

SESSION_TYPE = 'null'
app = Flask(__name__)
app.secret_key = authorization.secrets['app_key']
sess = Session()


# Spotify URLS
SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_API_BASE_URL = "https://api.spotify.com"
API_VERSION = "v1"
SPOTIFY_API_URL = "{}/{}".format(SPOTIFY_API_BASE_URL, API_VERSION)


# Server-side Parameters
CLIENT_SIDE_URL = "http://localhost"
PORT = 8765
REDIRECT_URI = "{}:{}/callback/q".format(CLIENT_SIDE_URL, PORT)
SCOPE = "playlist-modify-public playlist-modify-private"
STATE = ""
SHOW_DIALOG_bool = True
SHOW_DIALOG_str = str(SHOW_DIALOG_bool).lower()


auth_query_parameters = {
    "response_type": "code",
    "redirect_uri": REDIRECT_URI,
    "scope": SCOPE,
    "client_id": CLIENT_ID
}

@app.route("/")
def index():
    # Auth Step 1: Authorization
    url_args = "&".join(["{}={}".format(key,urllib.quote(val)) for key,val in auth_query_parameters.iteritems()])
    auth_url = "{}/?{}".format(SPOTIFY_AUTH_URL, url_args)
    return redirect(auth_url)


@app.route("/callback/q")
def callback():
    # Auth Step 4: Requests refresh and access tokens
    auth_token = request.args['code']
    code_payload = {
        "grant_type": "authorization_code",
        "code": str(auth_token),
        "redirect_uri": REDIRECT_URI
    }
    base64encoded = base64.b64encode("{}:{}".format(CLIENT_ID, CLIENT_SECRET))
    session['headers'] = {"Authorization": "Basic {}".format(base64encoded)}
    post_request = requests.post(SPOTIFY_TOKEN_URL, data=code_payload, headers=session['headers'])

    # Auth Step 5: Tokens are Returned to Application
    response_data = post_request.json()
    session['access_token'] = response_data["access_token"]
    session['refresh_token'] = response_data["refresh_token"]
    session['token_type'] = response_data["token_type"]
    session['expires_in'] = response_data["expires_in"]

    # Auth Step 6: Use the access token to access Spotify API
    session['auth_header'] = {"Authorization":"Bearer {}".format(session['access_token'])}

    # Get profile data
    user_profile_api_endpoint = "{}/me".format(SPOTIFY_API_URL)
    profile_response = requests.get(user_profile_api_endpoint, headers=session['auth_header'] )
    profile_data = profile_response.json()
    session['profile_href'] = profile_data["href"]

    return render_template("index.html")


@app.route("/playlists")
def playlists():
    # Get user playlist data
    playlist_api_endpoint = "{}/playlists".format(session['profile_href'])
    playlists_response = requests.get(playlist_api_endpoint, headers=session['auth_header'])
    playlist_data = playlists_response.json()

    # Combine profile and playlist data to display
    pl_owners = []
    pl_names  = []
    pl_ids    = []
    pl_images = []
    for pl in playlist_data['items']:
        pl_owners.append(pl['owner']['id'])
        pl_names.append(pl['name'])
        pl_ids.append(pl['id'])
        pl_images.append(pl['images'][0]['url'])
    playlists = zip(pl_owners, pl_ids, pl_names, pl_images)
    return render_template("playlists.html",playlists=playlists)

@app.route('/playlist_data/<pl_owner>/<pl_id>', methods=['GET', 'POST'])
def playlist_data(pl_owner, pl_id):

    # Get playlist data
    #  E.G. profile data['href']="https://api.spotify.com/v1/users/wizzler"
    pl_track_endpoint = "https://api.spotify.com/v1/users/{0}/playlists/{1}/tracks".format(pl_owner, pl_id)
    pl_track_response = requests.get(pl_track_endpoint, headers=session['auth_header'])
    if pl_track_response.status_code != 200:
        raise IOError(pl_track_endpoint + ' ' + pl_track_response.content)
    pl_tracks= pl_track_response.json()

    track_names   = []
    track_ids     = []
    track_artists = []
    for track in pl_tracks['items']:
        track_names.append(track['track']['name'])
        track_ids.append(track['track']['id'])
        temp = []
        for artist in track['track']['artists']:
            temp.append(artist['name'])
        track_artists.append(', '.join(temp))
    tracks = zip(track_ids, track_names, track_artists)
    recommender.get_playlist_data(track_ids, session['access_token'])
    # resp = recommender.get_playlist_data(track_ids, session['access_token'])

    # return render_template('tracks.html', tracks = resp)
    return render_template('tracks.html',
                            plot_url = build_histograms(recommender.playlist),
                            tracks = tracks)

@app.route('/recommendations', methods=['GET', 'POST'])
def recommendations():
    suggestion = recommender.recommend()
    return render_template('recommender.html', rec = suggestion)

@app.route('/like_song/<track_id>', methods=['GET', 'POST'])
def like_song(track_id):
    recommender.like_song(track_id)
    return (''), 204

@app.route('/dislike_song/<track_id>', methods=['GET', 'POST'])
def dislike_song(track_id):
    recommender.dislike_song(track_id)
    return (''), 204

if __name__ == "__main__":
    import cPickle as pickle
    with open ('../data/complete_data_py2.p', 'rb') as fp:
        song_db = pickle.load(fp)
    recommender = Recommend(song_db)
    app.run(debug=True,port=PORT)
