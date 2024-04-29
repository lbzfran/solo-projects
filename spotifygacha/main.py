import secrets
from random import randint
import sys
import itertools
from time import sleep
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from password import cid, secret

# global playlist link
playlist_link = "https://open.spotify.com/playlist/37i9dQZEVXbNG2KDcFcKOF?si=1333723a6eff4b7f"
#playlist_link = "https://open.spotify.com/playlist/6xBwgclLuApOc3FwBbJtPa?si=1333723a6eff4b7f"

starRating: int = 1.5

ref_table: dict = {} # stores all item ids, with its respective reference code.

class Item:

    _id_iter = itertools.count()

    def __init__(self,_ref,weight):
        self._id = next(self._id_iter)
        self._ref = _ref # the reference id of the item.
        self._weight = weight # the rarity of the item. The lower, the more weight.

        ref_table[self._id] = self._ref

    @property
    def id(self):
        return self._id

    @property
    def ref(self):
        return self._ref

    @property
    def weight(self):
        return self._weight

def pull_rates(items: list, rarity: int) -> tuple:
    """
    Determines the pull rate of a list of items based on weights.

    :param items:       The list from which to determine the pulls from.
    :param rarity:      Determines the strength of the weights.
    :return:            Tuple of the list of rates and weights.
    """
    rates: list = []
    weights: list = []
    for item in items:
        weights.append(item.weight)
        for _ in range(item.weight**round(2*rarity)):
            rates.append(item.id)

    return (rates,weights)

def pull(items: list) -> int:
    """helper function that chooses (or `pulls`) a random integer id from a list."""
    return secrets.choice(items)

if __name__ == "__main__":

    # Gacha System Application using Spotify Playlists.

    track_items = []
    # spotify authentication section
    client_credentials_manager = SpotifyClientCredentials(client_id=cid,client_secret=secret)

    sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

    playlist_URI = playlist_link.split("/")[-1].split("?")[0]
    print(f"Loading Gacha System for `{sp.playlist(playlist_URI)['name']}`")
    track_uris = [x["track"]["uri"] for x in sp.playlist_tracks(playlist_URI)["items"]]
    
    track_names: dict = {}
    for tid,track in enumerate(sp.playlist_tracks(playlist_URI)["items"]):

        # tracks the uri, track name, and track artist
        track_names[tid] = (track["track"]["uri"],track["track"]["name"],track["track"]["artists"][0]["name"])
        track_items.append(Item(tid,randint(1,5)))

    # end section #

    if len(sys.argv) > 1:
        user = sys.argv[1]

    else:
        user = input(f"How many times would you like to pull??\ninput integer: ")

    # pull section
    pulls = [] # all the pulls.
    ratings = pull_rates(track_items,starRating)
    for x in range(int(user)): # loop the amount of pulls done.
        y = pull(ratings[0])
        pulls.append(y)

    pullcount = sum(pulls)
    for i in range(len(track_items)):
        occur = pulls.count(i)
        if occur > 0:
            ctrack = track_names[i]

            stars = '*' * (6-ratings[1][i])

            if stars == ('*' * 5):
                print(f"({stars}) {i} `{ctrack[1]} by {ctrack[2]}` seen {occur} times: {round((occur/pullcount)*100,3)}%")
            else:
                print(f"[{stars}] {i} `{ctrack[1]} by {ctrack[2]}` seen {occur} times: {round((occur/pullcount)*100,3)}%")
            sleep(0.15)

    """
    while True:

        id_to_check = input("Input id of track: ")

        if not id_to_check.isdigit():
            break

        #f = sp.audio_features(find_item(track_names,int(id_to_check))[0])[0]
        f = sp.audio_features(track_names[int(id_to_check)][0])[0]

        print(f"danceability: {f['danceability']} energy: {f['energy']} loudness: {f['loudness']}\nliveness: {f['liveness']} tempo: {f['tempo']}")
    """
