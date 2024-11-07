from ...models import DiscordServer


async def update_server_information(server_instance: DiscordServer, server_name: str):
    if server_instance.discord_server_name == server_name:
        return
    server_instance.discord_server_name = server_name
    await server_instance.asave()
