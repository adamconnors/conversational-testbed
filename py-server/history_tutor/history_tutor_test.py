import json
from typing import Iterator, List, Optional
import unittest
from langchain.llms import BaseLLM
from langchain_core.messages import AIMessage, HumanMessage
from history_tutor.history_tutor import (
    HistoryTutor,
    load_file,
    BLACK_DEATH_TUTOR_CONTEXT,
)
from agents import AgentState
from langchain_google_vertexai import VertexAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
import test_utils
from langchain.llms import BaseLLM
from langchain.globals import set_debug


class TestHistoryTutor(unittest.TestCase):

    def setUp(self):
        self.llm = VertexAI(model_name="gemini-pro")
        self.tutor = HistoryTutor()

    def test_loads_initial_world_state(self):
        lesson = self.tutor._lesson_context
        self.assertIsNotNone(lesson["question"])
        self.assertEqual(len(lesson["answers"]), 4)

    def test_introduce_lesson_and_ask_first_question(self):
        last_message = "start lesson"
        response, world_state = self.tutor.chat(AgentState(last_message, [], None))

        # TODO: Evaluate N times to account for randomness of model.
        # TODO: Create an "examples" evaluator that will accept multiple examples.
        result = test_utils.evaluate(
            response,
            self.llm,
            last_message,
            criteria="Does the output provide a short introduction and then ask the first question?",
            reference="""
            Let's begin our lesson on the Black Death. 
            What were the different theories about the cause of the Black Death?
            """,
        )

        self.assertTrue(
            result["value"] == "Y",
            f"Evualation of model response failed. Score was {result['value']}.  Response: {response} failed. \nReason: {result['reasoning']}",
        )

    def test_restart(self):
        world_state = json.loads(load_file(BLACK_DEATH_TUTOR_CONTEXT))
        for answer in world_state["answers"]:
            answer["hasAnswered"] = "true"
        last_message = "start again"
        world_state = self.tutor.update_question_state(world_state, last_message)
        self.assertEqual("false", world_state["answers"][0]["hasAnswered"])
        self.assertEqual("false", world_state["answers"][1]["hasAnswered"])
        self.assertEqual("false", world_state["answers"][2]["hasAnswered"])
        self.assertEqual("false", world_state["answers"][3]["hasAnswered"])

    def test_update_world_state_no_answers(self):
        world_state = json.loads(load_file(BLACK_DEATH_TUTOR_CONTEXT))
        last_answer = "start lesson."
        world_state = self.tutor.update_question_state(world_state, last_answer)
        self.assertEqual("false", world_state["answers"][0]["hasAnswered"])
        self.assertEqual("false", world_state["answers"][1]["hasAnswered"])
        self.assertEqual("false", world_state["answers"][2]["hasAnswered"])
        self.assertEqual("false", world_state["answers"][3]["hasAnswered"])

    def test_update_world_state_two_answers(self):
        world_state = json.loads(load_file(BLACK_DEATH_TUTOR_CONTEXT))
        last_answer = "The four humors and the miasma theory."
        world_state = self.tutor.update_question_state(world_state, last_answer)
        self.assertEqual(world_state["answers"][1]["hasAnswered"], "true")
        self.assertEqual(world_state["answers"][2]["hasAnswered"], "true")

    def test_update_world_state_all_answers(self):
        world_state = json.loads(load_file(BLACK_DEATH_TUTOR_CONTEXT))
        last_answer = "Punishment from God, the four humors theory, miasma theory, and strangers or outsiders."
        world_state = self.tutor.update_question_state(world_state, last_answer)
        self.assertEqual(world_state["answers"][0]["hasAnswered"], "true")
        self.assertEqual(world_state["answers"][1]["hasAnswered"], "true")
        self.assertEqual(world_state["answers"][2]["hasAnswered"], "true")
        self.assertEqual(world_state["answers"][3]["hasAnswered"], "true")

    def test_student_gives_two_answers_correctly(self):
        world_state = json.loads(load_file(BLACK_DEATH_TUTOR_CONTEXT))
        message_history = test_utils.build_message_history_for_test(
            [
                "start lesson",
                "Let's begin our lesson on the Black Death. What were the different theories about the cause of the Black Death?",
            ]
        )
        last_message = "The four humors and the miasma theory."
        response, world_state = self.tutor.chat(
            AgentState(last_message, message_history, world_state)
        )

        # Four humours and miasma have both been marked as true.
        self.assertEqual(world_state["answers"][1]["hasAnswered"], "true", world_state)
        self.assertEqual(world_state["answers"][2]["hasAnswered"], "true", world_state)

        result = test_utils.evaluate(
            response,
            self.llm,
            last_message,
            criteria="""Does the output congratulate the student. Then, does it ask the student to provide more answers to the current question?""",
            reference="""Great! You're correct. The four humors and the miasma theory were two theories about the cause of the Black Death. 
                        Can you think of any others?""",
        )

        self.assertTrue(
            "Y" in result["value"],
            f"\nScore was {result['value']}.  \n\nResponse: {response} failed. \n\nReason: {result['reasoning']}\n\n{result}",
        )


if __name__ == "__main__":
    unittest.main()
