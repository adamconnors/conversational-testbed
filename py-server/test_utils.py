from typing import List
from agents import MessageHistory
from langchain_core.messages import AIMessage, HumanMessage

def build_message_history_for_test(messages: List[str]) -> MessageHistory:
    """
    Builds a message history in the same form as agents expect.
    This is a list of BaseMessage objects, starting with the first
    message from the user and alternating between user and agent.
    """
    rtn = []
    for i, message in enumerate(messages):
        if i % 2 == 0:
            rtn.append(HumanMessage(message))
        else:
            rtn.append(AIMessage(message))
    return rtn
