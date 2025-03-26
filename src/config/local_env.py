import os
from dotenv import load_dotenv
load_dotenv()

class AppConfig:
    """Singleton class to store configuration values for Snowflake and Azure."""
    
    # Snowflake Configuration
    SNOWFLAKE_USER = os.getenv("SF_USER")
    SNOWFLAKE_PASSWORD = os.getenv("SF_PASSWORD")
    SNOWFLAKE_ACCOUNT = os.getenv("SF_ACCOUNT")
    SNOWFLAKE_WAREHOUSE = os.getenv("SF_WAREHOUSE")
    SNOWFLAKE_DATABASE = os.getenv("SF_DATABASE")
    SNOWFLAKE_ROLE = os.getenv("SF_ROLE")

    # Azure Configuration
    AZURE_ENDPOINT = os.getenv("ENDPOINT")
    AZURE_KEY = os.getenv("KEY")
    AZURE_MODEL = os.getenv("MODEL")
    AZURE_EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL")

    @classmethod
    def get_snowflake_config(cls):
        """Returns Snowflake configuration as a dictionary."""
        return {
            "user": cls.SNOWFLAKE_USER,
            "password": cls.SNOWFLAKE_PASSWORD,
            "account": cls.SNOWFLAKE_ACCOUNT,
            "warehouse": cls.SNOWFLAKE_WAREHOUSE,
            "database": cls.SNOWFLAKE_DATABASE
        }

    @classmethod
    def get_azure_config(cls):
        """Returns Azure configuration as a dictionary."""
        return {
            "endpoint": cls.AZURE_ENDPOINT,
            "key": cls.AZURE_KEY,
            "model": cls.AZURE_MODEL
        }

