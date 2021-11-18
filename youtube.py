# from re import search
from ytmusicapi import YTMusic
import threading
import time


class PlaylistToYoutube(threading.Thread):
    def __init__(self, playlists_to_import: list) -> None:
        super().__init__()
        self.progress: int = 0
        self.total: int = 0
        self.done: bool = False
        self.ytmusic: YTMusic = YTMusic('headers_auth.json')
        self.playlists_to_import: list = playlists_to_import

    def addSongToPlaylist(self, playlistId: str, search_query: str) -> None:
        search_results: list = self.ytmusic.search(search_query)
        for result in search_results:
            if result['resultType'] == "song":
                self.ytmusic.add_playlist_items(playlistId,
                                                [result['videoId']])
                break

    def migratePlaylist(self, playlists_to_import: list) -> None:
        debug: bool = True
        if debug:
            for playlist in playlists_to_import:
                self.total = len(playlist['tracks'])
                for x in playlist['tracks']:
                    time.sleep(0.1)
                    self.progress += 1
            self.done = True
            return
        else:
            for playlist in playlists_to_import:
                playlistId: str = self.ytmusic.create_playlist(
                    playlist['playlist_name'], 'Imported from Spotify')
                print("localhost:5000/delete?playlist_id=" + playlistId)
                print("migrando " + playlist['playlist_name'])
                # print(playlist['tracks'])
                print(len(playlist['tracks']))
                # processes = []
                for song in playlist['tracks']:
                    self.progress += 1
                    search_query: str = song['name'] + " " + song['artist']
                    self.addSongToPlaylist(playlistId,
                                           search_query, self.ytmusic)

    def run(self) -> None:
        self.migratePlaylist(self.playlists_to_import)

    def deletePlaylist(self, playlistId) -> None:
        self.ytmusic.delete_playlist(playlistId)


if __name__ == "__main__":
    pass

# ytmusic = YTMusic('headers_auth.json')
# playlistId = ytmusic.create_playlist('test', 'test description')
# search_results = ytmusic.search('oasis Wonderwall')
# ytmusic.add_playlist_items(playlistId, [search_results[0]['videoId']])
