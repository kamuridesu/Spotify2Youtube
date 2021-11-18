import json
import random

from flask import Flask, render_template, redirect, request, session
import spotipy

from SpotyApi import SpotifyApi
import youtube

app: Flask = Flask(__name__)
app.secret_key: str = "secret-key"
secrets: dict = {}
with open("credentials.json", "r", encoding="utf-8") as f:
    secrets = json.loads(f.read())

API_BASE: str = "https://accounts.spotify.com"
# Change this accordingly to your callback url
REDIRECT_URI: str = "http://localhost:5000/callback"
SCOPE: str = 'playlist-modify-private,playlist-modify-public,user-top-read'

THREADS: dict = {}


@app.route("/")
def main_page():
    return render_template("index.html")


@app.route("/auth")
def verify():
    sp_oauth = spotipy.oauth2.SpotifyOAuth(client_id=secrets['clientID'],
                                           client_secret=secrets["clientSecret"],
                                           redirect_uri=REDIRECT_URI, scope=SCOPE)
    auth_url = sp_oauth.get_authorize_url()
    print(auth_url)
    return redirect(auth_url)


@app.route("/success")
def success():
    try:
        session['token_info']
        return render_template("success.html")
    except KeyError:
        return redirect("/")


@app.route("/callback")
def callback():
    sp_oauth = spotipy.oauth2.SpotifyOAuth(client_id=secrets['clientID'],
                                           client_secret=secrets["clientSecret"],
                                           redirect_uri=REDIRECT_URI, scope=SCOPE)
    session.clear()
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)

    # Saving the access token along with all other token related info
    session["token_info"] = token_info

    return redirect("success")


@app.route("/playlists")
def playlists():
    try:
        api = SpotifyApi()
        playlists = api.getPlaylists(session["token_info"]['access_token'])
        return render_template("playlists.html", args=playlists)
    except (spotipy.exceptions.SpotifyException, KeyError):
        return redirect("/")


@app.route('/playlists/tracks')
def tracks():
    try:
        api = SpotifyApi()
        playlists = api.getPlaylists(session["token_info"]['access_token'])
        tracks = api.getTracks(playlists,
                               session["token_info"]['access_token'])
        for track in tracks:
            print(track)
            print()

        return "false"
    except (spotipy.exceptions.SpotifyException, KeyError):
        return redirect("/")


@app.route('/migrate')
def migrate():
    try:
        api = SpotifyApi()
        playlist_id = request.args.get('playlist_id')
        if playlist_id is None:
            return redirect("/")
        playlists = api.getPlaylists(session["token_info"]['access_token'])
        playlist = ""
        for pl in playlists:
            if pl['id'] == playlist_id:
                playlist = [pl]
        if playlist == "":
            return redirect("/")
        tracks = api.getTracks(playlist,
                               session["token_info"]['access_token'])

        thread_id = random.randint(0, 10000)
        THREADS[thread_id] = youtube.PlaylistToYoutube(tracks)
        THREADS[thread_id].start()
        return redirect("/migrating?task_id=" + str(thread_id))
    except (spotipy.exceptions.SpotifyException, KeyError):
        return redirect("/")


@app.route("/progress/<int:task_id>")
def progress(task_id):
    global THREADS
    if task_id in THREADS.keys():
        if THREADS[task_id].done:
            return "done"
        return str(THREADS[task_id].progress) + "/" + str(THREADS[task_id].total)
    return redirect("/")


@app.route("/migrating")
def migrating():
    args = request.args.get("task_id")
    if args:
        return render_template("migrating.html", task_id=args)
    else:
        return redirect("/")


@app.route('/delete')
def delete():
    playlist = youtube.PlaylistToYoutube()
    playlist_id = request.args.get('playlist_id')
    playlist.deletePlaylist(playlist_id)
    return "success"


if __name__ == "__main__":
    app.run(host="localhost", debug=True, port=5000)
    # Comment the line above and remove the comment from the line bellow
    # if you're running on Docker.
    # app.run(host="0.0.0.0", debug=True, port=5000)
