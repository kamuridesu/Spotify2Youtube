# Spotify2Youtube
Migrate Spotify playlists to Youtube Music


## ATTENTION!
I made this project because I wanted to move from Spotify to YTMusic without losing all my playlists with years of music. It worked, but there's a lot of bugs that I need to fix:
- Create a front page on /index, after the user authenticate
- Create a /auth page to authenticate users instead of only /
- Ability to choose the playlist to migrate
- The user needs to take the YTMusic cookie in order to authenticate to Youtube Music (this is a known ytmusicapi issue, you can read more about it [here](https://github.com/sigma67/ytmusicapi/issues/10))

Besides these critial issues, there's a lot of minor ones.

I also want to refactor everything, most of the methods are ugly and can be improved a lot. Also, the performance is painful, takes a long time to process everything and it looks like the server is down idk.

## Usage
### Setup
Create an app on [Spotify Developer Dashboard](https://developer.spotify.com/dashboard), create a `credentials.json` file with the following structure:
```json
{
  "clientID": "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
  "clientSecret": "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
}
```
Then create a `headers_auth.json` file following [this tutorial](https://ytmusicapi.readthedocs.io/en/latest/setup.html#copy-authentication-headers).

To add your local callback to the app on the Spotify App Dashboard, go to Edit Settings -> Redirect URIs and put your callback url, then save. Remember to edit the `REDIRECT_URI` file on the `SpotifyAuthPage.py` file.

### Running
You can build the Dockerfile with `docker build -t spotify .` and run with `docker run --rm -it -p 5000:5000 spotify`, then access your IP to authenticate.

### Routes
The defined routes are:
- /, welcome page
- /auth, authenticates the user
- /callback, callback for the app, retrieves the user tokens
- /success, after authentication, shows that everything was successful
- /playlists, shows all available playlists and the option to migrate
- /playlists/tracks, prints the playlists tracks to your terminal
- /delete, deletes a youtube playlist using a query string to receive the playlist id, like: `delete?playlist_id=PLxMD4Nzoqa861bL7m3OSY-N4dn3Wr45f4`
