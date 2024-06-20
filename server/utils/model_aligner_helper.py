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
