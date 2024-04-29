import json
from typing import Iterator
import unittest
from langchain_core.messages import AIMessage, HumanMessage
from history_tutor.history_tutor import HistoryTutor
from agents import AgentState
from langchain_google_vertexai import VertexAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain.evaluation import load_evaluator, EvaluatorType
import concurrent.futures
import test_utils


class TestHistoryTutor(unittest.TestCase):

    def setUp(self):
        self.llm = VertexAI(model_name="gemini-pro")

    def test_loads_initial_world_state(self):
        tutor = HistoryTutor()
        lesson = tutor.lesson_context
        self.assertEqual(len(lesson), 4)

    def test_introduce_lesson_and_ask_first_question(self):
        tutor = HistoryTutor()
        last_message = "start lesson"
        message_history = []

        criteria = {
            "introduction": "Does the output provide a one sentence introduction to the topic and ask the first question?",
        }

        eval = load_evaluator(
            EvaluatorType.LABELED_CRITERIA, llm=self.llm, criteria=criteria
        )


        def evaluate():
            response, world_state = tutor.chat(
                AgentState(last_message, [], None)
            )
            
            result = eval.evaluate_strings(
                input=last_message,
                prediction=response,
                criteria=criteria,
                reference=f"""
                Let's begin our lesson on the Black Death, a devastating pandemic that swept through Europe in the 14th century. 
                What were the different theories about the cause of the Black Death?
            """,
            )
            
            return result

        results = test_utils.run_in_parallel(evaluate, 10)
        for result in results:
            print(result.result())
#        test_utils.tabulate_evaluator_results(responses, results)

if __name__ == "__main__":
    unittest.main()
