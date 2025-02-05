import unittest
from unittest.mock import MagicMock, patch
from infrastructure.openai.client import OpenAIClient


class TestOpenAIClient(unittest.TestCase):
    @patch('infrastructure.openai.client.OpenAI')
    def test_get_models_and_chat(self, mock_openai_class: any) -> None:
        # Setup dummy responses
        dummy_model_list = {"data": ["model1", "model2"]}
        dummy_chat_response = MagicMock()
        dummy_chat_response.choices = [MagicMock(message=MagicMock(content="dummy chat response"))]

        # Create a dummy instance of OpenAI
        dummy_instance = MagicMock()
        dummy_instance.models.list.return_value = dummy_model_list
        dummy_instance.chat.completions.create.return_value = dummy_chat_response
        mock_openai_class.return_value = dummy_instance

        client = OpenAIClient(api_key="dummy_key")
        models = client.get_models()
        self.assertEqual(models, dummy_model_list)

        response = client.chat("dummy-model", "Hello")
        self.assertEqual(response, "dummy chat response")


if __name__ == '__main__':
    unittest.main()
