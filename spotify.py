import spotipy,os,pickle;from spotipy.oauth2 import SpotifyOAuth
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

# Starting web player in your default browser
os.startfile('index.html')
# Authenticating with spotify
auth_manager = SpotifyOAuth(client_id=keys['client_id'], client_secret=keys['client_secret'],
                            redirect_uri='http://localhost:8000/auth/callback',
                            scope='user-library-read,user-read-playback-state,user-modify-playback-state,streaming,user-read-currently-playing,playlist-read-private,playlist-read-collaborative,user-follow-read,user-top-read')
sp = spotipy.Spotify(auth_manager=auth_manager)

# Spotify Commands
def song_search(song):
    # search for a track
    try:
        results = sp.search(q=f'track:{song[0]} artist:{song[1]}', type='track')
        print(f"Playing {song[0].title()} by {song[1].title()}")
    except IndexError:
        results = sp.search(q=f'track:{song[0]}', type='track')
        print(f"Playing {song[0].title()}")
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
        print(f'Plating songs by {artist_name}')
        # if no active device is found, use the first available device
        if device_id is None and len(devices['devices']) > 0:
            device_id = devices['devices'][0]['id']


        # play the track on the selected device
        sp.start_playback(device_id=device_id, uris=track_uris)
def userplaylist():
    results = sp.current_user_saved_tracks()
    track_uris = [item['track']['uri'] for item in results['items']]
    print("Playing your Liked Songs")
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
def TopTracks():
    results = sp.current_user_top_tracks()
    print(results)
    track_uris = [item['track']['uri'] for item in results['items']]
    print("Playing your Liked Songs")
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
def PausePlay(option):
    if option == 'pause':
        sp.pause_playback()
    elif option == 'continue':
        sp.start_playback()
def SkipBack(option):
    if option == 'skip':
        sp.next_track()
    elif option == 'back':
        sp.previous_track()
    elif option == 'shuffle':
        sp.shuffle(state=True)
        print("Shuffling")
def selections():
    # Ask user for a song (temp for text only)
    option = input("\n\nWelcome to Spotify\n------------------\nPlease enter a selection: ")\
        .lower().split('on spotify')[0]
    # Changing formatting
    if option.__contains__('play '):
        option = option.split('play ')[1]
    # User didn't give a option
    if option == 'play':
        print('What would you like to play?')
        selections()
    elif option.__contains__("songs by "):
        artist_playlist(option)
    # Play the users liked playlist
    elif option.__contains__("my playlist") or option.__contains__("my songs") \
            or option.__contains__("my liked songs"):
        userplaylist()
    # Play/ Pause
    elif option.__contains__('pause') or option.__contains__('continue'):
        PausePlay(option)
    elif option == 'skip' or option == 'back' or option == 'shuffle':
        SkipBack(option)
    # Search for song
    elif option.__contains__('top tracks') or option.__contains__('music'):
        TopTracks()
    else:
        # More formatting...
        if option.__contains__(", "):
            option = option.split(", ")
        else:
            option = option.split(" by ")
        song_search(option)
while True:
    selections()