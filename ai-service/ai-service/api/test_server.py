import unittest
from fastapi.testclient import TestClient
from .server import app

class TestServer(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_generate_code(self):
        response = self.client.post("/generate", json={
            "prompt": "Create a function to add two numbers",
            "language": "python",
            "complexity": "simple"
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn("code", response.json())

    def test_generate_code_error(self):
        response = self.client.post("/generate", json={
            "prompt": "",
            "language": "python",
            "complexity": "simple"
        })
        self.assertEqual(response.status_code, 500)

if __name__ == '__main__':
    unittest.main()
