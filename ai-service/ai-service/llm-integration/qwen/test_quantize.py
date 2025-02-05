import unittest
import torch
from quantize import quantize_qwen_linear_layers

class TestQuantizeQwenLinearLayers(unittest.TestCase):
    def test_quantize_qwen_linear_layers(self):
        class MockModel(torch.nn.Module):
            def __init__(self):
                super(MockModel, self).__init__()
                self.attention = torch.nn.Linear(10, 10)
                self.mlp = torch.nn.Linear(10, 10)
                self.other = torch.nn.Linear(10, 10)

            def named_modules(self):
                return [("attention", self.attention), ("mlp", self.mlp), ("other", self.other)]

        model = MockModel()
        quantized_model = quantize_qwen_linear_layers(model)

        self.assertEqual(quantized_model.attention.weight.dtype, torch.int8)
        self.assertEqual(quantized_model.mlp.weight.dtype, torch.int8)
        self.assertNotEqual(quantized_model.other.weight.dtype, torch.int8)

if __name__ == '__main__':
    unittest.main()
