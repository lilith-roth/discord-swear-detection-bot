from typing import List

from discord import Role

from ...models import DiscordServerAdminGroup

async def is_discord_mod(discord_user_groups: List[Role], discord_server_id: int) -> bool:
    discord_swear_group_ids = DiscordServerAdminGroup.objects.filter(discord_server__discord_server_id=discord_server_id)
    in_group = False
    for role in discord_user_groups:
        async for swear_group in discord_user_groups:
            if role.id == swear_group.group_id:
                in_group = True
    return in_group
