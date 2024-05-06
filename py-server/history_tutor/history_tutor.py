import json
import sys
from typing import List
from langchain_google_vertexai import ChatVertexAI, VertexAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field

# set parent directory path
sys.path.append("../py-server")
from agents import AgentResponse, ConversationalAgent
import os


CONVERSATION_PROMPT = """
    You are an expert AUDIO chatbot designed to provide a history quiz to GCSE students.
    
    The topic you're teaching is the Black Death.
    
    This is the first question, and the answer has multiple parts. This JSON bundle is the lesson context and it will
    tell you the question, the answers, and which answers the student has already correctly given in the conversation so far.:

    {lesson_context}
    
    Consider each of these possibilities and give the most appropriate response:

    1. Is this the start of the lesson? --> Provide a one sentence introduction to the topic and then ask the first question.
    2. Has the student correctly given one or more of the answers to the current question? 
    --> Congratulate them. Add more details based on their last answer.
    3. Are there still unanswered parts to the question? --> Ask the student to give more answers to the current question.
    4. Did the student get the answer wrong? --> Explain to them why this answer is wrong and ask them to try again.
    5. Has the student said they don't know or asked for a hint? --> Give them a clue but don't give
    them the actual answer. Ask them if they know the answer now.
    6. If the student doesn't get the answer after you've given them a hint --> give them the answer and ask the next question.
    7. If you gave the student an answer earlier --> ask if they remember the answer you gave them earlier. 
    8 Has the student given ALL the answers to the question? --> Say well done, the lesson is complete. DON'T ask any questions
    that aren't in the lesson context.
        
    ALWAYS RESPOND by asking the student another question unless the lesson is complete.
            
    Always be warm and encouraging. Before you reply, attend, think and remember all the
    instructions set here. You are truthful and never lie. Never make up facts and
    if you are not 100 percent sure, reply with why you cannot answer in a truthful
    way and prompt the user for more relevant information.
"""

UPDATE_STATE_PROMPT = """
    You are a history tutor and you must mark a history test.

    This is the marking sheet with the question, the list of the correct answers, and example responses and how they should be marked:

    MARKING SHEET:
    ```
    {answers}
    
    examples {{
        [
        {{
            "response": "There was a lot of superstition and people thought that god might be angry",
            "marks": ["religion"]
        }},
        {{
            "response": "People thought the water was poisoned",
            "marks": ["none"]
        }},
        {{
            "response": "begin",
            "marks": ["none"],
        }},
        {{
            "response": "There was a hypothesis that strangers were spreading the disease and that people had an imbalance of the humours",
            "marks": ["strangers", "humours"]
        }},
        {{
            "response": "Smells from decaying rubbish caused miasma",
            "marks": ["miasma"]
        }},
        {{
            "response": "Start again",
            "marks": ["restart"]
        }}
        ]
    ```

    This is the student's response to the question:

    STUDENTS RESPONSE:
    ===
    {last_message}
    ===

    Your task: carefully review the student's response and determine if the student's response give any of the answers on the marking sheet.

    Return the keys from the marking sheet for the answers that the STUDENT correctly gave.
    If the student's response didn't contain any correct answers then return the key "none".

    {format_instructions}
"""


BLACK_DEATH_TUTOR_CONTEXT = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "the_black_death.json"
)


def load_file(filename):
    with open(filename, "r") as file:
        return file.read()


class HistoryTutor(ConversationalAgent):
    def __init__(self):
        self.chat_model = ChatVertexAI(
            model="gemini-pro", convert_system_message_to_human=False
        )
        self.model = VertexAI(model_name="gemini-pro", temperature=0)
        self._lesson_context = json.loads(load_file(BLACK_DEATH_TUTOR_CONTEXT))

    def chat(self, agent_state) -> AgentResponse:
        prompt = self._from_messages(CONVERSATION_PROMPT, agent_state)
        chain = prompt | self.model

        # Set world state on first request.
        if agent_state.world_state == None:
            agent_state.world_state = self._lesson_context
        else:
            # Update the question state based on the last answer.
            agent_state.world_state = self.update_question_state(
                agent_state.world_state, agent_state.message
            )

        # Get the response.
        prompt2 = prompt.invoke({"lesson_context": agent_state.world_state})
        response = self.chat_model.invoke(prompt2)
        return (response.content, agent_state.world_state)

    def update_question_state(self, world_state, last_answer):

        parser = JsonOutputParser(pydantic_object=QuestionAnswerList)

        prompt = PromptTemplate(
            template=UPDATE_STATE_PROMPT,
            input_variables=["answers", "last_message"],
            partial_variables={"format_instructions": parser.get_format_instructions()},
        )

        chain = prompt | self.model | parser

        try:
            response = chain.invoke(
                {
                    "answers": world_state,
                    "last_message": last_answer,
                }
            )
            answered_questions = response["correct_responses"]
        except Exception as e:
            answered_questions = []

        # Update the world state based on the list of answers given.            
        for answer in world_state["answers"]:
            if answer["key"] in answered_questions:
                answer["hasAnswered"] = "true"
            if "restart" in answered_questions:
                answer["hasAnswered"] = "false"
                
        return world_state


# Data structure for the output of the update_question_state function
class QuestionAnswerList(BaseModel):
    correct_responses: List[str] = Field(
        description="""Keys for the correct answers in the student's response or the key \"none\"
        if the response didn't contain any correct answers or the key \"restart\" if the student wants to start again."""
    )
