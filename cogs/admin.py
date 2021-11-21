import discord
from discord.ext import commands
from discord.commands import slash_command, permissions
from bot import MyClient, config


class Admin(commands.Cog):
    def __init__(self, client: MyClient):
        self.client = client

    @slash_command(
        guild_ids=config["guild_ids"], default_permission=False
    )  # creates a command for the specified guilds, with a permission override
    @permissions.has_any_role(
        *config["admin_roles"]
    )  # example with admin role permissions
    async def clear(self, ctx, amount: int = 5):
        """Clears an amount of messages"""
        await ctx.channel.purge(limit=amount)
        await ctx.respond(f"{amount} messages deleted!", delete_after=3)

    @slash_command(guild_ids=config["guild_ids"], default_permission=False)
    @permissions.has_any_role(*config["admin_roles"])
    async def kick(self, ctx, member: discord.Member, *, reason: str = None):
        """Kicks a member from the server"""
        await member.kick(reason=reason)
        await ctx.respond(f"{member} was kicked!", delete_after=3)

    @slash_command(guild_ids=config["guild_ids"], default_permission=False)
    @permissions.has_any_role(*config["admin_roles"])
    async def ban(self, ctx, member: discord.Member, *, reason: str = None):
        """Bans a member from the server"""
        await member.ban(reason=reason)
        await ctx.respond(f"{member} was banned!", delete_after=3)

    @slash_command(guild_ids=config["guild_ids"], default_permission=False)
    @permissions.has_any_role(*config["admin_roles"])
    async def unban(self, ctx, member_id: str):
        """Unbans a member from the server"""
        banned_users = await ctx.guild.bans()

        for ban_entry in banned_users:
            if ban_entry.user.id == int(member_id):
                await ctx.guild.unban(ban_entry.user)
                await ctx.respond(f"Unbanned {ban_entry.user}")
                return
        await ctx.respond("Unable to Unban member")


def setup(client: MyClient):
    client.add_cog(Admin(client))
