# LastFmListenAlong

## Description

LastFmListenAlong is a program made in Python, allowing you to listen along a Last.fm user, by playing the songs the user is listening to on Spotify, in real time.    
It uses the Last.fm API to fetch what the user is listening to, and the Spotify API to search for the track on Spotify, and play it.

## Configuration

First, you have to register an app on the [Spotify developper page](https://developer.spotify.com/dashboard/).
Do not forget to whitelist a callback URL for the app (eg. `http://localhost/`). Note the API key and secret and populate it in the code.

Then you need to get an API key and secret on the [Last.fm API page](https://www.last.fm/api/account/create), and populate it in the code.

## Dependencies

This program relies on the `spotipy` and `pylast` libraries. They also require `requests`. Install them with :

```bash
pip install spotipy
pip install pylast
pip install requests
```

Note that, at the date this program was created, the spotipy version installed by pip is a bit outdated and do not contain a method we need to play a song on Spotify.   
You may need to get the last version of spotipy yourself here : [plamere/spotipy](https://github.com/plamere/spotipy) and place it in the current directory (renaming it just "spotipy", so that Python can import it from the current dir when it's not installed system-wide).


## Running

Once everything is configured, you just have to run the program with two parameters:

```bash
python listen.py lastfm_user_to_listen_along your_spotify_username
```

## Blog article about it

If you're curious you can read a blog article on how I came up with this idea on my blog: [here](https://hexaly.se/2019/02/27/how-to-listen-along-a-last-fm-user-on-spotify/).


## License

This program is released under no license. Do whatever you want with it. Share it, copy it, play with it, eat it. 
