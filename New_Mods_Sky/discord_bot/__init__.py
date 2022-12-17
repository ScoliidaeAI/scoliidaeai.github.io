"""This package is made to show the source code of the bot used in New Mods Sky community"""
print("\nStart of __init__; Prepping the process...")
# OS dependant path seperator
# Relative Path
# Check if path exists
# Check if path is a file
# Check if path is a directory
# Enables json handling in this file
import json
from os.path import exists, isfile, isdir, relpath
from os.path import sep as OS_SEPERATOR


class EnvironmentVariables:
    """Defines environment variables important to the package"""

    def __init__(self) -> None:
        # Path of the package
        self.root_Path = relpath(f'{__file__}{OS_SEPERATOR}..')

        # Logs path
        self.ENVIRONMENT_LOG_PATH = f"{self.root_Path}{OS_SEPERATOR}logs{OS_SEPERATOR}"

        # Referenceable filename
        self.ENVIRONMENT_VARIABLE_FILE_NAME = "var.env"
        # Path of the local env variables file

        def _verify_path(path: str, check_type: bool | str = False) -> str | tuple:
            """Verifies a given path exists and determines if the path the type should be checked"""

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

        # Handles the environment variable file path
        _expected_environment_file_path=f"{self.root_Path}{OS_SEPERATOR}{self.ENVIRONMENT_VARIABLE_FILE_NAME}"
        if _verify_path(path=_expected_environment_file_path)[0] is True: self.ENVIRONMENT_VARIABLE_FILE_PATH= _expected_environment_file_path
        else: raise OSError(
            f"Required environment file could not be found @ {_expected_environment_file_path}!",
            "\nPlease ensure that the path is correct and that the file exists and try again."
            ) 


print(f"Package= {__package__}")
print(f"Root Path= {EnvironmentVariables().root_Path}")
print("Checking for environment files...")
print(f"Path to required environment variables= {EnvironmentVariables().ENVIRONMENT_VARIABLE_FILE_PATH}")
print("Environment files found!\nLoading values required...")

print("End of __init__, transfering process to __main__...\n")
