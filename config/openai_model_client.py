from autogen_ext.models.openai import OpenAIChatCompletionClient
from config.config import config


# function to get openai model client
def get_model_client():
    """
    Function to get openai model client.
    """
    openai_model_client = OpenAIChatCompletionClient(
        model="gpt-4o-mini", api_key=config.openai_api_key
    )
    return openai_model_client
