import logging

from discord import Client, Message
from ...models import Swear, SwearCount
from ...utils.discord_integration.update_metadata import update_server_information


async def handle_swear(swear: Swear, message: Message, client: Client):
    """
    Manages an incoming detected swear.
    :param swear:
    :param message:
    :return:
    """
    server_instance = await Swear.objects.select_related('discord_server').aget(swear=swear)
    await update_server_information(server_instance.discord_server, message.guild.name)
    await update_swear_statistic(swear, message.author.id, message.author.name)
    if server_instance.discord_server.react_swears is True:
        await message.add_reaction(swear.reaction_emoji)
    swear_count_channel = client.get_channel(server_instance.discord_server.discord_swear_info_chat_id)
    if swear_count_channel == 0:
        logging.warning("No count channel defined!")
    else:
        await swear_count_channel.send(f"Swear by {message.author}: {swear}")


async def update_swear_statistic(swear: Swear, discord_user_id: int, discord_user_name: str):
    new_count, _ = await SwearCount.objects.aget_or_create(
        swear=swear,
        discord_user_id=discord_user_id
    )
    new_count.discord_user_name = discord_user_name
    new_count.swear_count = new_count.swear_count + 1
    await new_count.asave()
