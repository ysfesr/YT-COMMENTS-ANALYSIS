from django.shortcuts import render
from .functions import * 
from django.contrib.auth.decorators import login_required
import re
from django.contrib.auth import login, authenticate


def home(request):
    if request.method == 'POST':
        try:
            video_url = request.POST['video_url']
            video_id = get_video_id(video_url)
            thumbnail = get_video_thumbnail(video_id)
            title = get_video_title(video_id)
            comments = get_video_comments(video_id)
            length = comments.__len__
            allcomments, polarity = analyse(comments)
            mylist = zip(allcomments, polarity)
            pos, neg, neu = calcule(polarity)

            context = {"comments":mylist, "length": length, "pos":pos, "neg":neg, "neu":neu, "title":title, "thumbnail":thumbnail}
        except:
            context = {"title":0, "comments":0, "error": True}
    else:
        context = {"title":"", "comments":""}
    
    return render(request, 'main/home.html', context)

def index(request):
    return render(request,'main/index.html',{})