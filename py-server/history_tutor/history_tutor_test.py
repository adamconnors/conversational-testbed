import unittest
from history_tutor import HistoryTutor
from main import build_message_history


class TestHistoryTutor(unittest.TestCase):
    def setUp(self):
        self.tutor = HistoryTutor()

    def test_conversation_no_history(self):
        resp = self.tutor.chat(None, """Tell me a joke""")


if __name__ == "__main__":
    unittest.main()
