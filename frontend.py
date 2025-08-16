import asyncio
import streamlit as st
import os
from config.openai_model_client import get_model_client
from config.docker_utils import get_docker_code_executor, start_docker, stop_docker
from teams.analyzer_gpt import Analyzer_GPT_Team
from autogen_agentchat.messages import TextMessage
from autogen_agentchat.base import TaskResult


async def run_gpt_analyzer(docker, openai_model_client, task):
    """
    Function to run the GPT analyzer.

    Args:
        docker: Docker code executor.
        openai_model_client: OpenAI model client.
        task: The task to analyze.

    Returns:
        str: The result of the GPT analyzer.
    """
    try:
        print(f"Starting Docker container...")
        await start_docker(docker)
        print(f"Docker container started successfully")

        # Create a new team for each analysis
        print(f"Creating Analyzer GPT team...")
        team = Analyzer_GPT_Team(docker, openai_model_client)
        print(f"Team created successfully")

        # Store the team in session state for potential reuse
        st.session_state.autogen_team = team

        print(f"Starting analysis with task: {task.content}")
        async for message in team.run_stream(task=task):
            if isinstance(message, TextMessage):
                msg = f"{message.source} : {message.content}"
                print(msg)
                st.session_state.messages.append(msg)
                st.markdown(msg)
            elif isinstance(message, TaskResult):
                print("Stop_Reason", message.stop_reason)
                st.markdown(f"Task completed: {message.stop_reason}")
                st.session_state.messages.append(
                    f"Task completed: {message.stop_reason}"
                )
        return None
    except Exception as e:
        print(f"Error in run_gpt_analyzer: {e}")
        import traceback

        traceback.print_exc()
        return str(e)
    finally:
        print(f"Stopping Docker container...")
        await stop_docker(docker)
        print(f"Docker container stopped")


def main():
    st.title("Analyzer GPT - Digital Data Analyzer")

    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "autogen_team" not in st.session_state:
        st.session_state.autogen_team = None

    uploaded_file = st.file_uploader("Upload your CSV file", type="csv")

    # Display previous messages
    if st.session_state.messages:
        for msg in st.session_state.messages:
            st.markdown(msg)

    # Task input
    task = st.chat_input("Enter your task")

    # Run the analysis for the uploaded dataset
    if task:
        if not uploaded_file:
            st.error("Please upload a CSV file first.")
        else:
            # Create temp directory if it doesn't exist
            if not os.path.exists("temp"):
                os.makedirs("temp")

            # Save uploaded file
            with open("temp/data.csv", "wb") as f:
                f.write(uploaded_file.getbuffer())

            # Get clients
            openai_model_client = get_model_client()
            docker = get_docker_code_executor()

            # Run analysis
            if task and task.strip():  # Check if task is not empty
                try:
                    # Create a TextMessage from the task
                    from autogen_agentchat.messages import TextMessage

                    task_message = TextMessage(content=task.strip(), source="user")

                    # Show progress message
                    with st.spinner("Running analysis..."):
                        error = asyncio.run(
                            run_gpt_analyzer(docker, openai_model_client, task_message)
                        )
                        if error:
                            st.error(f"An error has occurred: {error}")
                        else:
                            st.success("Analysis completed successfully!")
                except Exception as e:
                    st.error(f"Failed to run analysis: {str(e)}")
                    import traceback

                    st.error(f"Traceback: {traceback.format_exc()}")
            elif task:
                st.warning("Please enter a valid task description.")

            # Display output image if it exists
            if os.path.exists("temp/output.png"):
                st.image("temp/output.png", caption="Analysis Result")


if __name__ == "__main__":
    main()
