from re import search
from ytmusicapi import YTMusic, ytmusic

class Playlist:
    def __init__(self, playlistId):
        self.playlistID = playlistId

    def addTrack(self):
        pass


class PlaylistToYoutube:
    def __init__(self) -> None:
        self.ytmusic = YTMusic('headers_auth.json')
    
    def migratePlaylist(self, playlists_to_import):
        for playlist in playlists_to_import:
            playlistId = self.ytmusic.create_playlist(playlist['playlist_name'], 'Imported from Spotify')
            print("localhost:5000/delete?playlist_id=" + playlistId)
            print("migrando " + playlist['playlist_name'])
            # print(playlist['tracks'])
            print(len(playlist['tracks']))
            for song in playlist['tracks']:
                search_query = song['name'] + " " + song['artist']
                search_results = self.ytmusic.search(search_query)
                print(search_results)
                self.ytmusic.add_playlist_items(playlistId, [search_results[0]['videoId']])

    def deletePlaylist(self, playlistId):
        self.ytmusic.delete_playlist(playlistId)


if __name__ == "__main__":
    migration = PlaylistToYoutube()
    # migration.createPlaylist(test_dict)

# ytmusic = YTMusic('headers_auth.json')
# playlistId = ytmusic.create_playlist('test', 'test description')
# search_results = ytmusic.search('oasis Wonderwall')
# ytmusic.add_playlist_items(playlistId, [search_results[0]['videoId']])