from flask import Flask, render_template, redirect, request, session, make_response,session,redirect, request
import spotipy
import spotipy.util as util
import time
import json

from SpotyApi import SpotifyApi
import youtube

app = Flask(__name__)

app.secret_key = "secret-key"
secrets = {}
with open("credentials.json", "r", encoding="utf-8") as f:
    secrets = json.loads(f.read())

API_BASE = 'https://accounts.spotify.com'

# Make sure you add this to Redirect URIs in the setting of the application dashboard
REDIRECT_URI = "http://127.0.0.1:5000/api_callback"

SCOPE = 'playlist-modify-private,playlist-modify-public,user-top-read'


@app.route("/")
def verify():
    # Don't reuse a SpotifyOAuth object because they store token info and you could leak user tokens if you reuse a SpotifyOAuth object
    sp_oauth = spotipy.oauth2.SpotifyOAuth(client_id = secrets['clientID'], client_secret = secrets["clientSecret"], redirect_uri = REDIRECT_URI, scope = SCOPE)
    auth_url = sp_oauth.get_authorize_url()
    print(auth_url)
    return redirect(auth_url)


@app.route("/index")
def index():
    try:
        with open("session_token", "w", encoding="utf-8") as f:
            f.write(json.dumps(session["token_info"]))
        return render_template("index.html")
    except KeyError:
        return verify()


@app.route("/api_callback")
def api_callback():
    sp_oauth = spotipy.oauth2.SpotifyOAuth(client_id = secrets['clientID'], client_secret = secrets["clientSecret"], redirect_uri = REDIRECT_URI, scope = SCOPE)
    session.clear()
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)

    # Saving the access token along with all other token related info
    session["token_info"] = token_info

    return redirect("index")


@app.route("/playlists")
def playlists():
    try:
        api = SpotifyApi()
        playlists = api.getPlaylists(session["token_info"]['access_token'])
        out = []
        for x in playlists:
            output = ""
            output += "name: " + str(x['name'])
            output += " -- id: " + str(x['id'])
            output += " -- url: " + str(x['url'])
            output += "\n"
            out.append(output)
        return render_template("playlists.html", args=[out])
    except (spotipy.exceptions.SpotifyException, KeyError):
        return verify()

@app.route('/playlists/tracks')
def tracks():
    try:
        api = SpotifyApi()
        playlists = api.getPlaylists(session["token_info"]['access_token'])
        tracks = api.getTracks(playlists, session["token_info"]['access_token'])
        for track in tracks:
            print(track)
            print()

        return "false"
    except (spotipy.exceptions.SpotifyException, KeyError):
        return verify()


@app.route('/migrate')
def migrate():
    try:
        api = SpotifyApi()
        playlists = api.getPlaylists(session["token_info"]['access_token'])
        tracks = api.getTracks(playlists, session["token_info"]['access_token'])
        playlist = youtube.PlaylistToYoutube()
        playlist.migratePlaylist(tracks)

        return redirect('index')
    except (spotipy.exceptions.SpotifyException, KeyError):
        return verify()


@app.route('/delete')
def delete():
    playlist = youtube.PlaylistToYoutube()
    id = request.args.get('playlist_id')
    playlist.deletePlaylist(id)
    return "success"


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
