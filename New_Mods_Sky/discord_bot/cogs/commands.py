"""Cogs file handling all commands for the bot"""

import discord
from discord.ext import commands
bot=commands.Bot

class botCommands(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot:commands.Bot= bot

    @commands.command(name="sync_all_cmd")
    @commands.has_role("Bot Developer")
    async def sync_all_commands(self, interaction:discord.Interaction) -> None:
        """Syncs all of the commands registered with the bot"""

        await interaction.response.send_message("this is a test")

async def setup(bot):
    await bot.add_cog(botCommands())

        
