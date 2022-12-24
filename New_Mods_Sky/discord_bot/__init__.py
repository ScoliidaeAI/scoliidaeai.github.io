"""This package is made to show the source code of the bot used in New Mods Sky community"""

class setup:
    """Sets up the python environment for running the scripts"""

    from os.path import relpath, sep as OS_SEPERATOR
    import logging

    def _verify_path(path: str, check_type: bool | str = False) -> str | tuple:
        """Verifies a given path exists and determines if the path the type should be checked"""
        
        from os.path import exists, isfile, isdir

        if exists(path) is not False: # Check if the given path exists
            match check_type: # Compare potential values for "check_type"
                case False if check_type is False: return exists(path), "" # Checks if "check_type" is "False"
                case "dir" | "directory":
                    return exists(path), isdir(path) # Returns the path exists and if it's a directory
                case "file":
                    return exists(path), isfile(path) # Returns the path exists and if it's a file
                case _: # Default "else" statement for if other math cases fail
                    return exists(path), "unknown type"
        else: return exists(path), "unknown type"
    def __init__(self) -> None: pass
    
    @classmethod
    def environment_handler(self): # must be called from within another function
        """
        ### handles access to the environment call to set the bot's api key to avoid exposure
        """

        from os import environ, getenv
        
        def _call_stack() -> tuple:
            """
            Checks the current call stack and returns a tuple of:

            [0]: Name of current function calling this one (the child)
            [1]: Name of function calling the functiong thats calling this one (the parent)

            ---

            returns child, parent
            """
            # Function calling the function calling this one: the grandparent (if any)
            # Function calling this one: the parent
            # Current function: child
            #
            # return child, parent
            from inspect import stack; return stack()[1][3], [
                stack()[2][3] if str(stack()[2][3]) != "<module>" and str(stack()[2][3]) != "<lambda>" else None][0]
        def _read_from_environment_file(file_path:str, grandparent:str) -> None|str:
            """
            ### Reads contents from the environment file
            
            - Filters results

            - Adds filtered results to global environment

            ---

            - Returns none if contents were added to environment

            - Returns api_key if called by the filtered function
            """
            
            if file_path.strip()=='': raise AttributeError("file_path is blank")
            elif grandparent.strip()=='': raise AttributeError("grandparent is blank")
            elif ' ' in grandparent.strip(): raise AttributeError("grandparent is an invalid name")
            else: file_path=file_path.strip(); grandparent=grandparent.strip()

            match grandparent: # Checks access
                case "_main_setup"|"_discord_bot_token": pass
                case _: raise SystemError("Unallowed access attempted to retrieve environment information")

            def read_raw() -> dict:
                """Reads the environment file and returns filtered data (skips template at beginning)"""

                from json import loads

                # Queue all entries found in file and store all values (searches for the start of the json in the file)
                with open(file_path, "r") as LocalEnvVar: # Opens the file as a referenceable by using its path
                    while True: # Loop over unneeded lines in the file
                        current_section= LocalEnvVar.readline() # Reads the current line

                        # Checks for the end of the template within the file
                        if current_section.upper().strip()=="### END OF TEMPLATE ###":
                            LocalEnvVar.readline() # Skips the empty line after the end of the template
                            values_raw=LocalEnvVar.readlines() # Store everything else remaining in the file to a variable
                            del LocalEnvVar # Delete raw file read access as it wont be needed past this point

                            cleaned_values_raw=list() # placeholder list while formatting lines
                            for index in values_raw: cleaned_values_raw.append(index.strip()) # remove all excess whitespace from each line
                            # store list as a string and remove prior "raw" variables required for it
                            string_values= "".join(cleaned_values_raw).strip(); del values_raw, cleaned_values_raw
                            # convert to string a json object
                            json_object= loads(string_values); del string_values
                            return json_object
            json_output_fromLocalEnvFile=lambda: read_raw()

            match grandparent:
                case "_discord_bot_token": return json_output_fromLocalEnvFile()["bot"]["token"]["api_public"]
                case _:
                    if getenv("local_env_file") is None:
                        environ["local_env_file"]=str(json_output_fromLocalEnvFile()).strip()
                    return

        child, parent=_call_stack() # Store call stack outputs for current function and parent to a file
        return _read_from_environment_file(file_path=setup.ENVIRONMENT_VARIABLE_FILE_PATH, grandparent=parent) # gather filtered values
    @classmethod
    def _discord_bot_token(self):
        """Gets the public bot token"""
        return setup.environment_handler()
    @classmethod
    def lookup_token_by_alias(self, public_token:str): # can be called at anytime
        """
        ### Takes a passed api public token and returns value of it's secret token

        This is being used in the obfuscation of the secret token from the debugger when being referenced

        ---

        If alias or secret cannot be found, return value will be a tuple

        - "token_not_found", "description"

        If all values found, will return a tuple

        - "token_found", "api_secret"
        """

        from json import loads
        from os import getenv
        if getenv("local_env_file") is None:
            return "token_not_found", "local environment file has not been passed to the environment yet"
        
        # Checks api tokens in the environment for if a value should be returned if possible to begin with
        return_value= [
            loads(
                getenv("local_env_file").replace( "'",'"')
            )["bot"]["token"]["api_secret"] if loads(
                getenv("local_env_file").replace( "'",'"')
            )["bot"]["token"]["api_public"] == public_token.strip() else None
        ][0]
        if return_value is not None: return "token_found", return_value
        else: return "token_not_found", "invalid token passed, could not retrieve secret token"
    @classmethod
    def logger(self, path:str, log_level=logging.INFO):
        """Custom logger for the bot to use in outputs"""

        #import logging
        import logging.handlers

        logger = logging.getLogger('discord')
        logger.setLevel(log_level)
        logging.getLogger('discord.http').setLevel(logging.DEBUG)

        handler = logging.handlers.RotatingFileHandler(
            filename=path,
            encoding='utf-8',
            maxBytes=32 * 1024 * 1024,  # 32 MiB
            backupCount=5,  # Rotate through 5 files
        )
        dt_fmt = '%Y-%m-%d %H:%M:%S'
        formatter = logging.Formatter('[{asctime}] [{levelname:<8}] {name}: {message}', dt_fmt, style='{')
        handler.setFormatter(formatter)
        logger.addHandler(handler)


    # Path of the package
    root_Path = relpath(f'{__file__}{OS_SEPERATOR}..')
    # Logs path
    ENVIRONMENT_LOG_PATH = f"{root_Path}{OS_SEPERATOR}logs{OS_SEPERATOR}"
    # Referenceable filename
    ENVIRONMENT_VARIABLE_FILE_NAME = "var.env"
    # Handles the environment variable file path
    _expected_environment_file_path=f"{root_Path}{OS_SEPERATOR}{ENVIRONMENT_VARIABLE_FILE_NAME}"
    if _verify_path(path=_expected_environment_file_path)[0] is True: ENVIRONMENT_VARIABLE_FILE_PATH= _expected_environment_file_path
    else: raise OSError(f"Required environment file could not be found @ {_expected_environment_file_path}!",
        "\nPlease ensure that the path is correct and that the file exists and try again.")

    COGS= []
