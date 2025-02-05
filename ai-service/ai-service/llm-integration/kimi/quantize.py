from transformers import GPTQConfig
import torch
import logging

logging.basicConfig(level=logging.INFO)

def getKimiGptqConfig() -> GPTQConfig:
    """GPTQ quantization config for Kimi models"""
    return GPTQConfig(
        bits=4,
        group_size=128,
        desc_act=False
    )

def applyKimiAdaptiveQuant(model, tokenizer):
    """Apply GPTQ quantization to Kimi models

    Args:
        model: The model to be quantized.
        tokenizer: The tokenizer associated with the model.

    Returns:
        The quantized model.
    """
    try:
        config = getKimiGptqConfig()
        model = model.quantize(config)
        logging.info("Quantization successful")
        return model
    except Exception as e:
        logging.error(f"Quantization failed: {e}")
        raise
