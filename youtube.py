# from re import search
from ytmusicapi import YTMusic


def addSongToPlaylist(playlistId, search_query, ytmusic_intance):
    search_results = ytmusic_intance.search(search_query)
    for result in search_results:
        if result['resultType'] == "song":
            print(result['title'])
            ytmusic_intance.add_playlist_items(playlistId, [result['videoId']])
            break


class PlaylistToYoutube:
    def __init__(self) -> None:
        self.ytmusic = YTMusic('headers_auth.json')

    def migratePlaylist(self, playlists_to_import):
        for playlist in playlists_to_import:
            playlistId = self.ytmusic.create_playlist(
                playlist['playlist_name'], 'Imported from Spotify')
            print("localhost:5000/delete?playlist_id=" + playlistId)
            print("migrando " + playlist['playlist_name'])
            # print(playlist['tracks'])
            print(len(playlist['tracks']))
            # processes = []
            for song in playlist['tracks']:
                search_query = song['name'] + " " + song['artist']
                addSongToPlaylist(playlistId, search_query, self.ytmusic)

    def deletePlaylist(self, playlistId):
        self.ytmusic.delete_playlist(playlistId)


if __name__ == "__main__":
    pass

# ytmusic = YTMusic('headers_auth.json')
# playlistId = ytmusic.create_playlist('test', 'test description')
# search_results = ytmusic.search('oasis Wonderwall')
# ytmusic.add_playlist_items(playlistId, [search_results[0]['videoId']])
