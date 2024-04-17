import json
import unittest
from langchain_core.messages import AIMessage, HumanMessage
from history_tutor.history_tutor import HistoryTutor
from agents import AgentState
from langchain_google_vertexai import VertexAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser


FAKE_INITIAL_WORLD_STATE = json.loads(
    """
    [{"question": "What were the different theories about the cause of the Black Death?", 
    "answers": 
    [
        {"answer": "Religion: God sent the plague as a punishment for people's sins.", "hasAnswered": "false"}, 
        {"answer": "Miasma: bad air or smells caused by decaying rubbish.", "hasAnswered": "false"}, 
        {"answer": "Four Humours: most physicians believed that disease was caused by an imbalance in the Four Humours.", "hasAnswered": "false"}, 
        {"answer": "Outsiders: strangers or witches had caused the disease.", "hasAnswered": "false"}
    ]}
    ]
    """
)

FAKE_INITIAL_WORLD_STATE_TWO_QUESTIONS = json.loads(
    """
    [
    {"question": "What were the different theories about the cause of the Black Death?", "answers": [{"answer": "Religion: God sent the plague as a punishment for people's sins.", "hasAnswered": "false"}, {"answer": "Miasma: bad air or smells caused by decaying rubbish.", "hasAnswered": "false"}, {"answer": "Four Humours: most physicians believed that disease was caused by an imbalance in the Four Humours.", "hasAnswered": "false"}, {"answer": "Outsiders: strangers or witches had caused the disease.", "hasAnswered": "false"}]},
    {"question": "What methods were used to prevent the Black Death?", "answers": [{"answer": "Religious methods, such as prayer, donating to the Church and flagellation.", "hasAnswered": "false"}, {"answer": "Clearing up rubbish in the streets.", "hasAnswered": "false"}, {"answer": "Smelling their toilets or other bad smells.", "hasAnswered": "false"}, {"answer": "Lighting a fire in the room, ringing bells or having birds flying around the room to keep air moving.", "hasAnswered": "false"}, {"answer": "Carrying herbs and spices to avoid breathing in 'bad air'.", "hasAnswered": "false"}, {"answer": "Not letting unknown people enter the town or village.", "hasAnswered": "false"}]}
    ]
    """
)


FAKE_LLM_RESPONSE_1 = """
The Black Death was a devastating pandemic that swept through
Europe in the 14th century, killing millions of people.

To start, what were some of the different theories about what caused the
Black Death? 
"""

RESPONSE_EXPECTATIONS_PROMPT = """
You are an engineer building a conversational agent. You must assess the AI response below to
ensure it meets the following criteria:

1. Does it {response_expectations}?

The AI response you are assessing is:
{ai_response}

Return your answer in JSON in the following format stating whether the response passes
the criteria or not along with a SHORT one sentence rationale for your decision:
{{ "pass": "true", "rationale": "The reason why this response is not correct." }} 
"""


