import time
from langchain_google_vertexai import ChatVertexAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_core.output_parsers import JsonOutputParser
import json
from langchain_core.messages import AIMessage, SystemMessage, HumanMessage
from langchain_google_vertexai import VertexAI

PROMPT = """
    You are an expert AUDIO chatbot designed to teach GCSE History.
    
    This is the history lesson plan.:
    ```
    {lesson_context}
    ```
    
    The JSON below represents all the questions the student needs to answer and whether or not they have answered:
    ```
    {world_state}
    ```
    
    Start by introducing the topic and giving a short summary of the main areas you'll be asking
    questions about.
    
    Then pick the next unanswered question from the list and ask it.
    
    If they have answer correctly and completely, immediately ask the next unanswered question.
    
    If they don't know the answer to the question or give an incorrect answer, provide a hint.
    
    If they don't get it after two hints, give them the answer.
    
    If there are multiple answers to a question, stay on that topic until it has been answered completely.
    
    If they ask a question about the topic, answer it, even if it is not in the provided information.
    
    If they give an incomplete answer, prompt them for more details.   
    
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
            {{answer: "Religion: God sent the plague as a punishment for people's sins.", has_answered="false"}},
            {{answer: "Miasma: 'bad air' or smells caused by decaying rubbish.", has_answered="false}},
            {{answer: "Four Humours: most physicians believed that disease was caused by an imbalance in the Four Humours.", has_answered="false}},
            {{answer: "Outsiders: strangers or witches had caused the disease.", has_answered="false"}}
            ]
        }}
        ...
    ] 
"""

UPDATE_WORLD_STATE_PROMPT = """
You are a history tutor testing a student. The JSON below represents all the
questions they need to answer and whether or not that have answered.

```
{world_state}
```

Based on the previous chat history with the student, update the world state to reflect
any questions they have answered.

Chat history: {chat_history}

    Return results as an array of JSON objects.   
    For Example:
    [
        {{
            "question": "What were the different theories about the cause of the Black Death?",
            "answers": [
            {{answer: "Religion: God sent the plague as a punishment for people's sins.", has_answered="false"}},
            {{answer: "Miasma: 'bad air' or smells caused by decaying rubbish.", has_answered="false}},
            {{answer: "Four Humours: most physicians believed that disease was caused by an imbalance in the Four Humours.", has_answered="false}},
            {{answer: "Outsiders: strangers or witches had caused the disease.", has_answered="false"}}
            ]
        }}
        ...
    ] 
"""

BLACK_DEATH_TUTOR_CONTEXT = "./history_tutor/the_black_death.md"


class HistoryTutor:
    def __init__(self):
        start = time.time()
        self.gemini = VertexAI(model_name="gemini-pro")
        self.chat_model = ChatVertexAI(
            model="gemini-pro", convert_system_message_to_human=True
        )
        end = time.time()
        print(f"HistoryTutor loaded in {end - start:0.2f} seconds")

        self.lesson_context = self.load_file(BLACK_DEATH_TUTOR_CONTEXT)

    def chat(self, message_history, world_state, message):

        updated_world_state = self.update_world_state(world_state, message_history)

        system_prompt = PromptTemplate.from_template(PROMPT).format(
            lesson_context=self.lesson_context,
            world_state=json.dumps(updated_world_state),
        )
        messages = [SystemMessage(system_prompt)]
        messages.extend(message_history)
        messages.append(HumanMessage(message))
        response = self.chat_model.invoke(messages)
        return response.content, updated_world_state

    def build_world_state(self):
        world_state = {}
        prompt = PromptTemplate.from_template(INITIAL_WORLD_STATE_PROMPT).format(
            lesson_context=self.lesson_context
        )
        response = self.gemini.invoke(prompt)
        parser = JsonOutputParser()
        json = parser.parse(response)
        return json

    def update_world_state(self, world_state, chat_history):
        prompt = PromptTemplate.from_template(UPDATE_WORLD_STATE_PROMPT).format(
            world_state=json.dumps(world_state), chat_history=chat_history
        )

        try:
            response = self.gemini.invoke(prompt)
            parser = JsonOutputParser()
            output = parser.parse(response)
        except Exception as e:
            print("Couldn't parse world_state", e)
            return ["failed"]

        return output

    def load_file(self, filename):
        with open(filename, "r") as file:
            return file.read()
