import unittest
import model_aligner_helper as helper
from model_alignment import model_helper, single_run


# TODO: Add real tests here.
class TestModelAlignerHelper(unittest.TestCase):
    def testVertexHelper(self):
        vertex = helper.VertexModelHelper()
        result = vertex.predict("Tell me a joke", 0.5, candidate_count=1)
        print(result)

    def testGeneratesPrinciple(self):
        single_run_prompt = single_run.AlignableSingleRun(helper.VertexModelHelper())
        initial_prompt = "Tell me a joke about {topic}."
        single_run_prompt.set_model_description(initial_prompt)
        output = single_run_prompt.send_input({"topic": "fish"})
        single_run_prompt.set_input_output_pair(output)
        principles = single_run_prompt.critique_response("Not funny enough.")
        print(f"Principles {principles}")
        single_run_prompt.update_model_description_from_principles()

        model_description = single_run_prompt.get_model_description_with_principles()
        print(f"Updated model description {model_description}")
