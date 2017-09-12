import pickle
import pandas as pd
import numpy as np

# open saved artist and track data:
# track data includes all features of music
with open ('../data/track_data.p', 'rb') as fp:
    track_data = pickle.load(fp)

# tracks includes artist and song names w ID's
with open ('../data/tracks.p', 'rb') as fp:
    tracks = pickle.load(fp)

# merge artist and songs names with track data
data = pd.merge(track_data, tracks, how='left', left_on=['id'], right_on=['song_id'])

# drop any duplicated rows
data.drop_duplicates(keep='first', inplace = True)

with open ('../data/complete_data.p', 'wb') as fp:
    pickle.dump(data, fp)
