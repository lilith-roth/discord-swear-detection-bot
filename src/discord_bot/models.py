from django.db import models
from django.utils import timezone


# Create your models here.
class DiscordServer(models.Model):
    discord_server_name = models.CharField(max_length=128, blank=True)
    discord_server_id = models.BigIntegerField(unique=True)

    discord_swear_info_chat_id = models.BigIntegerField(default=0)

    react_swears = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.discord_server_name} - {str(self.discord_server_id)}"


class DiscordServerSwearGroup(models.Model):
    group_id = models.BigIntegerField()
    discord_server = models.ForeignKey(DiscordServer, on_delete=models.CASCADE)

    def __str__(self):
        return f"{str(self.discord_server.discord_server_id)}: {str(self.group_id)}"


class DiscordServerAdminGroup(models.Model):
    group_id = models.BigIntegerField()
    discord_server = models.ForeignKey(DiscordServer, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.discord_server.discord_server_name}"


class Swear(models.Model):
    swear = models.CharField(max_length=64)
    added_by = models.BigIntegerField()
    discord_server = models.ForeignKey(DiscordServer, on_delete=models.CASCADE)
    reaction_emoji = models.CharField(max_length=64, default="😡")
    added_timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('swear', 'discord_server')

    def __str__(self):
        return self.swear


class SwearCount(models.Model):
    swear = models.ForeignKey(Swear, on_delete=models.CASCADE)
    swear_count = models.IntegerField(default=0)
    discord_user_id = models.BigIntegerField()
    discord_user_name = models.CharField(max_length=128)

    class Meta:
        unique_together = ('swear', 'discord_user_id')

    def __str__(self):
        return f"{self.swear.discord_server.discord_server_name} - {self.discord_user_name} - {self.swear.swear}: {self.swear_count}"
