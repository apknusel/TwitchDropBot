import urllib.request
import requests
import json
import configparser

config = configparser.ConfigParser()
config.read("config.ini")
CLIENT_ID = config["Twitch Application"]["CLIENT_ID"]
CLIENT_SECRET = config["Twitch Application"]["CLIENT_SECRET"]

def make_request(URL):
  header = {"Client-ID": CLIENT_ID, "Authorization": f"Bearer {get_access_token()}" }
  req = urllib.request.Request(URL, headers=header)
  recv = urllib.request.urlopen(req)
  return json.loads(recv.read().decode("utf-8"))

def get_access_token():
  x = requests.post(f"https://id.twitch.tv/oauth2/token?client_id={CLIENT_ID}&client_secret={CLIENT_SECRET}&grant_type=client_credentials")
  return json.loads(x.text)["access_token"]

def get_current_online_streams(streamers):
  URL = "https://api.twitch.tv/helix/streams?user_login="
  resps = []
  online_streams = []
  for name in streamers:
      resps.append(make_request(URL + name))
  for i, r in enumerate(resps, 0):
      if r["data"]:
        is_live = r["data"][0]["type"]
        online_streams.append((streamers[i], is_live))
  return online_streams