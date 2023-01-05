import os
try:
    import requests
except:
    os.system("pip install requests")
try:
    import flask
    from flask import request
except:
    os.system("pip install flask")

from winreg import HKEY_CURRENT_USER, OpenKey, QueryValueEx, HKEY_CLASSES_ROOT
import logging, base64

userCode = None

clientId = '440fd6baab334f568adac323a600296e'
clientSecret = '4c9b1e58b12448e79ca81f91b38b7486'

url = f'https://accounts.spotify.com/authorize?client_id={clientId}&response_type=code&redirect_uri=http://localhost:45/callback&scope=user-read-private user-read-email ugc-image-upload user-read-playback-state user-modify-playback-state user-read-currently-playing app-remote-control streaming playlist-read-private playlist-read-collaborative playlist-modify-private playlist-modify-public user-follow-modify user-follow-read user-read-playback-position user-top-read user-read-recently-played user-library-modify user-library-read'

def create_dummy_redirector(): # creates a dummy server on localhost:45 to catch the redirect from Spotify (getting user token from the spotify login form.)
    app = flask.Flask(__name__)
    log = logging.getLogger('werkzeug')
    log.disabled = True # just disables annoying little logs
    @app.post('/kill')
    def kill():
        func = request.environ.get('werkzeug.server.shutdown')
        if func is None:
            pass # if cannot kill, just pass
        func()
        return ""

    @app.route('/callback',methods=['GET'])
    def e():
        os.system("cls")
        global userCode # zip it
        userCode = request.args.get('code')
        requests.post('http://localhost:45/kill')
        os.system("cls")
        return 'You have authorized the app. You can close this window now.'

    app.run(port=45)

def get_default_browser_path(): # gets the default browser path from the registry
    with OpenKey(HKEY_CURRENT_USER,r'SOFTWARE\Microsoft\Windows\Shell\Associations\UrlAssociations\http\UserChoice') as key:
        cmd = QueryValueEx(key, 'ProgId')[0]
    with OpenKey(HKEY_CLASSES_ROOT, r'{}\shell\open\command'.format(cmd)) as regkey:
        browser_path_tuple = QueryValueEx(regkey, None)
        browser_path = browser_path_tuple[0].split('"')[1]
    return browser_path

def exchangeCodeForAuth(code): # exchanges the given code from the redirect for a Bearer token
    headers = {
        "Authorization": f'Basic {base64.b64encode(f"{clientId}:{clientSecret}".encode()).decode()}'
    }
    data = {
        "code": code,
        "redirect_uri": "http://localhost:45/callback",
        "grant_type": 'authorization_code'
    }
    with requests.post("https://accounts.spotify.com/api/token",headers=headers,data=data) as r: # making the request
        return r.json()

def return_access_token():   
    os.system(f'start "{get_default_browser_path()}" "{url}"') # opens the spotify login form in the default browser
    create_dummy_redirector() # starts the dummy server
    access_token = exchangeCodeForAuth(userCode).get('access_token') # gets the bearer token
    return access_token

