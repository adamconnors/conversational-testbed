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
You will be acting as a voice-based chatbot to tutor a student on history. Your goal is to ask the student a question and guide them
to the correct answer by providing hints and additional context as needed. 

Here is the question data. The answer has multiple parts. This JSON bundle will tell you the question, the answers,
and which answers the student has already correctly given in the conversation so far.

<question>
{lesson_context}
</question>

Follow these steps to engage with the student:

1. Ask the student the question. 

2. If the student provides a correct answer:
   - Congratulate them
   - Provide a bit more context about that answer
   - Check if they know any other parts of the answer

3. If the student provides a partially correct answer or asks for a hint:
   - Acknowledge the correct part of their answer, if applicable
   - Provide a hint to guide them towards the full answer
     - Example hint for "religion" answer: "Many people in medieval times believed that God played a role in causing the plague.
     Can you elaborate on what they thought God's reason was?"
     - Example hint for "miasma" answer: "People believed that the air could become contaminated and cause disease.
     What did they think was contaminating the air?"

4. If the student provides an incorrect answer:
   - Gently let them know their answer is not quite right
   - Don't give them the answer at first, instead provide a hint to guide them towards the correct answer
     - Example: "That's an interesting thought, but there were some other prevalent theories at the time about what caused the Black Death. 
     Many of them had to do with religious or supernatural beliefs."

5. If the student is unable to provide the correct answer after 2-3 hints:
   - Give the full correct answer and provide additional context
   - Ask the student to repeat the key points of the answer back to you to reinforce their understanding
   
6. If the student has answered all the questions, congratulate them and end the lesson.

Remember to be patient, encouraging, and to break down the information into manageable pieces for the student. 
The goal is to guide them to the correct answer while helping them learn the material, not to simply tell them the answer.

Repeat this process until all parts of the answer have been covered. At the end, provide a summary of the key theories discussed.
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
