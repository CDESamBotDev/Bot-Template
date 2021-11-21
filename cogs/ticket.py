import discord, json, asyncio
from discord import ApplicationContext
from discord.ext import commands
from discord.commands import slash_command
from bot import MyClient, config


class Ticket(commands.Cog):
    def __init__(self, client: MyClient):
        self.client = client

    @slash_command(guild_ids=config["guild_ids"])
    async def ticket(self, ctx: ApplicationContext):
        """Creates a ticket"""

        with open("data/tickets.json", "r") as f:
            data = json.load(f)

        category = self.client.get_channel(config["ticket"]["open_cat"])
        overwrites = {
            ctx.guild.get_role(ctx.guild.id): discord.PermissionOverwrite(
                read_messages=False, send_messages=False
            ),  # Everyone Role
            ctx.author: discord.PermissionOverwrite(
                read_messages=True, send_messages=True
            ),  # The Author
            self.client.user: discord.PermissionOverwrite(
                read_messages=True, send_messages=True
            ),  # The Bot
        }

        ticket = await ctx.guild.create_text_channel(
            name=f'{ctx.author.display_name}-{data["num"]}',
            category=category,
            overwrites=overwrites,
        )

        data["open"].append(ticket.id)

        # Ticket Creation Message
        ticket_embed = discord.Embed(colour=0x50C878, title="Ticket Created")
        await ctx.respond(embed=ticket_embed)

        # Welcome Message

        interior_ticket_embed = discord.Embed(
            colour=0x50C878,
            title=f'Ticket {ctx.author.display_name}-{data["num"]}',
            description=f"Welcome to your ticket. Someone will be with you as soon as possible, but in the meantime, providing some information about your issue will help us fix your problem faster.",
        )

        await ticket.send(
            content=f"Welcome {ctx.author.mention}!", embed=interior_ticket_embed
        )

        data["num"] += 1

        with open("data/tickets.json", "w") as f:
            json.dump(data, f, indent=4)

    @slash_command(guild_ids=config["guild_ids"])
    async def close(self, ctx: ApplicationContext):
        """Closes a ticket"""

        with open("data/tickets.json", "r") as f:
            data = json.load(f)

        if ctx.channel.id in data["open"]:
            data["open"].remove(ctx.channel.id)

            with open("data/tickets.json", "w") as f:
                json.dump(data, f, indent=4)

            await ctx.respond(f"Ticket closed!")

            new_cat = self.client.get_channel(config["ticket"]["closed_cat"])
            overwrites = {
                ctx.guild.get_role(ctx.guild.id): discord.PermissionOverwrite(
                    read_messages=False, send_messages=False
                ),  # Everyone Role
                ctx.author: discord.PermissionOverwrite(
                    read_messages=False, send_messages=False
                ),  # The Author
                self.client.user: discord.PermissionOverwrite(
                    read_messages=True, send_messages=True
                ),  # The Bot
            }
            await asyncio.sleep(10)
            await ctx.channel.edit(category=new_cat, overwrites=overwrites)

        else:
            await ctx.respond(f"You do not have permission to close this ticket!")


def setup(client: MyClient):
    client.add_cog(Ticket(client))
