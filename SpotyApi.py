import spotipy


def getTrackInfo(results: dict) -> list:
    tracks: list = []
    for item in results['items']:
        track: dict = item['track']
        tracks.append({
            'name': track['name'], 'artist': track['artists'][0]['name']
        })
    return tracks


class SpotifyApi:
    def processPlaylists(self, playlist_dict: dict) -> list:
        playlists: list = playlist_dict[list(playlist_dict.keys())[1]]
        info: list = []
        for playlist in playlists:
            info.append({
                "name": playlist['name'],
                'id': playlist['id'],
                'url': playlist['href']
            })
        return info

    def getPlaylists(self, token: str) -> list:
        connection: spotipy.client.Spotify = spotipy.Spotify(auth=token)

        user: dict = connection.current_user()
        user_id: str = user['id']
        playlists: dict = connection.user_playlists(user_id)
        return self.processPlaylists(playlists)

    def getTracks(self, playlists: list, token: str) -> list:
        connection: spotipy.client.Spotify = spotipy.Spotify(auth=token)

        playlist_tracks: list = []
        for playlist in playlists:
            results: dict = connection.playlist(playlist['id'],
                                                fields="tracks,next")
            tracks: dict = results['tracks']
            tracks_list: list = (getTrackInfo(tracks))

            while tracks['next']:
                tracks: dict = connection.next(tracks)
                tracks_list: list = (getTrackInfo(tracks))
            playlist_tracks.append({
                'playlist': playlist['id'],
                'playlist_name': playlist['name'],
                'tracks': tracks_list
            })
        return playlist_tracks


if __name__ == "__main__":
    api = SpotifyApi()
    api.getPlaylists("")
