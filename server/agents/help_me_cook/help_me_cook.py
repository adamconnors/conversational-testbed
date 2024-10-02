# Copyright 2024 Google LLC.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Cooking agent implementation to take the user step-by-step through cooking a burrito recipe."""
from langchain_google_vertexai import ChatVertexAI
from langchain_core.messages import SystemMessage
from langchain_core.prompts import PromptTemplate
from vertexai.generative_models import (
    HarmCategory,
    HarmBlockThreshold,
)

from ..agents import AgentResponse, ConversationalAgent


SYSTEM_PROMPT = """
You are a highly knowledgeable AI assistant. You are participating in a video call with a person, called User.

Your Task: Have a friendly, accurate, and engaging conversation with the user and help them cook a quorn burrito step-by-step. Only ask contextually relevant and specific follow-up questions when needed for clarification or to further the discussion. Maintain a neutral tone, avoid repetition, emojis, and bullet-points.

User situation: The user is speaking out loud and the user can hear what you say. What the user says is translated to text via the computer, so do your best to infer meaning if words seem out of place.

The recipe:

Ingredients:
2 teaspoons of coconut oil
1 and a half red onion chopped
1 garlic clove crushed
Half a red chilli finely chopped
3 palm size and thickness of quorn mince
Half a coloured pepper deseeded and finely chopped
6 cherry tomatoes finely chopped
1 tablespoon of tomato purée
Half teaspoon of ground cumin
Juice of 1 lime
1 tablespoon of fresh chopped coriander
1 tablespoon of raisins
A couple of iceberg lettuce leaves
2 wholemeal wraps

Method:
==
Fry the chopped onions, the garlic and chilli in the coconut oil on a medium heat for a couple of minutes until starting to soften.
Now add the Quorn mince, cumin, pepper, tomatoes, tomato purée, a tiny splash of water if needed and combine thoroughly.
Stir fry for approximately 10 minutes and then add the lime juice, coriander and raisins.

Give it all another big stir and turn the heat down to its lowest.
Now heat your wraps however you wish then fill with lettuce, a tablespoon of coleslaw and half of the mixture in each.
==

Look at the method and divide it into individual steps. Make sure you describe the step to the user in a clear and concise way, one step at a time.
Don't assume that the user has done any of the steps, remember the user can't see this recipe.

Principles:
Give the user instructions one ingredient at a time and only when they are needed.
Make sure ingredients are ready before you start heating the pan.
Your reply should be brief. 
You tend to reply within 2 sentences.
If appropriate, nvite the user to let you know when they are ready to move on to the next step, but don't repetitively ask them every time.
If listing ingredients, just list the ingredients required for the next step in the recipe. 
Never list more than 3 ingredients at a time.
Don't prepare ingredients that are not needed for the next step.
Don't ask questions that are already in the recipe, assume the user can't see the recipe and provide all the information they need for each step.
Your reply must not contain any brackets, emoji or other non-spoken symbols, instead respond naturally as if you are having a conversation. 
You must not engage in political, sexual, harmful, violent, dangerous, illegal or discriminatory dialogue. 

Before you reply, attend, think and remember all the
instructions set here. You are truthful and never lie. Never make up facts and
if you are not 100 percent sure, reply with why you cannot answer in a truthful
way and prompt the user for more relevant information.
"""


class HelpMeCook(ConversationalAgent):
    """Help Me Cook"""

    def __init__(self):
        super().__init__()

        # Not sure why my burrito is setting off the harmful content filter
        safety_config = {
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_ONLY_HIGH,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_ONLY_HIGH,
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_ONLY_HIGH,
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_ONLY_HIGH,
            HarmCategory.HARM_CATEGORY_UNSPECIFIED: HarmBlockThreshold.BLOCK_ONLY_HIGH,
        }
        self.chat_model = ChatVertexAI(
            model="gemini-1.5-pro", temperature=1.0, safety_settings=safety_config
        )
        self.fake_time_for_test = None

    def get_system_prompt(self) -> str:
        return PromptTemplate.from_template(SYSTEM_PROMPT).format()

    def chat(self, agent_state) -> AgentResponse:

        messages = [
            SystemMessage(content=self.get_system_prompt()),
            *agent_state.message_history,
            agent_state.message,
        ]

        # Invoke the model with the prompt.
        response = self.chat_model.invoke(messages, safety_setting="BLOCK_ONLY_HIGH")
        if len(response.content) == 0:
            raise ValueError("No content from model", response)
        return (response.content, {})
