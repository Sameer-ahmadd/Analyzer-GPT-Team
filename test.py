from autogen_core.models import UserMessage
from autogen_ext.models.openai import OpenAIChatCompletionClient
from config.config import config


async def main():
    model_client = OpenAIChatCompletionClient(
        model="gemini-1.5-flash-8b",
        api_key=config.gemini_api_key,
    )

    response = await model_client.create(
        [UserMessage(content="What is the capital of France?", source="user")]
    )
    print(response)
    await model_client.close()


# Run the async function
import asyncio

asyncio.run(main())
