from autogen_agentchat.agents import CodeExecutorAgent
from autogen_core import CancellationToken
from autogen_ext.code_executors.docker import DockerCommandLineCodeExecutor
import asyncio
from autogen_agentchat.messages import TextMessage

# initiazling a DockerCommandLineCodeExecutor
docker = DockerCommandLineCodeExecutor(work_dir="temp", timeout=120)


# function to get a CodeExecutorAgent
def GetCodeExecutorAgent(code_executor) -> CodeExecutorAgent:
    """
    Get a CodeExecutorAgent.

    Args:
        docker: DockerCommandLineCodeExecutor

    Returns:
        CodeExecutorAgent
    """
    code_executor_agent = CodeExecutorAgent(
        name="CodeExecutorAgent",
        description="A agent that can execute code in a docker container.",
        code_executor=code_executor,
    )

    return code_executor_agent


async def main():
    # start the Docker container
    await docker.start()

    # get the code executor agent
    code_executor_agent = GetCodeExecutorAgent(docker)

    # create a task
    task = TextMessage(
        content=""" Here is the Python code you need to execute:
```python
print("Hello, World!")
```
        Please execute the code and return the output.
        """,
        source="user",
    )

    try:
        result = await code_executor_agent.on_messages(
            messages=[task], cancellation_token=CancellationToken()
        )
        print("Result: ", result)
    except Exception as e:
        print("Error: ", e)
    finally:
        await docker.stop()


if __name__ == "__main__":
    asyncio.run(main())
