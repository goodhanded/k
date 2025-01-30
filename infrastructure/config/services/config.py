import os
from dotenv import load_dotenv

class Config:
    """
    A configuration service that reads environment variables
    and falls back to values defined in a .env file.
    """

    def __init__(self, dotenv_path: str = '.env'):
        """
        Initialize the ConfigService, loading the .env file.
        
        :param dotenv_path: The path to the .env file (default is .env).
        """
        # Load environment variables from dotenv_path, but do NOT override
        # already-set environment variables
        load_dotenv(dotenv_path, override=False)

    def get(self, key: str, default=None):
        """
        Return the value for environment variable `key`.
        If it's not found, return `default`.
        
        :param key: The environment variable name.
        :param default: Value to return if `key` is not found.
        :return: The environment variable or default value.
        """
        return os.getenv(key, default)

    def require(self, key: str):
        """
        Return the value for environment variable `key`.
        Raises an error if not found.
        
        :param key: The environment variable name.
        :return: The environment variable value.
        :raises ValueError: If `key` is not found or empty.
        """
        value = os.getenv(key)
        if not value:
            raise ValueError(f"Required environment variable '{key}' is not set.")
        return value