import json
import time
import sys
from langchain_google_vertexai import ChatVertexAI, VertexAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser

# set parent directory path
sys.path.append("../py-server")
from agents import ConversationalAgent
import os


CONVERSATION_PROMPT = """
    You are an expert AUDIO chatbot designed to teach GCSE History.
    
    This is the history lesson plan.:
    ```
    {lesson_context}
    ```
    
    The JSON below represents all the questions to ask. Each question has multiple parts to the answer.
    The hasAnswered flag indicates whether the student has already answered this question or not.
    
    ```
    {world_state}
    ```
    
    This is the chat history so far:
    {chat_history}
    
    This is the last message sent by the student:
    {last_message}

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

INITIAL_WORLD_STATE_PROMPT = """
    You are a history tutor. Based on this lesson plan, identify the main areas you'll be asking
    questions about and organize them into a list. Include an attribute has_answered which is always false.
    
    Some questions have multiple parts to the answer, list all answers.
    
    This is the lesson plan:
    ```
    {lesson_context}
    ```
    
    Return results as an array of JSON objects.   
    [
        {{
            "question": "What were the different theories about the cause of the Black Death?",
            "answers": [
            {{"answer": "Religion: God sent the plague as a punishment for people's sins.", "hasAnswered": "false"}},
            {{"answer": "Miasma: bad air or smells caused by decaying rubbish.", "hasAnswered": "false"}},
            {{"answer": "Four Humours: most physicians believed that disease was caused by an imbalance in the Four Humours.", "hasAnswered": "false"}},
            {{"answer": "Outsiders: strangers or witches had caused the disease.", "hasAnswered": "false"}}
            ]
        }}
    ]
"""

UPDATE_WORLD_STATE_PROMPT = """
You are a history tutor testing a student. The JSON below represents all the
questions they need to answer and whether or not that have answered.

```
{world_state}
```

Based on the previous chat history with the student and their last message, update the world state to reflect
any questions they have answered.

Chat history: {chat_history}
Last message: {last_message}

Return results as an array of JSON objects. Return ALL answers in the original world state.  
"""

BLACK_DEATH_TUTOR_CONTEXT = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "the_black_death.md"
)


def load_file(filename):
    with open(filename, "r") as file:
        return file.read()


class HistoryTutor(ConversationalAgent):
    def __init__(self):
        start = time.time()
        self.gemini = VertexAI(model_name="gemini-pro")
        self.chat_model = ChatVertexAI(
            model="gemini-pro", convert_system_message_to_human=True
        )
        end = time.time()
        print(f"HistoryTutor loaded in {end - start:0.2f} seconds")

        self.lesson_context = load_file(BLACK_DEATH_TUTOR_CONTEXT)

    def chat(self, message: str):
        response = self.chat_model.invoke(self._state.message_history)
        return response.content

    def _build_system_prompt(self, state):
        return PromptTemplate.from_template(CONVERSATION_PROMPT).format(
            lesson_context=self.lesson_context,
            last_message=state.message,
            chat_history=state.message_history,
            world_state=json.dumps(state.world_state),
        )

    def _init_world_state(self):
        prompt = PromptTemplate.from_template(INITIAL_WORLD_STATE_PROMPT).format(
            lesson_context=self.lesson_context
        )
        response = self.gemini.invoke(prompt)
        return JsonOutputParser().parse(response)

    def _build_world_state(self, state):
        world_state = None
        if not state.world_state:
            print("No world state received, creating new one")
            world_state = self._init_world_state()
            print("World state created", world_state)
            return world_state

        prompt = PromptTemplate.from_template(UPDATE_WORLD_STATE_PROMPT).format(
            world_state=json.dumps(state.world_state),
            chat_history=state.message_history,
            last_message=state.message,
        )
        try:
            response = self.gemini.invoke(prompt)
            return JsonOutputParser().parse(response)
        except Exception as e:
            print("Couldn't parse world_state", e)
            return {"failed": True}
