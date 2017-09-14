import pandas as pd
import matplotlib.pyplot as plt
import StringIO
import base64
plt.style.use('ggplot')
plt.rcParams.update({'font.family': 'monospace',
                     'savefig.facecolor': '#f0f0f5',
                     'savefig.facecolor':'#f0f0f5'})

def build_histograms(track_df,
                    features = ['danceability', 'energy', 'valence'],
                    colors = ['cyan', 'orange', 'green'],
                    bkgd_color = "#f0f0f5", font = 'monospace'):

    img = StringIO.StringIO()
    fig, ax = plt.subplots( )
    for i, feature in enumerate(features):
        ax.hist(track_df[feature],
                 bins=30,
                 range=(min(track_df[feature]),max(track_df[feature])),
                 facecolor=colors[i],
                 alpha=0.5,
                #  histtype = 'step',
                 normed=1,
                 label = feature);
        labels = ax.get_xticklabels() + ax.get_yticklabels()
        [label.set_fontname(font) for label in labels]
        ax.legend(loc="upper left")
    # fig.savefig(img, format='png', bbox_inches='tight')
    fig.savefig(img, format='png')

    img.seek(0)
    plot_url = base64.b64encode(img.getvalue())
    return plot_url
