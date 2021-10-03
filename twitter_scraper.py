from tweepy import Stream
import paho.mqtt.client as mqtt
import tweepy
import re
import json
import os
import logging

consumer_key = os.environ['consumer_key']
consumer_secret = os.environ['consumer_secret']
access_token = os.environ['access_token']
access_token_secret = os.environ['access_token_secret']

twitter_user_id = os.environ['twitter_user_id']
host_ip = os.environ['mqtt_host_ip']
client_id_name = os.environ['mqtt_client_id']

QOS = 2


linie_stations = {
  "Linie 16": "Sebastianstr",
  "Linie 12": "Neusser Str",
  "Linie 13": "Neusser Str",
  "Linie 15": "Neusser Str",
  "Linie 147": "Neusser Str.",
  "Linie": "H"
}


def init_mqtt(host_ip, client_id_name):
    global client 
    client = mqtt.Client(client_id = client_id_name)
    client.connect(host_ip)
    client.publish("KVB_status/script_status", "Online", QOS)
    client.loop()
    client.disconnect()


def return_tweets(status):

        if not status.truncated:
            text = status.text
        else:
            text = status.extended_tweet['full_text']

        Linie = get_linie(text)

        logging.warning(text)
        Linie = Linie[:-1]
        client.connect(host_ip)
        client.loop_start()
        logging.warning(get_message(text))

        payload = {"Linie": Linie, "message": get_message(text), "stations": get_stations(text, (linie_stations[Linie] if Linie in linie_stations else "H" ))}

        client.publish("KVB_status/" + str(status.id), json.dumps(payload, ensure_ascii=False) ,qos = QOS)
        client.loop_stop()
        client.disconnect()
        logging.warning("\n")

def get_message(status_text):
    try:
        result = re.search('\*(.*?)\*',status_text).group(0)
        return result
    except:
        return "* Keine Meldung gefunden *"

def get_linie(status_text):
    try:
        result = re.search('(.*?)\*',status_text).group(0)
        result = result[:-1]
        return (result)
    except:
        return("Linie 0 ")
    
def get_stations(status_text, search_station):
    try:
        result = re.search('\((.*?)\-',status_text)
        for i in range(len(result.groups())+1):
            if search_station in result.group(i):
                return result.group(i)
        return result.group(0)
    except:
        return "Haltestellen unbekannt"

class Get_Tweet(tweepy.Stream):

    def on_status(self, status):
        
        logging.warning(status.user.id_str)
        if status.user.id_str == twitter_user_id and status.in_reply_to_status_id is None:
            return_tweets(status)

    def on_error(self, status):
        logging.warning(status)

if __name__ == '__main__':
    init_mqtt(host_ip, client_id_name)
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    twitterStream = Get_Tweet(consumer_key,consumer_secret,access_token,access_token_secret)
    twitterStream.filter(follow=[twitter_user_id])

        

