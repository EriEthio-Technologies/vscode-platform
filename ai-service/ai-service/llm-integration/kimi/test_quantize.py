import unittest
import torch
from transformers import GPTQConfig
from quantize import apply_kimi_adaptive_quant, get_kimi_gptq_config

class TestKimiQuantization(unittest.TestCase):
    def test_apply_kimi_adaptive_quant(self):
        class MockTokenizer:
            def __init__(self, model_max_length):
                self.model_max_length = model_max_length

        class MockModel(torch.nn.Module):
            def quantize(self, config):
                self.config = config
                return self

        model = MockModel()
        tokenizer = MockTokenizer(model_max_length=10000)
        quantized_model = apply_kimi_adaptive_quant(model, tokenizer)

        self.assertEqual(quantized_model.config, get_kimi_gptq_config())

if __name__ == '__main__':
    unittest.main()
