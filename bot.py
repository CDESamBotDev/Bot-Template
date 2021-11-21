import discord, json, os
from discord import ApplicationContext
from discord.commands import permissions

with open("config.json") as f:
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


client = MyClient(intents=discord.Intents.default())

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
