import json
import time
import sys
from langchain_google_vertexai import ChatVertexAI, VertexAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser

# set parent directory path
sys.path.append("../py-server")
from agents import AgentResponse, ConversationalAgent
import os


CONVERSATION_PROMPT = """
    You are an expert AUDIO chatbot designed to provide a history quiz to GCSE students.
    
    This is the set of questions to ask and whether or not the student has asked them.:
    ```
    {lesson_context}
    ```
    
    Consider each of these possibilities and give the most appropriate response:

    1. If this is the start of the lesson, give a one sentence introduction to the topic and then ask the first question.
    2. If the student answered the question correctly, congratulate them and add one sentence of additional context.
    3. If there are more unanswered answers for the current question, ask the student to provide more answers.
    4. If all the answers are true for a given question, ask the student to answer the next question in the list.
    5. If the student gives an incorrect answer, tell them its incorrect and explain why. Then provide a subtle clue to guide them to the right answer.
    6. If the student says they don't know the answer, give them a clue.
    7. If none of the questions are unanswered say: Well done, this lesson is complete.

    ALWAYS RESPOND by asking the student another question unless the lesson is complete.
            
    Always be warm and encouraging. Before you reply, attend, think and remember all the
    instructions set here. You are truthful and never lie. Never make up facts and
    if you are not 100 percent sure, reply with why you cannot answer in a truthful
    way and prompt the user for more relevant information.
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
            model="gemini-pro", convert_system_message_to_human=True
        )

        self.lesson_context = json.loads(load_file(BLACK_DEATH_TUTOR_CONTEXT))

    def chat(self, agent_state) -> AgentResponse:
        promptTemplate = self._from_messages(CONVERSATION_PROMPT, agent_state)
        
        # Any JSON added to the prompt needs to be escaped.
        escaped_lesson_context = json.dumps(self.lesson_context).replace("{", "{{").replace("}", "}}")     
        prompt = promptTemplate.invoke({"lesson_context": escaped_lesson_context})
        
        response = self.chat_model.invoke(prompt)
        return (response.content, self.lesson_context)