import discord
from discord.ext import commands
from discord.commands import slash_command
from discord import ApplicationContext
from bot import MyClient, config


class Base(commands.Cog):  # creates the cog class
    def __init__(self, client: MyClient):
        self.client = client

    # Base Command
    @slash_command()
    async def base(self, ctx: ApplicationContext):
        await ctx.respond("base")


def setup(client: MyClient):
    client.add_cog(Base(client))
