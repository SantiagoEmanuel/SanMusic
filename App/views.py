# JSON IMPORTS
import json

# DJANGO IMPORTS
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# MODELS IMPORTS
from .models import User, Song, Playlist, LikeSong, LikePlaylist, Follow

# RANDOM IMPORTS
import random

# Create your views here.
# URLS
def index(request):
    if request.user.is_authenticated is not True:
        return HttpResponseRedirect(reverse("login"))
    else:

        # Get random song
        randomID = random.randint(1, Song.objects.count())
        randomSong = Song.objects.get(id=randomID)
        # Get all songs
        songs = Song.objects.all()

        return render(request, "App/index.html", {
            "randomSong": randomSong,
            "songs": songs
        })
        

# API'S
@login_required
def song_api(request, song_id):
    # Get song
    if request.method == "GET":
        song = Song.objects.get(id=song_id)
        # Return song
        return JsonResponse(song.serialize(), safe=False)
    # Create song
    elif request.method == "POST":
        # Get data
        data = json.loads(request.body)
        # Create song
        song = Song.objects.create(
            title=data["title"],
            artist=data["artist"],
            song=data["song"],
            album=data["album"],
            genre=data["genre"],
            lyrics=data["lyrics"],
        )
        song.save()
    # Delete song
    elif request.method == "DELETE":
        # Get song
        song = Song.objects.get(id=song_id)
        # Delete song
        song.delete()
        # Return success
        return JsonResponse({"success": True})
    elif request.method == "PUT":
        # Get data
        data = json.loads(request.body)
        # Get song
        song = Song.objects.get(id=song_id)
        # Update song
        song.title = data["title"]
        song.artist = data["artist"]
        song.album = data["album"]
        song.genre = data["genre"]
        song.lyrics = data["lyrics"]
        song.save()
    else:
        # Return petition error
        return JsonResponse({"error": "Invalid request."}, status=400)
    

    # Return song
    return JsonResponse(song.serialize(), safe=False)



# AUTHENTICATION
def login_view(request):
    if request.method != "POST":
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "App/login.html")
    else:
        username = request.POST["username"]
        password = request.POST["password"]

        # Username convert to lowercase
        username = username.lower()

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "App/login.html", {
                "error": "Invalid credentials."
            })

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))

def register_view(request):
    if request.method != "POST":
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "App/register.html")
    else:
        username = request.POST["username"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]

        # Username convert to lowercase
        username = username.lower()

        # Ensure password matches confirmation
        if password != confirmation:
            return render(request, "App/register.html", {
                "error": "Passwords must match."
            })

        try:
            user = User.objects.create_user(username, password)
            user.save()
        except:
            return render(request, "App/register.html", {
                "error": "Username already taken."
            })

        login(request, user)
        return HttpResponseRedirect(reverse("index"))