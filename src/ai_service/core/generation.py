# src/ai_service/core/generation.py
# Copyright (c) 2023 Your Company. All rights reserved.

import torch

def generate_text(model, tokenizer, prompt: str) -> str:
    """
    Generate text using the given model and tokenizer.

    Args:
        model: The model to use for text generation.
        tokenizer: The tokenizer to use for text generation.
        prompt (str): The prompt to generate text from.

    Returns:
        str: The generated text.
    """
    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = model.generate(**inputs)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

class CodeGenerator:
    def __init__(self):
        self.router = ModelRouter(models=[
            deepseek_33b,
            qwen_72b,
            kimi_22b
        ])

    async def generate(self, prompt: str, context: CodeContext) -> str:
        # Retrieve relevant code context
        related_code = self.vector_db.query(
            embedding=encode(prompt),
            project_id=context.project_id
        )

        # Route to best model
        selected_model = self.router.select(
            language=context.language,
            complexity=calculate_cyclomatic_complexity(related_code)
        )

        # Generate and validate
        raw_output = await selected_model.generate(
            prompt=prompt,
            context=related_code
        )
        return self.sanitizer.sanitize(raw_output)
