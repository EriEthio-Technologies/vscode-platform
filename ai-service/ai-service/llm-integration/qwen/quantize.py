from transformers import BitsAndBytesConfig
import torch

def get_qwen_quant_config() -> BitsAndBytesConfig:
    """8-bit quantization config for Qwen models"""
    return BitsAndBytesConfig(
        load_in_8bit=True,
        llm_int8_threshold=6.0,
        llm_int8_has_fp16_weight=False,
        bnb_8bit_compute_dtype=torch.float16
    )

def quantize_qwen_linear_layers(model):
    """Apply quantization to specific layers"""
    for name, module in model.named_modules():
        if "attention" in name or "mlp" in name:
            module = module.to(torch.int8)
    return model
