from config.openai_model_client import get_model_client
from agents.code_executor_agent import GetCodeExecutorAgent
from agents.Data_analyzer_agent import get_data_analyzer_agent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination

# termination condition
text_termination_condition = TextMentionTermination("STOP")


# function to get a analyzer gpt team
def Analyzer_GPT_Team(docker, model_client):
    """
    Get a analyzer gpt team.
    """
    code_executor_agent = GetCodeExecutorAgent(docker)
    data_analyzer_agent = get_data_analyzer_agent(model_client)

    # Defining a RoundRobinGroupChat team.
    team = RoundRobinGroupChat(
        participants=[data_analyzer_agent, code_executor_agent],
        max_turns=10,
        termination_condition=text_termination_condition,
    )

    return team
