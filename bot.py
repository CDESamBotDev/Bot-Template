import discord, json, os
from discord import ApplicationContext
from discord.commands import permissions

with open("data/config.json") as f:
    config = json.load(f)


class MyClient(discord.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def on_ready(
        self,
    ):  # event function, which is ran when the bot is 'ready'/online
        print(f"Logged in as {self.user}")

        # Code to change the Bot's status
        # await self.change_presence(status=discord.Status.online)
        # await self.change_presence(activity=discord.Activity(type=discord.ActivityType.playing,name='example'))

    async def on_member_join(
        self, member: discord.Member
    ):  # Event which is ran when a member joins a guild

        # Welcome message
        channel = self.get_channel(config["welcome_channel"])

        welcome_embed = discord.Embed(
            title=f"Welcome to {member.guild.name}!",
            description=f"Welcome {member.mention} to the server!",
            color=discord.Color.green(),
        )

        welcome_embed.set_thumbnail(url=member.avatar.url)

        await channel.send(embed=welcome_embed)

        # Update Stats Channels
        await self.update_guild_stats(member)

    async def on_member_remove(self, member: discord.Member):  # ran on member leave
        # Update Stats Channels
        await self.update_guild_stats(member)

    async def update_guild_stats(self, member: discord.Member):
        # Update Total Channel
        await self.get_channel(config["member_stats"]["total"]).edit(
            name=f"Total Members: {len(member.guild.members)}"
        )
        # Update Members Channel
        member_count = len([m for m in member.guild.members if not m.bot])
        await self.get_channel(config["member_stats"]["members"]).edit(
            name=f"Member Count: {member_count}"
        )
        # Update Bots Channel
        await self.get_channel(config["member_stats"]["bots"]).edit(
            name=f"Bot Count: {len(member.guild.members)-member_count}"
        )


intents = discord.Intents.default()
intents.members = True

client = MyClient(intents=intents)

# Basic Commands


@client.command()  # creates a global slash command
async def ping(ctx: ApplicationContext):
    """Replies with the bot's ping"""  # the command description is supplied as a docstring
    await ctx.respond(f"Pong! {int(client.latency*1000)} ms")


@client.command(
    default_permissioin=False
)  # creates a global slash command with permission overrides
@permissions.is_owner()  # sets permission override to be bot owner
async def reload(ctx, extension: str):
    """Reloads a cogs extension"""
    client.reload_extension(f"cogs.{extension}")
    await ctx.respond(f"Reloaded {extension}")


# Running Bot
if __name__ == "__main__":  # Only runs the bot when the bot.py file is run directly

    # Load Extensions from the /cogs directory
    for filename in os.listdir("cogs"):
        if filename.endswith(".py"):
            client.load_extension(f"cogs.{filename[:-3]}")
            print(f"Loaded extension: {filename[:-3]}")

    # Runs the bot using the token specified in config.json
    client.run(config["token"])
