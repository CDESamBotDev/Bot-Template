import discord, json, os
from discord import ApplicationContext
from discord.commands import permissions

with open('config.json') as f:
    config = json.load(f)

class MyClient(discord.Bot):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def on_ready(self):
        print(f'Logged in as {self.user}')

        # await self.change_presence(status=discord.Status.online)
        # await self.change_presence(activity=discord.Activity(type=discord.ActivityType.watching,name='Panel API'))

client = MyClient(intents=discord.Intents.default())

# Basic Commands

@client.command()
async def ping(ctx: ApplicationContext):
    """Replies with the bot's ping"""
    await ctx.respond(f'Pong! {int(client.latency*1000)} ms')

@client.command(default_permissioin=False)
@permissions.is_owner()
async def reload(ctx, extension: str):
    """Reloads a cogs extension"""
    client.reload_extension(f'cogs.{extension}')
    await ctx.respond(f'Reloaded {extension}')

# Running Bot
if __name__ == '__main__':

    # Load Extensions
    for filename in os.listdir('cogs'):
        if filename.endswith('.py'):
            client.load_extension(f'cogs.{filename[:-3]}')
            print(f'Loaded extension: {filename[:-3]}')

    # Run Bot
    client.run(config['token'])