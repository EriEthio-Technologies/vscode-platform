# ai-service/tests/unit/test_router.py
import unittest
from ..model_router.router import ModelRouter

class TestModelRouter(unittest.TestCase):
    def test_select_model(self):
        router = ModelRouter(models={
            "deepseek": "deepseek-mock",
            "qwen": "qwen-mock",
            "kimi": "kimi-mock"
        })
        self.assertEqual(router.select_model("python code", "python", 60), "deepseek-mock")
