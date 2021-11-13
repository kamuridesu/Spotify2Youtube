# import requests
import json

import spotipy
# from spotipy.oauth2 import SpotifyClientCredentials
# from spotipy.oauth2 import SpotifyOAuth


def getTrackInfo(results):
    tracks = []
    for item in results['items']:
        track = item['track']
        track_info = {}
        track_info['name'] = track['name']
        track_info['artist'] = track['artists'][0]['name']
        tracks.append(track_info)
    return tracks


class SpotifyApi:
    def __init__(self):
        SECRETS = self.readSecrets()
        self.client_id = SECRETS['clientID']
        self.client_secret = SECRETS['clientSecret']

    def readSecrets(self):
        with open("credentials.json", "r", encoding="utf-8") as f:
            return json.loads(f.read())

    def processPlaylists(self, playlist_dict):
        d = playlist_dict[list(playlist_dict.keys())[1]]
        info = []
        for k in d:
            playlist_info = {}
            playlist_info['name'] = k['name']
            playlist_info['id'] = k['id']
            playlist_info['url'] = k['href']
            info.append(playlist_info)
        return info

    def getPlaylists(self, token):
        connection = spotipy.Spotify(auth=token)

        user = connection.current_user()
        user_id = user['id']
        # username = user['display_name']
        playlists = connection.user_playlists(user_id)
        return self.processPlaylists(playlists)

    def getTracks(self, playlists, token):
        connection = spotipy.Spotify(auth=token)

        playlist_tracks = []
        for playlist in playlists:
            pl = {}
            pl['playlist'] = playlist['id']
            pl['playlist_name'] = playlist['name']
            tracks_list = []
            results = connection.playlist(playlist['id'], fields="tracks,next")
            tracks = results['tracks']
            tracks_list = (getTrackInfo(tracks))
            # show_tracks(tracks)

            while tracks['next']:
                tracks = connection.next(tracks)
                tracks_list = (getTrackInfo(tracks))
            pl['tracks'] = tracks_list
            playlist_tracks.append(pl)
        return playlist_tracks


if __name__ == "__main__":
    api = SpotifyApi()
    api.getPlaylists("uk6rvhamepkrbzpx2lqh9a78z")
