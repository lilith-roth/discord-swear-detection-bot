import logging

from discord import Client
from discord.app_commands import CommandTree
from ..handlers.swear_handlers import handle_swear

from ...models import DiscordServerSwearGroup, Swear


def setup_events(client: Client, command_tree: CommandTree[Client]):
    @client.event
    async def on_ready():
        """
        Runs as soon as the Discord bot has connected.
        :return:
        """
        await command_tree.sync()
        logging.info("Logged on as %s!", client.user)

    @client.event
    async def on_message(message):
        """
        On new message handler.
        :param message:
        :return:
        """
        logging.debug("Message from %s: %s", message.author, message.content)
        if message.author.id == client.user.id:
            return
        in_group = False

        discord_swear_group_ids = DiscordServerSwearGroup.objects.filter(discord_server__discord_server_id=message.guild.id)

        for role in message.author.roles:
            async for swear_group in discord_swear_group_ids:
                if role.id == swear_group.group_id:
                    in_group = True
        if not in_group:
            return

        discord_server_swear_list = Swear.objects.filter(discord_server__discord_server_id=message.guild.id)

        async for swear in discord_server_swear_list:
            if swear.swear.lower() in message.content.lower():
                await handle_swear(swear, message, client)
