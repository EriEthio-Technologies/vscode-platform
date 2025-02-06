import logging
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

class ActualModel:
    """
    Implementation of a model using Hugging Face Transformers.
    """
    def __init__(self, name: str, model_id: str, device: str = "cuda" if torch.cuda.is_available() else "cpu"):
        self.name = name
        self.model_id = model_id
        self.device = device
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(model_id)
            self.model = AutoModelForCausalLM.from_pretrained(model_id).to(device)
            logging.info(f"Model {name} loaded from {model_id} on device: {device}")
        except Exception as e:
            logging.error(f"Error loading model {name} from {model_id}: {e}", exc_info=True)
            raise

    async def generate(self, prompt: str = None, context: str = None, max_length: int = 200, **kwargs):
        """
        Generate code using the loaded model.
        """
        log_message = f"Generating code with {self.name}"
        if prompt:
            log_message += f" for prompt: {prompt[:50]}"
        if context:
            log_message += f" with context: {context[:50]}"
        logging.info(log_message)

        try:
            inputs = self.tokenizer(prompt + context, return_tensors="pt").to(self.device)
            outputs = self.model.generate(**inputs, max_length=max_length)
            return self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        except Exception as e:
            logging.error(f"Error during code generation with {self.name}: {e}", exc_info=True)
            return ""

    def decode(self, tokens, skip_special_tokens=True):
        """Decode method."""
        logging.info(f"Decoding tokens: {tokens[:50]}...")
        return self.tokenizer.decode(tokens, skip_special_tokens=True)

    def __repr__(self):
        return f"ActualModel(name='{self.name}', model_id='{self.model_id}', device='{self.device}')"

# Example models - replace with your desired models
deepseek_33b = ActualModel(name="deepseek_33b", model_id="EleutherAI/gpt-j-6B") # Replace with actual model ID
qwen_72b = ActualModel(name="qwen_72b", model_id="EleutherAI/gpt-j-6B") # Replace with actual model ID
kimi_22b = ActualModel(name="kimi_22b", model_id="EleutherAI/gpt-j-6B") # Replace with actual model ID
