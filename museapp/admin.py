from django.contrib import admin
from museapp.models import UserProfile, Comment, MusicProject, ExtraFile
# Register your models here.
admin.site.register(Comment)
admin.site.register(MusicProject)
admin.site.register(ExtraFile)
