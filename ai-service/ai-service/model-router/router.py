# ai-service/model-router/router.py
class ModelRouter:
    def __init__(self, models: dict):
        self.models = models  # Dictionary of loaded LLM instances

    def select_model(self, prompt: str, language: str, complexity: int) -> str:
        """Route prompts based on language and complexity."""
        if language == "python" and complexity > 50:
            return self.models["deepseek"]
        elif "reason" in prompt.lower():
            return self.models["qwen"]
        else:
            return self.models["kimi"]
