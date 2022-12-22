"""The main handler of the package"""

# Triggers the script
def __main_setup() -> None:
    """Makes sure everything that needs setup for scripts to run is pre-handled"""

    from . import setup

    setup.environment_handler() # Sets up the environment
    # Gets the public token and uses it to lookup the secret token to initialize the bot
    secret_token= lambda Public_Token=setup._discord_bot_token(): setup.lookup_token_by_alias(public_token=Public_Token)

    print(secret_token())
if __package__ is not None and __name__=="__main__": __main_setup() # Starts the script