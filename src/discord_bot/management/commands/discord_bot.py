from django.core.management.base import BaseCommand

import logging

from discord import app_commands, Intents, Client

from discord_bot_project.settings import DISCORD_TOKEN
from ...utils.discord_integration.events import setup_events
from ...utils.discord_integration.commands import setup_commands


class Command(BaseCommand):
    help = "Discord Bot Application"

    def handle(self, *args, **options):
        intents = Intents.default()
        intents.message_content = True
        client = Client(intents=intents)

        command_tree = app_commands.CommandTree(client)

        setup_events(client, command_tree)
        setup_commands(command_tree)
        client.run(DISCORD_TOKEN, log_level=logging.INFO)
