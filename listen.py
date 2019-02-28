#!/usr/bin/env python3

import argparse
import os
import time

import pylast
import spotipy
import spotipy.util as util

API_KEY = "your_lastfm_api_key"
API_SECRET = "your_lastfm_api_secret"
os.environ['SPOTIPY_CLIENT_ID'] = 'your_spotify_api_key'
os.environ['SPOTIPY_CLIENT_SECRET'] = 'your_spotify_api_secret'
# You can use whatever address you want here.
# The spotipy library will ask you to copy/paste the URL you have been redirected to.
# Beware : you must whitelist the url used here, in your app on your Spotify Dashboard
os.environ['SPOTIPY_REDIRECT_URI'] = 'http://localhost/'

SESSION_KEY_FILE = ".session_key"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="This application allows you to listen the same music a Last.fm user is listening to,"
                    " through Spotify",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("user", help="User to follow along")
    parser.add_argument("sp_username", help="Your Spotify username")
    args = parser.parse_args()

    sp = spotipy.Spotify()
    token = util.prompt_for_user_token(args.sp_username, 'streaming user-library-read')

    if token:
        sp = spotipy.Spotify(auth=token)
    else:
        print("Can't get token for", args.sp_username)
        exit()

    network = pylast.LastFMNetwork(API_KEY, API_SECRET)

    if not os.path.exists(SESSION_KEY_FILE):
        skg = pylast.SessionKeyGenerator(network)
        url = skg.get_web_auth_url()

        print("Please authorize the scrobbler to scrobble to your account: {url}\n")
        import webbrowser

        webbrowser.open(url)

        while True:
            try:
                session_key = skg.get_web_auth_session_key(url)
                fp = open(SESSION_KEY_FILE, "w")
                fp.write(session_key)
                fp.close()
                break
            except pylast.WSError:
                time.sleep(1)
    else:
        session_key = open(SESSION_KEY_FILE).read()

    network.session_key = session_key
    user = network.get_user(args.user)
    print("Tuned in to", args.user)

    playing_track = None
    just_started_playing = False

    while True:
        try:
            new_track = user.get_now_playing()
            if new_track is None:
                print("\rUser is not listening to music right now (checking every 1 min).", end="")
                # Wait 1 minute if nothing is playing
                track_duration = 60
                just_started_playing = False
            # user is listening to a new song
            elif new_track != playing_track:
                playing_track = new_track
                just_started_playing = True
                print("User is now listening to: ", new_track)
                print("Searching for the track on Spotify...")
                results = sp.search(q=new_track, limit=1, type='track')
                # Track found ?
                if len(results['tracks']['items']) > 0:
                    track = results['tracks']['items'][0]
                    track_duration = int(track['duration_ms']) / 1000
                    m, s = divmod(track_duration, 60)
                    print("Playing track on Spotify (duration: {:d}:{:02d}). Enjoy :)".format(int(m), int(s)))
                    sp.start_playback(uris=[track['uri']])
                else:
                    print('Track not found :(')
                    track_duration = 10
            else:
                just_started_playing = False
        except Exception as e:
            print("Error: %s" % repr(e))
        # Listen at least for the duration of the song, so that it's not cut before it ends
        # we will slowly drift in delay (because of requests time etc)
        # but at worst we will miss a song from time to time
        # Bonus : If the song just changed and the user decides to change track, we might miss the change in case
        # we tuned in right when he started listening to a song. So the first time, wait for 15s and then for the rest
        # of the duration of the song afterwards.
        if just_started_playing is True:
            time.sleep(15)
        else:
            time.sleep(track_duration - 15)


# End of file
