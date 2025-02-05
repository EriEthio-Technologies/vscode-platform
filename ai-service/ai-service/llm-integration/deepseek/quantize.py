from transformers import BitsAndBytesConfig
import torch

def get_deepseek_quant_config() -> BitsAndBytesConfig:
    """4-bit quantization config for DeepSeek models"""
    return BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.bfloat16,
        bnb_4bit_use_double_quant=True
    )

def apply_deepseek_quantization(model):
    """Apply quantization to existing DeepSeek model"""
    quant_config = get_deepseek_quant_config()
    return model.quantize(quant_config)
