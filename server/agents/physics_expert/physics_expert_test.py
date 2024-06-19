import time
import unittest
from langchain.globals import set_debug
from langchain_google_vertexai import VertexAI
from agents.physics_expert.physics_expert import PhysicsExpert, load_resources
import utils.test_utils
from agents.agents import AgentState, AgentResponse
from langchain.evaluation import load_evaluator, EvaluatorType
from langsmith import unit, traceable


class PhysicsExpertTest(unittest.TestCase):

    def setUp(self):
        self.llm = VertexAI(model_name="gemini-pro")

    @traceable
    @unit
    def test_chat(self):
        agent = PhysicsExpert()
        message_history = utils.test_utils.build_message_history_for_test([])
        message = "Tell me about the double slit experiment."
        response, world_state = agent.chat(
            AgentState(
                message,
                message_history,
                None,
            )
        )

        word_count = len(response.split())
        self.assertLess(word_count, 100, f"Response was too long: {response}")

    @unittest.skip("Test skipped")
    def test_load_document(self):
        overview, rqm = load_resources()
        print(overview)
