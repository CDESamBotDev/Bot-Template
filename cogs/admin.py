import discord
from discord.ext import commands
from discord.commands import slash_command, permissions
from bot import MyClient, config


class Admin(commands.Cog):
    def __init__(self, client: MyClient):
        self.client = client

    @slash_command(guild_ids=config["guild_ids"], default_permission=False)
    @permissions.has_role(config["admin_role"])
    async def clear(self, ctx, amount: int = 5):
        """Clears an amount of messages"""
        await ctx.channel.purge(limit=amount)
        await ctx.respond(f"{amount} messages deleted!", delete_after=3)

    @slash_command(guild_ids=config["guild_ids"], default_permission=False)
    @permissions.has_role(config["admin_role"])
    async def kick(self, ctx, member: discord.Member, *, reason: str = None):
        """Kicks a member from the server"""
        await member.kick(reason=reason)
        await ctx.respond(f"{member} was kicked!", delete_after=3)

    @slash_command(guild_ids=config["guild_ids"], default_permission=False)
    @permissions.has_role(config["admin_role"])
    async def ban(self, ctx, member: discord.Member, *, reason: str = None):
        """Bans a member from the server"""
        await member.ban(reason=reason)
        await ctx.respond(f"{member} was banned!", delete_after=3)

    @slash_command(guild_ids=config["guild_ids"], default_permission=False)
    @permissions.has_role(config["admin_role"])
    async def unban(self, ctx, member: discord.Member, *, reason: str = None):
        """Unbans a member from the server"""
        await member.unban(reason=reason)
        await ctx.respond(f"{member} was unbanned!", delete_after=3)


def setup(client: MyClient):
    client.add_cog(Admin(client))
