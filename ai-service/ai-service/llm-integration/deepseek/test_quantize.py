import unittest
import torch
from quantize import apply_deepseek_quantization, get_deepseek_quant_config

class TestDeepSeekQuantization(unittest.TestCase):
    def test_apply_deepseek_quantization(self):
        class MockModel(torch.nn.Module):
            def quantize(self, config):
                self.config = config
                return self

        model = MockModel()
        quantized_model = apply_deepseek_quantization(model)

        self.assertEqual(quantized_model.config, get_deepseek_quant_config())

if __name__ == '__main__':
    unittest.main()
