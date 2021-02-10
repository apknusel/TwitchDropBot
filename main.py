import twitch_integration
from selenium import webdriver
import time
import configparser

config = configparser.ConfigParser()
streamers = []
streamerslive = []

def get_streamers():
    streamers = input("Names of streamers with commas seperating: ").replace(" ","").split(",")
    times = input("Time in seconds to watch each streamer with commas seperating respective to the streamer: ").replace(" ","").split(",")
    return streamers, times

def checklive(streamers):
    results = []
    isLive = twitch_integration.get_current_online_streams(streamers)
    for i in range(len(streamers)):
        try:
            if isLive[i][1] == "live":
                results.append(streamers[i])
        except:
            none = "no"
    return results

def start_watching(streamers, streamerslive, username, t):
    config.read("config.ini")
    profile = config["Chrome"]["Profile"]
    print(f"Started watching {username}!")
    URL = f"https://www.twitch.tv/{username}"
    options = webdriver.ChromeOptions()
    options.headless = True
    options.add_argument(f"user-data-dir={profile}")
    driver = webdriver.Chrome(executable_path=r"chromedriver.exe", options=options)
    driver.get(URL);
    time.sleep(60+int(t))
    streamers.remove(username)
    streamerslive.remove(username)
    driver.close()
    time.sleep(5)
    return streamers, streamerslive

def main():
    print('''
  _____                  ____        _   
 |  __ \                |  _ \      | |  
 | |  | |_ __ ___  _ __ | |_) | ___ | |_ 
 | |  | | '__/ _ \| '_ \|  _ < / _ \| __|
 | |__| | | | (_) | |_) | |_) | (_) | |_ 
 |_____/|_|  \___/| .__/|____/ \___/ \__|
                  | |                    
                  |_|   By: Alex Knusel  
''')
    streamers, times = get_streamers()
    while True:
        if len(streamers) == 0:
            break
        streamerslive = checklive(streamers)
        try:
            streamers, streamerslive = start_watching(streamers, streamerslive, streamerslive[0], times[0])
        except IndexError:
            print("Nobody is live right now!\nStreamers Left: {}".format(", ".join(streamers)))
            time.sleep(60)

if __name__ == "__main__":
    main()