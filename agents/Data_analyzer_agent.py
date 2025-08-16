from autogen_agentchat.agents import AssistantAgent

from .DataAnalyzerPrompt import DATA_ANALYZER_PROMPT


# function to get a data analyzer agent
def get_data_analyzer_agent(
    model_client,
) -> AssistantAgent:
    """
    Get a data analyzer agent.

    Args:
        model_client: ModelClient
    Returns:
        AssistantAgent
    """
    # create a data analyzer agent
    data_analyzer_agent = AssistantAgent(
        name="Data_Analyzer_Agent",
        description="",
        model_client=model_client,
        system_message=DATA_ANALYZER_PROMPT,
    )
    return data_analyzer_agent
