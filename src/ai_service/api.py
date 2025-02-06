from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Optional
from ai_service.core.generation import CodeGenerator
from ai_service.core.code_context import CodeContext
from ai_service.vector_database import VectorDatabase
from ai_service.models import deepseek_33b, qwen_72b, kimi_22b, ActualModel
import logging
import os
import sqlite3
import asyncio
from ai_service.model_router import ModelRouter
from scripts.train_model_selection_model import train_model_selection_model
from sse_starlette.sse import EventSourceResponse
import time

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = FastAPI()

# CORS configuration
origins = [
    "http://localhost:3000",  # Example: Allow requests from your React app
    "http://localhost:8000",  # Add any other origins as needed
    "http://localhost:5173",
    "http://localhost:5173/",
    "http://localhost:4173",
    "http://localhost:4173/",
    "*",  # WARNING: This allows all origins. Use with caution in production.
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize VectorDatabase (replace with your actual initialization)
vector_db = VectorDatabase()

# Initialize CodeGenerator
code_generator = CodeGenerator(vector_db=vector_db)

# Define available models
available_models = {
    "deepseek_33b": "EleutherAI/gpt-j-6B",
    "qwen_72b": "EleutherAI/gpt-j-6B",
    "kimi_22b": "EleutherAI/gpt-j-6B",
}

# Model name mappings
model_name_mappings = {
    "deepseek_33b": "EleutherAI/gpt-j-6B",
    "qwen_72b": "EleutherAI/gpt-j-6B",
    "kimi_22b": "EleutherAI/gpt-j-6B",
    # Add more mappings as needed
}

# Database configuration
DATABASE_FILE = "settings.db"
MODEL_SELECTION_DATA = "model_selection_data.csv"
MODEL_SELECTION_MODEL = "model_selection_model.joblib"

def get_db_connection():
    """Gets a database connection."""
    conn = None
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        conn.row_factory = sqlite3.Row  # Access columns by name
        return conn
    except sqlite3.Error as e:
        logging.error(f"Error connecting to database: {e}", exc_info=True)
        if conn:
            conn.close()
        raise

def initialize_db():
    """Initializes the database."""
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS settings (
                id INTEGER PRIMARY KEY,
                strategy TEXT NOT NULL,
                model TEXT
            )
        """)
        # Check if settings exist, if not, insert default settings
        cursor.execute("SELECT COUNT(*) FROM settings")
        count = cursor.fetchone()[0]
        if count == 0:
            cursor.execute("INSERT INTO settings (strategy, model) VALUES (?, ?)", ("auto", None))
        conn.commit()
        logging.info("Database initialized successfully.")
    except sqlite3.Error as e:
        logging.error(f"Error initializing database: {e}", exc_info=True)
    finally:
        if conn:
            conn.close()

# Initialize the database
initialize_db()

# Load initial settings from the database
def load_settings():
    """Loads settings from the database."""
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT strategy, model FROM settings LIMIT 1")
        row = cursor.fetchone()
        if row:
            return {"strategy": row["strategy"], "model": row["model"]}
        else:
            return {"strategy": "auto", "model": None}
    except sqlite3.Error as e:
        logging.error(f"Error loading settings from database: {e}", exc_info=True)
        return {"strategy": "auto", "model": None}
    finally:
        if conn:
            conn.close()

# Save settings to the database
def save_settings(settings: dict):
    """Saves settings to the database."""
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE settings SET strategy=?, model=? WHERE id=1", (settings["strategy"], settings["model"]))
        conn.commit()
        logging.info("Settings saved to database successfully.")
    except sqlite3.Error as e:
        logging.error(f"Error saving settings to database: {e}", exc_info=True)
    finally:
        if conn:
            conn.close()

# Load initial settings
settings = load_settings()
current_strategy = settings["strategy"]
selected_model = settings["model"]

async def model_update_process():
    """
    Simulates the model update process and yields progress updates.
    """
    total_steps = 10
    for i in range(total_steps):
        await asyncio.sleep(1)  # Simulate a step in the update process
        progress = int((i + 1) / total_steps * 100)
        yield {"data": {"progress": progress, "message": f"Updating model: {progress}%"}}
    # After the loop, yield a completion message
    yield {"data": {"progress": 100, "message": "Model update completed successfully."}}

async def update_model_selection_model():
    """
    Updates the model selection model by retraining it.
    """
    logging.info("Updating model selection model...")
    try:
        train_model_selection_model(data_path=MODEL_SELECTION_DATA, output_path=MODEL_SELECTION_MODEL)
        # Reload the ModelRouter with the new model
        global code_generator
        code_generator.router = ModelRouter(models=[
            deepseek_33b,
            qwen_72b,
            kimi_22b
        ], model_selection_model_path=MODEL_SELECTION_MODEL)
        logging.info("Model selection model updated successfully.")
    except Exception as e:
        logging.error(f"Error updating model selection model: {e}", exc_info=True)

async def periodic_model_update():
    """
    Periodically updates the model selection model.
    """
    while True:
        await asyncio.sleep(60 * 60 * 24 * 7)  # Update every 7 days
        await update_model_selection_model()

@app.on_event("startup")
async def startup_event():
    """
    Startup event to initialize the periodic model update task.
    """
    asyncio.create_task(periodic_model_update())

# New endpoint to trigger model update manually
@app.get("/update_model")
async def update_model():
    """
    Triggers a manual update of the model selection model and streams progress.
    """
    logging.info("Manual model update triggered")
    return EventSourceResponse(model_update_process())

# Endpoint to get available models
@app.get("/models", response_model=List[str])
async def get_models():
    """
    Returns a list of available model names.
    """
    try:
        return list(available_models.keys())
    except Exception as e:
        logging.error(f"Error getting models: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to retrieve models")

# Endpoint to generate code
@app.post("/generate")
async def generate_code(prompt: str, language: str, project_id: str):
    """
    Generates code based on the given prompt, language, and project ID.
    """
    try:
        context = CodeContext(project_id=project_id, language=language)
        generated_code = await code_generator.generate(prompt=prompt, context=context)
        return {"code": generated_code}
    except Exception as e:
        logging.error(f"Error generating code: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to generate code")

# Endpoint to set model selection strategy
@app.post("/set_strategy")
async def set_strategy(strategy: str = Query(..., enum=["auto", "manual"])):
    """
    Sets the model selection strategy (auto or manual).
    """
    try:
        global current_strategy
        current_strategy = strategy
        settings["strategy"] = strategy
        save_settings(settings)
        logging.info(f"Setting model selection strategy to: {strategy}")
        return {"message": f"Model selection strategy set to {strategy}"}
    except Exception as e:
        logging.error(f"Error setting strategy: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to set strategy")

# Endpoint to set selected model (manual strategy)
@app.post("/set_model")
async def set_model(model: str = Query(None)):
    """
    Sets the selected model when the strategy is manual.
    """
    try:
        global selected_model
        selected_model = model
        settings["model"] = model
        save_settings(settings)
        logging.info(f"Setting selected model to: {model}")
        return {"message": f"Selected model set to {model}"}
    except Exception as e:
        logging.error(f"Error setting model: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to set model")

# Endpoint to get model name mappings
@app.get("/model_mappings", response_model=Dict[str, str])
async def get_model_mappings():
    """
    Returns a dictionary of model name mappings.
    """
    try:
        return model_name_mappings
    except Exception as e:
        logging.error(f"Error getting model mappings: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to retrieve model mappings")

# Endpoint to get current settings
@app.get("/settings", response_model=Dict[str, Optional[str]])
async def get_settings():
    """
    Returns the current settings (strategy and selected model).
    """
    try:
        return {"strategy": current_strategy, "model": selected_model}
    except Exception as e:
        logging.error(f"Error getting settings: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to retrieve settings")
