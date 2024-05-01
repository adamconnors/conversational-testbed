from typing import List
from agents import AgentState, MessageHistory
from langchain_core.messages import AIMessage, HumanMessage
import tabulate
import concurrent.futures
from langchain.evaluation import load_evaluator, EvaluatorType


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


def evaluate(response, llm, last_message, criteria, reference):
    """
    Evaluates the response against the reference using the given criteria.
    """
    eval = load_evaluator(
        EvaluatorType.LABELED_CRITERIA,
        llm=llm,
        criteria={ "correctness": criteria }
    )
    result = eval.evaluate_strings(
        input=last_message,
        prediction=response,
        reference=reference
    )
    return result

