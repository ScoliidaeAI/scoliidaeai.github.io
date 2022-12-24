"""The main handler of the package"""

from . import setup
from os import sep as OS_SEPERATOR
from typing import Callable

import discord
from discord.ext import commands

bot= commands.Bot(
    command_prefix="/",
    help_command=None,
    description= "Connect the bot to discord and handles all of the code relating to it",
    intents= discord.Intents.all()
)
class botClient(commands.Bot):
    """Handles all bot functions and delegate workers"""
    def __init__(self) -> None:
        """Handles all bot functions and delegate workers"""; print("botClient has been initialized")
        # Runs the bot until it is fully disconnected from Discord
        def _main_setup() -> Callable:
            """Makes sure everything that needs setup for scripts to run is pre-handled"""; print("_main_setup() has been accessed\n")
            setup.environment_handler() # Sets up the environment
            # Log handler
            setup.logger(f"New_Mods_Sky{OS_SEPERATOR}logs{OS_SEPERATOR}discord.log")
            # Gets the public token and uses it to lookup the secret token to initialize the bot
            secret_token= lambda Public_Token=setup._discord_bot_token(): setup.lookup_token_by_alias(public_token=Public_Token)[1]

            # Supress the default log handler and default help command
            print("Gathered all important information. Connecting to Discord's API...", ); bot.run(secret_token(), log_handler=None)
        
        _main_setup(); print("Disconnected from Discord! Shutting down bot...")
        

    @bot.event
    async def on_ready():
        """Event that triggers when the bot has successfully connected to Discord's API"""
        print(f'{bot.user.name}#{bot.user.discriminator} <@{bot.user.id}>, is connected to Discord!')
        try:
            synced= await bot.tree.sync()
            print(f"Synced {len(synced)} command(s)")
        except Exception as e:
            print(e)

    @bot.tree.command(name="help")
    async def hello(self, interaction: discord.Interaction):
        """Help command to overwrite the default"""; print(f"Responding to {interaction.user.name}#{interaction.user.discriminator} <@{interaction.user.id}>")
        response= "Test help command"
        await interaction.response.send_message(content=response, ephemeral=True)
        print(f"responded to {interaction.user.name}#{interaction.user.discriminator} <@{interaction.user.id}> with: '''{response}'''")
botClient(); quit()