import time
import unittest

from langchain_google_vertexai import VertexAI
from default_agent import DefaultAgent
import test_utils
from agents import AgentState, AgentResponse
from langchain.evaluation import load_evaluator, EvaluatorType


class DefaultAgentTest(unittest.TestCase):

    def setUp(self):
        self.llm = VertexAI(model_name="gemini-pro")

    def test_chat(self):
        agent = DefaultAgent()

        message_history = test_utils.build_message_history_for_test(
            ["Hello", "Hello yourself"]
        )
        message = "Tell me what time it is in the style of a pirate, but make sure you're accurate to the minute."
        response, world_state = agent.chat(
            AgentState(
                message,
                message_history,
                None,
            )
        )

        # The criteria is lenient to avoid false negatives.
        criteria = {
            "time": "Does the output attempt to convey roughly the  time and is the time correct to within an hour?",
        }

        eval = load_evaluator(
            EvaluatorType.LABELED_CRITERIA, llm=self.llm, criteria=criteria
        )
        result = eval.evaluate_strings(
            input=message,
            prediction=response,
            criteria=criteria,
            reference=f"The Current time is {time.strftime('%I:%M %p')}",
        )

        score = result["score"]
        self.assertTrue(
            score == 1.0,
            f"Response: {response} failed. \nReason: {result['reasoning']}",
        )

    def test_short_responses(self):
        agent = DefaultAgent()

        message_history = []
        message = "Explain relativity to me."
        response, world_state = agent.chat(
            AgentState(
                message,
                message_history,
                None,
            )
        )
        print(response)
        self.assertLess(len(response), 300)
