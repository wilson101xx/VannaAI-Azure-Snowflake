from openai import AzureOpenAI
from src.config.local_env import AppConfig


def Azure_Client():
    client = AzureOpenAI(
        azure_endpoint=AppConfig.AZURE_ENDPOINT,
        api_version="2024-05-01-preview",
        api_key=AppConfig.AZURE_KEY
        )
    return client



if __name__ == "__main__":
    client = Azure_Client()

    print(client)