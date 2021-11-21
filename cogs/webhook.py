import discord
from discord.ext import commands
from discord.commands import slash_command, permissions
from discord import Webhook, Option
from bot import MyClient, config


class Webhook(commands.Cog):
    def __init__(self, client: MyClient):
        self.client = client

    @slash_command(guild_ids=config["guild_ids"], default_permission=False)
    @permissions.has_role(*config["admin_roles"])
    async def echo(
        self,
        ctx: discord.ApplicationContext,
        channel: Option(discord.TextChannel),
        message: Option(str),
        username: Option(str),
        avatar_url: Option(discord.Member),
    ):
        """Echoes a message"""
        avatar_url = avatar_url.avatar.url
        done = False
        for hook in await ctx.guild.webhooks():
            if hook.channel.id == channel.id:
                await hook.send(message, username=username, avatar_url=avatar_url)
                done = True
        if not done:
            hook = await channel.create_webhook(name="Echo")
            await hook.send(message, username=username, avatar_url=avatar_url)
        await ctx.respond("Done!")


def setup(client: MyClient):
    client.add_cog(Webhook(client))
