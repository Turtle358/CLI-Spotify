# SpotifyWebPython
## Spotify Web Player using spotify SDK, Webpage in JS, rest of the backend in Python
Client ID and Client Secret can be found at https://developer.spotify.com/dashboard by creating an app
#
Sadly this does require Spotify Premium
#
- spotify.py is used to run all of the commands such as play ect... you run this file to activate the program, you need both the client id and the client secret for this
- index.html is used to run the web player, you only need the client id for this
- Webpage.bat is used to allow the http server to run correctly for index for html.
- the redirects used are http://localhost:8000/auth/callback (for spotify.py) and http://127.0.0.1:8000/index.html (for index.html) they can both use the same app at spotify dev page
