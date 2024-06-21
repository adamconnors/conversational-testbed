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

import vertexai

from model_alignment import model_helper
from vertexai.generative_models import GenerationConfig, GenerativeModel


class VertexModelHelper(model_helper.ModelHelper):
    def __init__(self):
        super().__init__()

    def predict(
        self,
        prompt: str,
        temperature: float,
        stop_sequences: list[str] | None = None,
        candidate_count: int = 1,
        max_output_tokens: int | None = None,
    ) -> list[str] | str:

        model = GenerativeModel("gemini-1.5-flash-001")
        generation_config = GenerationConfig(
            temperature=temperature,
            candidate_count=candidate_count,
            max_output_tokens=max_output_tokens,
        )

        responses = model.generate_content(
            prompt,
            generation_config=generation_config,
        )

        # Gemini only support one candidate
        return responses.candidates[0].text
