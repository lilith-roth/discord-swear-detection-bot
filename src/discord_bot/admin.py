from django.contrib import admin

from .models import DiscordServer, DiscordServerSwearGroup, Swear, SwearCount, DiscordServerAdminGroup

# Register your models here.
admin.site.register(DiscordServer)
admin.site.register(DiscordServerSwearGroup)
admin.site.register(Swear)
admin.site.register(SwearCount)
admin.site.register(DiscordServerAdminGroup)
