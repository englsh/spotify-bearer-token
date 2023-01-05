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

def playTrack(bearer,trackId):
    headers = {
        "Authorization": f"Bearer {bearer}"
    }
    r = requests.put("https://api.spotify.com/v1/me/player/play",headers=headers,json={"uris":[f"spotify:track:{trackId}"]})
    try:
        return r.json()
    except:
        return {"success":True}