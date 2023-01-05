import os
try:
    import requests
except:
    os.system("pip install requests")

def searchTrack(bearer,query):
    headers = {
        "Authorization": f"Bearer {bearer}"
    }
    r = requests.get(f"https://api.spotify.com/v1/search?q={query}&type=track&include_external=audio",headers=headers)
    return r.json()

def getLastDeviceID(bearer):
    headers = {
        "Authorization": f"Bearer {bearer}"
    }
    r = requests.get("https://api.spotify.com/v1/me/player/devices",headers=headers)
    return r.json()['devices'][0]['id']

def playTrack(bearer,trackId):
    headers = {
        "Authorization": f"Bearer {bearer}"
    }
    r = requests.put("https://api.spotify.com/v1/me/player/play",headers=headers,json={"uris":[f"spotify:track:{trackId}"]})
    if r.content == b'':
        return {"status":"success"}
    else:
        if r.json()['error']['message'] == "Player command failed: No active device found":
            lastDevice = getLastDeviceID(bearer)
            r = requests.put(f"https://api.spotify.com/v1/me/player/play?device_id={lastDevice}",headers=headers,json={"uris":[f"spotify:track:{trackId}"]})
            if r.content == b'':
                return {"status":"success"}
            else:
                return r.json()
        else:
            return r.json()

def pauseTrack(bearer):
    headers = {
        "Authorization": f"Bearer {bearer}"
    }
    r = requests.put("https://api.spotify.com/v1/me/player/pause",headers=headers)
    if r.content == b'':
        return {"status":"success"}
    else:
        return r.json()

def gotoPoint(bearer,seconds):
    headers = {
        "Authorization": f"Bearer {bearer}"
    }
    r = requests.put(f"https://api.spotify.com/v1/me/player/seek?position_ms={seconds*1000}",headers=headers)
    if r.content == b'':
        return {"status":"success"}
    else:
        return r.json()

def getTrackInfo(bearer,id):
    headers = {
        "Authorization": f"Bearer {bearer}"
    }
    r = requests.get(f"https://api.spotify.com/v1/tracks/{id}",headers=headers)
    return r.json()
