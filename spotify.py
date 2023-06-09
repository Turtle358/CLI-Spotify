import spotipy,pickle,time,webbrowser,subprocess,random;from spotipy.oauth2 import SpotifyOAuth
# Starting web player in your default browser
subprocess.Popen("python -m http.server 8000")
webbrowser.open('http://127.0.0.1:8000/index.html')

# Get keys
try:
    with open("spotify.keys","rb") as file:
        keys = pickle.load(file)
except FileNotFoundError:
    # if no keys found, request them
    id = input("Please enter your client id: ")
    secret = input('Please enter your client secret: ')
    keys = {'client_id': id, 'client_secret': secret}
    with open('spotify.keys',"wb") as file:
        pickle.dump(keys, file)

# Authenticating with spotify
auth_manager = SpotifyOAuth(client_id=keys['client_id'], client_secret=keys['client_secret'],
                            redirect_uri='http://localhost:8000/auth/callback',
                            scope='user-library-read,user-read-playback-state,user-modify-playback-state,\
                            streaming,user-read-currently-playing,playlist-read-private,playlist-read-collaborative,\
                            user-follow-read,user-top-read')
sp = spotipy.Spotify(auth_manager=auth_manager)

# Spotify Commands
def song_search(song):
    try:
        # search for a track
        if song.__contains__("polish cow") or song.__contains__("polish cow song") or song.__contains__("polska cow"):
            song = ['Gdzie jest biały węgorz']
        try:
            results = sp.search(q=f'track:{song[0]} artist:{song[1]}', type='track')
        except IndexError:
            results = sp.search(q=f'track:{song[0]}', type='track')
        track_uri = results['tracks']['items'][0]['uri']
        # get the ID of the device running the script
        devices = sp.devices()
        device_id = None
        for device in devices['devices']:
            if device['is_active']:
                device_id = device['id']
                break
        # if no active device is found, use the first available device
        if device_id is None and len(devices['devices']) > 0:
            device_id = devices['devices'][0]['id']
        # play the track on the selected device
        sp.start_playback(device_id=device_id, uris=[track_uri])
        #say what is playing
        try:
            time.sleep(0.4)
            songinfo = sp.current_playback()
            return f"Playing {songinfo['item']['name']} by {songinfo['item']['artists'][0]['name']}"
        except:
            return f"Playing {song[0]}"
    except IndexError:
        return f"{song} not found"

def artist_playlist(Artist):
    artist_name = Artist.split('songs by ')[1]
    results = sp.search(q=f'artist:{artist_name}', type='artist', limit=1)
    artist = results['artists']['items'][0]
    artist_id = artist['id']
    top_tracks = sp.artist_top_tracks(artist_id)

    track_uris = []
    for track in top_tracks['tracks']:
        track_uris.append(track['uri'])
        # get the ID of the device running the script
        devices = sp.devices()
        device_id = None
        for device in devices['devices']:
            if device['is_active']:
                device_id = device['id']
                break
        # if no active device is found, use the first available device
        if device_id is None and len(devices['devices']) > 0:
            device_id = devices['devices'][0]['id']

        # play the track on the selected device
        sp.start_playback(device_id=device_id, uris=track_uris)
        return f'Playing songs by {artist_name.title()}'
def userplaylist():
    results = sp.current_user_saved_tracks()
    track_uris = [item['track']['uri'] for item in results['items']]
    # get the ID of the device running the script
    devices = sp.devices()
    device_id = None
    for device in devices['devices']:
        if device['is_active']:
            device_id = device['id']
            break
    # if no active device is found, use the first available device
    if device_id is None and len(devices['devices']) > 0:
        device_id = devices['devices'][0]['id']

    # play the track on the selected device
    sp.start_playback(device_id=device_id, uris=track_uris)
    return 'Playing your liked songs'
def TopTracks():
    results = sp.current_user_top_tracks(limit=20)
    top_tracks = results['items']
    track_uris = [track['uri'] for track in top_tracks]
    #Enabling shuffle (if not already on)
    sp.shuffle(state=True)
    # get the ID of the device running the script
    devices = sp.devices()
    device_id = None
    for device in devices['devices']:
        if device['is_active']:
            device_id = device['id']
            break
    # if no active device is found, use the first available device
    if device_id is None and len(devices['devices']) > 0:
        device_id = devices['devices'][0]['id']

    # play the track on the selected device
    sp.start_playback(device_id=device_id, uris=track_uris)
    return 'Playing your top songs'
