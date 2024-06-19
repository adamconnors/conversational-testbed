import unittest
from chat_client import ChatClient


# TODO: Add real tests here.
class ChatClientTest(unittest.TestCase):
    def testChatClient(self):
        client = ChatClient("physics_expert")
        client.process_input("Tell me about the double-slit experiment.")
        client.handle_command("feedback Talk like a prirate")
        client.handle_command("principles")
