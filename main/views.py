from django.shortcuts import render, redirect
from .functions import * 
from django.contrib.auth.decorators import login_required
import re
from django.contrib.auth import login, authenticate
from .forms import SignUpForm

def home(request):
    if request.user.is_authenticated:
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
    else:
        return render(request, "index.html", {})


from django.contrib.auth.models import User

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})



def index(request):
    return render(request,'',{})