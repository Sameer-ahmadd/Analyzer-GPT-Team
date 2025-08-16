from autogen_ext.code_executors.docker import DockerCommandLineCodeExecutor
from config.constants import WORK_DIR_DOCKER, TIMEOUT_DOCKER


def get_docker_code_executor() -> DockerCommandLineCodeExecutor:
    """
    Get a DockerCommandLineCodeExecutor.
    Args:
        None
    Returns:
        DockerCommandLineCodeExecutor
    """
    docker = DockerCommandLineCodeExecutor(
        work_dir=WORK_DIR_DOCKER, timeout=TIMEOUT_DOCKER
    )
    return docker


# function to start my docker container
async def start_docker(docker):
    """
    Function to start my docker container.

    Args:
        docker: DockerCommandLineCodeExecutor
    Returns:
        None
    """
    await docker.start()


# funcotion to stop my docker container
async def stop_docker(docker):
    """
    Function to stop my docker container.

    Args:
        docker: DockerCommandLineCodeExecutor
    Returns:
        None
    """
    await docker.stop()