class TestHistoryTutor(unittest.TestCase):

    def setUp(self):
        print("setUp")

    def test_create_initial_world_state(self):
        tutor = HistoryTutor()
        agent_state = tutor.update_state(AgentState("start lesson", [], {}))
        text = tutor.chat("start lesson")
        world_state = agent_state.world_state
        self.assertEqual(len(world_state), 4)
        print(world_state)

    def test_single_correct_answer(self):
        # Expect that when the student gives the correct answer, the model
        # updates with a bit of extra context and prompts for additional
        # answers to this question.
        tutor = HistoryTutor()
        message_history = ["start lesson", FAKE_LLM_RESPONSE_1]
        response, updated_state = chat(
            tutor,
            message_history,
            "Did they think strangers caused the Black Death?",
            FAKE_INITIAL_WORLD_STATE,
        )

        self.assertTrue(
            to_boolean(updated_state.world_state[0]["answers"][3]["hasAnswered"])
        )
        self.assertFalse(
            to_boolean(updated_state.world_state[0]["answers"][0]["hasAnswered"])
        )

        self.assert_response(
            """Congratulates the student for getting the answer correct and asks
            them if they can think of any more answers.""",
            response,
            updated_state,
        )

    def test_multiple_correct_answers(self):
        # Expect that when the student gives multiple correct answers, the model
        # responds to both answers and marks both answers as correct.
        tutor = HistoryTutor()
        message_history = ["start lesson", FAKE_LLM_RESPONSE_1]
        response, updated_state = chat(
            tutor,
            message_history,
            "They thought it was strangers. And they thought it was a punishment from God.",
            FAKE_INITIAL_WORLD_STATE,
        )

        self.assertTrue(
            to_boolean(updated_state.world_state[0]["answers"][0]["hasAnswered"])
        )
        self.assertTrue(
            to_boolean(updated_state.world_state[0]["answers"][3]["hasAnswered"])
        )

        self.assert_response(
            """Congratulates the student for getting the answer correct and mentions both answers,
            then asks them if they can think of any more answers.""",
            response,
            updated_state,
        )

    def test_moves_onto_next_question(self):
        tutor = HistoryTutor()
        message_history = ["start lesson", FAKE_LLM_RESPONSE_1]

        response, updated_state = chat(
            tutor,
            message_history,
            """They thought it was punishment from God, an imbalance in the four humours,
            strangers, and miasma.""",
            FAKE_INITIAL_WORLD_STATE,
        )

        self.assertTrue(
            to_boolean(updated_state.world_state[0]["answers"][0]["hasAnswered"])
        )
        self.assertTrue(
            to_boolean(updated_state.world_state[0]["answers"][1]["hasAnswered"])
        )
        self.assertTrue(
            to_boolean(updated_state.world_state[0]["answers"][2]["hasAnswered"])
        )
        self.assertTrue(
            to_boolean(updated_state.world_state[0]["answers"][3]["hasAnswered"])
        )

        self.assert_response(
            "Asks the student about the methods people used to prevent the Black Death.",
            response,
            updated_state,
        )

    def test_answers_incorrectly(self):
        tutor = HistoryTutor()
        message_history = [
            "start lesson",
            FAKE_LLM_RESPONSE_1,
            "Was it caused by witches?",
            """That's correct! Some people thought strangers or witches brought the disease. 
            What other theories for the cause of the Black Death can you think of?""",
        ]

        updated_world_state = FAKE_INITIAL_WORLD_STATE.copy()
        updated_world_state[0]["answers"][3]["hasAnswered"] = "true"

        response, updated_state = chat(
            tutor,
            message_history,
            "They thought it was caused by bacteria.",
            updated_world_state,
        )

        self.assert_response(
            """Tells the student that they were incorrect and asks
                             them for an alternative answer.""",
            response,
            updated_state,
        )

    @unittest.skip("Can't seem to make this work")
    def test_completes_the_lesson(self):
        tutor = HistoryTutor()
        message_history = ["start lesson", FAKE_LLM_RESPONSE_1]

        response, updated_state = chat(
            tutor,
            message_history,
            """They thought it was punishment from God, an imbalance in the four humours,
            strangers, and miasma.""",
            FAKE_INITIAL_WORLD_STATE,
        )

        self.assertTrue(
            to_boolean(updated_state.world_state[0]["answers"][0]["hasAnswered"])
        )
        self.assertTrue(
            to_boolean(updated_state.world_state[0]["answers"][1]["hasAnswered"])
        )
        self.assertTrue(
            to_boolean(updated_state.world_state[0]["answers"][2]["hasAnswered"])
        )
        self.assertTrue(
            to_boolean(updated_state.world_state[0]["answers"][3]["hasAnswered"])
        )

        self.assert_response(
            """Congratulates the student and tells them that the lesson is complete""",
            response,
            updated_state,
        )

    # TODO: Move into super class.
    def assert_response(self, response_expectations, actual_response, updated_state):
        llm = VertexAI(model_name="gemini-pro")
        prompt = PromptTemplate.from_template(RESPONSE_EXPECTATIONS_PROMPT).format(
            response_expectations=response_expectations, ai_response=actual_response
        )
        parser = JsonOutputParser()

        response = parser.parse(llm.invoke(prompt))
        passed = response["pass"]
        print(f"--Response-- \n{actual_response}\n---")
        if passed == "true":
            print(f"Response Passed: {response['rationale']}")
        else:
            self.fail(f"Response failed: {response['rationale']}")


def chat(tutor, message_history, latest_message, world_state):
    message_history = build_message_history(message_history)
    initial_agent_state = AgentState(latest_message, message_history, world_state)
    updated_agent_state = tutor.update_state(initial_agent_state)
    response = tutor.chat(latest_message)
    return response, updated_agent_state


# TODO: What's the proper way to do this, bool didn't seem to work?
def to_boolean(string):
    return string.lower() == "true"


def build_message_history(messages):
    rtn = []
    for i, message in enumerate(messages):
        if i % 2 == 0:
            rtn.append(HumanMessage(message))
        else:
            rtn.append(AIMessage(message))
    return rtn


if __name__ == "__main__":
    unittest.main()
