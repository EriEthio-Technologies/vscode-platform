# src/ai_service/core/generation.py
# Copyright (c) 2023 Your Company. All rights reserved.

import torch
from ai_service.model_router import ModelRouter
# Import necessary modules
import asyncio
import logging
from ai_service.core.code_context import CodeContext
from ai_service.vector_database import VectorDatabase
from ai_service.utils import encode, calculate_cyclomatic_complexity, sanitize
from ai_service.models import deepseek_33b, qwen_72b, kimi_22b

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

async def generate_text(model, prompt: str) -> str:
    """
    Generate text using the given model asynchronously.

    Args:
        model: The model to use for text generation.
        prompt (str): The prompt to generate text from.

    Returns:
        str: The generated text.
    """
    logging.info(f"Generating text with model: {model.name}")
    try:
        logging.info(f"Generating with prompt: {prompt}")
        output = await model.generate(prompt=prompt)
        return output
    except Exception as e:
        logging.error(f"Error during text generation: {e}", exc_info=True)
        return ""

class CodeGenerator:
    def __init__(self, vector_db: VectorDatabase):
        self.router = ModelRouter(models=[
            deepseek_33b,
            qwen_72b,
            kimi_22b
        ])
        self.vector_db = vector_db
        self.sanitizer = sanitize # Assuming sanitize is a function or class
        logging.info("CodeGenerator initialized")

    async def generate(self, prompt: str, context: CodeContext) -> str:
        """
        Generates code based on the given prompt and context.

        Args:
            prompt (str): The code generation prompt.
            context (CodeContext): The context in which the code is generated.

        Returns:
            str: The generated code.
        """
        logging.info(f"Generating code for prompt: {prompt} in project: {context.project_id}")
        try:
            # Retrieve relevant code context
            logging.info("Retrieving related code...")
            related_code = self.vector_database.query(
                embedding=encode(prompt),
                project_id=context.project_id
            )

            # Route to best model
            logging.info("Routing to best model...")
            selected_model = self.router.select(
                language=context.language,
                complexity=calculate_cyclomatic_complexity(related_code)
            )

            # Generate and validate
            logging.info(f"Generating code with model: {selected_model.name}")
            raw_output = await generate_text(
                model=selected_model,
                prompt=prompt,
            )
            logging.info("Sanitizing output...")
            return self.sanitizer(raw_output)
        except Exception as e:
            logging.error(f"Error during code generation: {e}", exc_info=True)
            return ""
