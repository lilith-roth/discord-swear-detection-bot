from asgiref.sync import sync_to_async
from discord import Interaction, Client
from discord.app_commands import CommandTree
from django.db import IntegrityError

from .admin_check import is_discord_mod
from ...models import Swear, DiscordServer, SwearCount
from ...utils.discord_integration.update_metadata import update_server_information


def setup_commands(command_tree: CommandTree[Client]):
    @command_tree.command(name="add_swear", description="Adds a new swear to the database")
    async def add_swear(interaction: Interaction, new_swear: str):
        """
        Bot slash command to add a new swear to the database.
        :param interaction:
        :param new_swear:
        :return:
        """
        if not await is_discord_mod(interaction.user.roles, interaction.guild_id):
            return
        discord_server_instance, created = await DiscordServer.objects.aget_or_create(
            discord_server_id=interaction.guild_id,
        )
        await update_server_information(discord_server_instance, interaction.guild.name)
        if created:
            discord_server_instance.save()
        new_swear = Swear(
            swear=new_swear,
            added_by=interaction.user.id,
            discord_server=discord_server_instance
        )
        try:
            await new_swear.asave()
            await interaction.response.send_message(
                f"{interaction.user} added {new_swear} to the swear list!"
            )
        except IntegrityError:
            await interaction.response.send_message(
                f"{new_swear} could not be saved. Likely already stored!"
            )

    @command_tree.command(
        name="remove_swear", description="Removes a swear in the database"
    )
    async def remove_swear(interaction: Interaction, swear_to_remove: str):
        """
        Bot slash command to remove a swear from database.
        :param interaction:
        :return:
        """
        if not is_discord_mod(interaction.user.roles, interaction.guild_id):
            return
        discord_server_instance, _ = await DiscordServer.objects.aget_or_create(
            discord_server_id=interaction.guild_id,
        )
        await update_server_information(discord_server_instance, interaction.guild.name)
        swear = Swear.objects.get(swear=swear_to_remove, discord_server=discord_server_instance)
        swear.delete()
        await interaction.response.send_message(
            f"{interaction.user} removed {swear_to_remove} to the swear list!"
        )

    @command_tree.command(
        name="list_swears", description="Lists all swears in the database"
    )
    async def list_swears(interaction: Interaction):
        """
        Bot slash command to retrieve all swears in the database.
        :param interaction:
        :return:
        """
        discord_server_instance, created = await DiscordServer.objects.aget_or_create(
            discord_server_id=interaction.guild_id,
        )
        await update_server_information(discord_server_instance, interaction.guild.name)
        swear_list = Swear.objects.filter(discord_server=discord_server_instance)
        reply_msg = "## Swear List:\n\n"
        async for swear in swear_list:
            reply_msg += f"- {swear.swear}\n"
        await interaction.response.send_message(reply_msg)

    @command_tree.command(
        name="statistics", description="Lists a swear statistic"
    )
    async def list_swear_statistic(interaction: Interaction):
        """
        Bot slash command to retrieve a statistic of swears in the current server.
        :param interaction:
        :return:
        """
        discord_server_instance, created = await DiscordServer.objects.aget_or_create(
            discord_server_id=interaction.guild_id,
        )
        await update_server_information(discord_server_instance, interaction.guild.name)
        swear_list = Swear.objects.filter(discord_server=discord_server_instance)
        reply_msg = "# Swear Statistics:\n\n"
        async for swear in swear_list:
            swear_count = SwearCount.objects.filter(swear=swear).order_by("-swear_count")
            reply_msg += f"## {swear.swear}\n"
            async for count in swear_count:
                reply_msg += f"- *{count.discord_user_name}*: {count.swear_count}\n"
            reply_msg += "\n"
        await interaction.response.send_message(reply_msg)
