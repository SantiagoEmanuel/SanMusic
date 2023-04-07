from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    pass

class Song(models.Model):
    title = models.CharField(max_length=64)
    artist = models.CharField(max_length=64)
    song = models.FileField(upload_to="songs/")
    album = models.CharField(max_length=64)
    genre = models.CharField(max_length=64)
    lyrics = models.TextField(blank=True)

    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "artist": self.artist,
            "song": self.song.url,
            "album": self.album,
            "genre": self.genre,
            "lyrics": self.lyrics
        }
    
class Playlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="playlists")
    title = models.CharField(max_length=64)
    songs = models.ManyToManyField(Song, blank=True, related_name="playlists")

    def serialize(self):
        return {
            "id": self.id,
            "user": self.user,
            "title": self.title,
            "songs": self.songs
        }
    
class LikeSong(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likedSongs")
    song = models.ForeignKey(Song, on_delete=models.CASCADE, related_name="likedBy")

    def serialize(self):
        return {
            "id": self.id,
            "user": self.user,
            "song": self.song
        }
    
class LikePlaylist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likedPlaylists")
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE, related_name="likedBy")

    def serialize(self):
        return {
            "id": self.id,
            "user": self.user,
            "playlist": self.playlist
        }
    
class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followed")
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")

    def serialize(self):
        return {
            "id": self.id,
            "user": self.user,
            "follower": self.follower
        }