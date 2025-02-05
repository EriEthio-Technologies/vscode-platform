# ai-service/api/server.py
from fastapi import FastAPI, HTTPException
from ..model_router.router import ModelRouter
from ..llm_integration.deepseek.adapter import DeepSeekAdapter
from ..llm_integration.qwen.adapter import QwenAdapter
from ..llm_integration.kimi.adapter import KimiAdapter
from .schemas import CodeRequest
import logging

app = FastAPI()
logging.basicConfig(level=logging.INFO)

@app.post("/generate")
async def generate_code(request: CodeRequest) -> dict:
    """
    Generate code based on the provided request.

    Args:
        request (CodeRequest): The request containing the prompt, language, and complexity.

    Returns:
        dict: A dictionary containing the generated code.
    """
    try:
        logging.info(f"Received request: {request}")
        router = ModelRouter(models={
            "deepseek": DeepSeekAdapter("/models/deepseek"),
            "qwen": QwenAdapter("/models/qwen"),
            "kimi": KimiAdapter("/models/kimi")
        })
        selected_model = router.select_model(request.prompt, request.language, request.complexity)
        logging.info(f"Selected model: {selected_model}")
        code = selected_model.generate(request.prompt)
        logging.info(f"Generated code: {code}")
        return {"code": code}
    except Exception as e:
        logging.error(f"Error generating code: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
