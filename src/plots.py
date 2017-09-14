import pandas as pd
import matplotlib.pyplot as plt
import StringIO
import base64

def build_histograms(track_df,
                    features = ['danceability', 'energy', 'valence'],
                    colors = ['cyan', 'orange', 'green']):
    img = StringIO.StringIO()
    fig, ax = plt.subplots()
    for i, feature in enumerate(features):
        ax.hist(track_df[feature],
                 bins=30,
                 range=(min(track_df[feature]),max(track_df[feature])),
                 facecolor=colors[i],
                 alpha=0.3,
                #  histtype = 'step',
                 normed=1,
                 label = feature);
        ax.legend(loc="upper left")
    fig.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue())
    return plot_url