def charts():
    pass
def on_repeat():
    mix_uri = None
    mixes = sp.current_user_playlists(limit=50, offset=0)
    for playlist in mixes['items']:
        if playlist['name'] == "On Repeat":
            mix_uri = playlist['uri']
            break
    if mix_uri:
        # play the mix using the Spotify SDK
        sp.start_playback(context_uri=mix_uri)
        return "Playing your most played songs"
    else:
        return "Mix playlist not found."
def PausePlay(option):
    if option == 'pause' or option == 'stop':
        sp.pause_playback()
    elif option == 'continue':
        sp.start_playback()
    return ""
def SkipBack(option):
    if option == 'skip':
        sp.next_track()
    elif option == 'back':
        sp.previous_track()
    elif option == 'shuffle':
        sp.shuffle(state=True)
        return "Shuffling"
    return ""

def WhatsPlaying(option):
    try:
        result = sp.current_playback()
        artist = result['item']['artists'][0]['name']
        album_cover = result['item']['album']['images'][0]['url']
        song_name = result['item']['name']
        if option == 'who is this' or "who's this" or "whos this":
            output = (f'This is {song_name} by {artist.title()}')
        else:
            output = (f'Currently playing {song_name} by {artist.title()}\n')
        output +=(f'\nAlbum cover: {album_cover}\n')
        # Shuffle State
        if sp.current_playback()['shuffle_state'] == True:
            output += ("Shuffle mode is on")
        else:
            output += ("Shuffle is off")
        # Get device it's currently playing on
        output += f"\nCurrently playing on {result['device']['name']}"
        return output

    except:
        # If nothing is playing, to prevent crashes
        return "Nothing is currently playing"
def selections(option):
    # Ask user for a song (temp for text only)
    option = option.lower().split('on spotify')[0].split("?")[0]
    # Changing formatting
    if option.__contains__('play '):
        option = option.split('play ')[1]
    # User didn't give a option
    if option == 'play':
        output = 'What would you like to play?'
    elif option.__contains__("songs by "):
        output = artist_playlist(option)
    # Play the users liked playlist
    elif option.__contains__("my playlist") or option.__contains__("my songs") \
            or option.__contains__("my liked songs"):
        output = userplaylist()
    # Play/ Pause
    elif option.__contains__('pause') or option.__contains__('continue') or option.__contains__('stop'):
        output = PausePlay(option)
    elif option == 'skip' or option == 'back' or option == 'shuffle':
        output = SkipBack(option)
    #Top tracks
    elif option.__contains__('top tracks') or option.__contains__('music'):
        tmp = random.randrange(2)
        if tmp == 0:
            output = TopTracks()
        else:
            output = on_repeat()
    # Currently Playing
    elif option.__contains__("what's playing") or option.__contains__('whats playing') or option.__contains__\
                ('what song is this') or option.__contains__("what is this") or option.__contains__('who is this')\
            or option.__contains__("who's this"):
        output = WhatsPlaying(option)
    elif option == 'commands':
        output = ('''Commands:\n
        (play) [song name]: play a specific song\n
        (play) music: plays your top tracks\n
        (play) top tracks: plays your top tracks\n
        (play) my songs/ my playlist: plays your liked songs\n
        (play) songs by [artist]: plays songs by a specific artist\n
        skip: skips the song\n
        shuffle: enables shuffle\n
        what's playing: tells you whats playing and info about song\n
        who's this: same as what's playing but phrased differently''')
    # Search for song
    else:
        # More formatting...
        if option.__contains__(", "):
            option = option.split(", ")
        else:
            option = option.split(" by ")
        output = song_search(option)
    return output
# To run on startup to allow for web page to open correctly
selections("what's playing")

# Ask the user what to do
while True:
    print(selections(input("\nWelcome to Spotify\n------------------\nPlease enter a selection: ")))
