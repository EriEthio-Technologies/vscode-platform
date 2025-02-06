import unittest
from unittest.mock import MagicMock
import asyncio
from ai_service.core.generation import generate_text, CodeGenerator
from ai_service.core.code_context import CodeContext
from ai_service.vector_database import VectorDatabase
from ai_service.models import MockModel

class TestGeneration(unittest.TestCase):
    def setUp(self):
        self.vector_db = VectorDatabase()  # Create an instance of VectorDatabase
        self.code_generator = CodeGenerator(vector_db=self.vector_db)
        self.mock_model = MockModel(name="TestModel")
        self.mock_model.device = "cpu"
        self.mock_model.generate = MagicMock(return_value="Mocked output")
        self.mock_model.tokenizer = MagicMock()
        self.mock_model.tokenizer.decode = MagicMock(return_value="Mocked output")
        self.mock_context = CodeContext(project_id="test_project", language="python")

    async def test_generate_text(self):
        result = await generate_text(self.mock_model, self.mock_model.tokenizer, "Test prompt")
        self.assertEqual(result, "Mocked output")

    async def test_code_generator_generate(self):
        result = await self.code_generator.generate("Test prompt", self.mock_context)
        self.assertEqual(result, "Mocked output")

    async def test_code_generator_generate_with_context(self):
        self.vector_db.add(project_id="test_project", code="Test code", embedding="Test embedding")
        result = await self.code_generator.generate("Test prompt", self.mock_context)
        self.assertEqual(result, "Mocked output")

    async def test_code_generator_generate_with_different_model(self):
        different_model = MockModel(name="DifferentModel")
        different_model.generate = MagicMock(return_value="Different output")
        self.code_generator.router.select = MagicMock(return_value=different_model)
        result = await self.code_generator.generate("Test prompt", self.mock_context)
        self.assertEqual(result, "Different output")

    async def test_code_generator_generate_error_handling(self):
        self.code_generator.vector_db.query = MagicMock(side_effect=Exception("Test error"))
        result = await self.code_generator.generate("Test prompt", self.mock_context)
        self.assertEqual(result, "")

if __name__ == '__main__':
    asyncio.run(unittest.main())
