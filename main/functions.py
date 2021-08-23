import json
import requests
from langdetect import detect
from textblob import TextBlob
from textblob_fr import PatternTagger, PatternAnalyzer
from textblob_de import TextBlobDE
from textblob import TextBlob
import re
from urllib.parse import urlparse, parse_qs

api_key = "AIzaSyD4ihso2KXy8cvUN_Q5mwiR2AK3AtX32T4"


        #returner des donnees
def get_data(url: str):
    json_url = requests.get(url)
    data = json.loads(json_url.text)
    return data


        # returner les commentaires
def get_video_comments(id: str):
    url_comments = f"https://www.googleapis.com/youtube/v3/commentThreads?part=snippet%2Creplies&textFormat=plainText&videoId={id}&key={api_key}"
    data = get_data(url_comments)
    comments = []
    while True:
        for item in data['items']:
            comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
            comments.append(comment)

        if 'nextPageToken' in data:
            nextPageToken = data['nextPageToken']
            url_nextPage = f"https://www.googleapis.com/youtube/v3/commentThreads?part=snippet%2Creplies&pageToken={nextPageToken}&videoId={id}&key={api_key}"
            data = get_data(url_nextPage)
        else:
            break
    return comments


        # returner le titre de video
def get_video_title(id: str):
    url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet&id={id}&key={api_key}"
    data = get_data(url)
    return data["items"][0]["snippet"]["title"]

def get_video_thumbnail(id: str):
    url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet&id={id}&key={api_key}"
    data = get_data(url)
    return data["items"][0]["snippet"]["thumbnails"]['high']['url']


def analyse(comments):
    
    allcomments = []
    polarity = []
    for comment in comments:
        try:
            allcomments.append(comment)
            try:
                if detect(comment) == 'de':
                    text = TextBlobDE(comment)  
                    x = text.sentiment.polarity
                    polarity.append(x)
                elif detect(comment) == 'fr':
                    blob = TextBlob(comment, pos_tagger=PatternTagger(), analyzer=PatternAnalyzer())
                    x = blob.sentiment[0]
                    polarity.append(x)
                else:
                    text = TextBlob(comment)  
                    x = text.sentiment.polarity
                    polarity.append(x)
            except:
                text = TextBlob(comment)  
                x = text.sentiment.polarity
                polarity.append(x)
        except:
            pass
        
        
    return allcomments, polarity
        
def calcule(polarity):
    pos = neg = neu = 0 
    for x in polarity:
        if x > 0:
            pos += 1
        elif x < 0:
            neg += 1
        else:
            neu += 1
    return pos,neg,neu

def get_video_id(url):
    query = urlparse(url)
    if query.hostname == 'youtu.be': return query.path[1:]
    if query.hostname in {'www.youtube.com', 'youtube.com'}:
        if query.path == '/watch': return parse_qs(query.query)['v'][0]
        if query.path[:7] == '/embed/': return query.path.split('/')[2]
        if query.path[:3] == '/v/': return query.path.split('/')[2]
    return None