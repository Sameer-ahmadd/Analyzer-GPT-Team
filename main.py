import asyncio

from autogen_agentchat.base import TaskResult
from autogen_agentchat.messages import TextMessage
from config.docker_utils import get_docker_code_executor, start_docker, stop_docker
from config.openai_model_client import get_model_client
from teams.analyzer_gpt import Analyzer_GPT_Team


# main function.
async def main():
    openai_model_client = get_model_client()
    docker = get_docker_code_executor()

    team = Analyzer_GPT_Team(docker, openai_model_client)

    try:
        task = "can you tell me the number of rows in titanic.csv in your working directory?"
        await start_docker(docker)

        async for message in team.run_stream(task=task):
            print("=" * 40)
            if isinstance(message, TextMessage):
                print(message.source, " : ", message.content)
            elif isinstance(message, TaskResult):
                print("Stop_Reason", message.stop_reason)

    except Exception as e:
        print(e)
    finally:
        await stop_docker(docker)


if __name__ == "__main__":
    asyncio.run(main())
