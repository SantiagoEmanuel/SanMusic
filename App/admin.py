from django.contrib import admin
from .models import User, Song, Playlist, LikeSong, LikePlaylist, Follow

# Register your models here.
admin.site.register(User)
admin.site.register(Song)
admin.site.register(Playlist)
admin.site.register(LikeSong)
admin.site.register(LikePlaylist)
admin.site.register(Follow)