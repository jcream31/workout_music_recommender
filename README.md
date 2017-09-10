It's hard enough to get yourself to the gym after work when you're exhausted and your drive is at an all-time low. You usually rely on your favorite playlist to give you that extra boost to push through your workout, but what happens when those songs loose their kick? My workout music recommender uses the features of your current workout playlist to find similar songs and recommend them in real time based on your activity.

### Data

##### Songs:
I generated a list of 600 artists through the Spotify API using a recursive search algorithm. I started with 6 artists that represented a wide range of genres that people may like to workout to ('Macklemore', 'Beyonce', '30 Seconds to Mars', 'Disturbed', 'Calvin Harris', and '2 Chainz') and used the Related Artist endpoint to return 10 related artists to each artist. For these related artists, I fetched another 10 related artists. The process repeated until I had 600 artists total.

##### Tracks:
For each artist in the data set, I used the Top Tracks endpoint to fetch up to 10 popular tracks. The number of top tracks varied among artists, resulting in a total of 5000 tracks. The Audio Features endpoint provided the data for each track including:  
* Energy: Perceptual measure of intensity and activity (0.0 to 1.0). Contributing features: dynamic range, perceived loudness, timbre, onset rate, and general entropy.
* Danceability: How suitable a track is for dancing (0.0 to 1.0). Contributing features: tempo, rhythm stability, beat strength, and overall regularity.
* Valence: Musical positiveness conveyed by a track (0.0 to 1.0). Tracks with high valence sound more positive (e.g. happy, cheerful, euphoric), while tracks with low valence sound more negative (e.g. sad, depressed, angry).
* Acousticness: A confidence measure of whether the track is acoustic (0.0 to 1.0).
* Instrumentalness: A confidence measure of whether the track is instrumental (i.e. has no vocals) (0.0 to 1.0).
