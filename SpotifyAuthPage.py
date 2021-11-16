from flask import Flask, render_template, redirect, request, session
import spotipy
import json

from SpotyApi import SpotifyApi
import youtube

import threading
import random

app = Flask(__name__)
app.secret_key = "secret-key"
secrets = {}
with open("credentials.json", "r", encoding="utf-8") as f:
    secrets = json.loads(f.read())

API_BASE = "https://accounts.spotify.com"
REDIRECT_URI = "http://localhost:5000/callback"
SCOPE = 'playlist-modify-private,playlist-modify-public,user-top-read'

THREADS = {}


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
        return redirect("auth")


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
        # out = []
        # for x in playlists:
        #     output = ""
        #     output += "name: " + str(x['name'])
        #     output += " -- id: " + str(x['id'])
        #     output += " -- url: " + str(x['url'])
        #     output += "\n"
        #     out.append(output)
        return render_template("playlists.html", args=playlists)
    except (spotipy.exceptions.SpotifyException, KeyError):
        return redirect("auth")


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
        return redirect("auth")


@app.route('/migrate')
def migrate():
    try:
        api = SpotifyApi()
        playlist_id = request.args.get('playlist_id')
        playlists = api.getPlaylists(session["token_info"]['access_token'])
        playlist = ""
        for pl in playlists:
            if pl['id'] == playlist_id:
                playlist = [pl]
        if playlist == "":
            playlist = playlists
        tracks = api.getTracks(playlist,
                               session["token_info"]['access_token'])

        thread_id = random.randint(0, 10000)
        THREADS[thread_id] = youtube.PlaylistToYoutube(tracks)
        THREADS[thread_id].start()
        # playlist = youtube.PlaylistToYoutube()
        # render_template("migrating.html")
        # playlist.migratePlaylist(tracks)
        # return redirect('success')
        return redirect("/migration_success?task_id=" + str(thread_id))
    except (spotipy.exceptions.SpotifyException, KeyError):
        return redirect("auth")


@app.route("/progress/<int:task_id>")
def progress(task_id):
    global THREADS
    if THREADS[task_id].done:
        return "done"
    return str(THREADS[task_id].progress)


@app.route("/migration_success")
def mg_success():
    args = request.args.get("task_id")
    if args:
        return render_template("migration_success.html", task_id=args)


@app.route('/delete')
def delete():
    playlist = youtube.PlaylistToYoutube()
    playlist_id = request.args.get('playlist_id')
    playlist.deletePlaylist(playlist_id)
    return "success"


if __name__ == "__main__":
    app.run(host="localhost", debug=True, port=5000)
