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

import unittest
from ..agents import AgentState, AgentResponse
from .physics_expert import PhysicsExpert, load_resources
from ...utils.test_utils import build_message_history_for_test
from langchain_google_vertexai import VertexAI
from langsmith import unit, traceable


class PhysicsExpertTest(unittest.TestCase):

    def setUp(self):
        self.llm = VertexAI(model_name="gemini-pro")

    @traceable
    @unit
    def test_chat(self):
        agent = PhysicsExpert()
        message_history = build_message_history_for_test([])
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
