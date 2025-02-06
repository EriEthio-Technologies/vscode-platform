import logging
import joblib  # For loading the trained model
import os
from sklearn.preprocessing import OneHotEncoder, StandardScaler
import numpy as np

class ModelRouter:
    """
    Routes requests to the best model based on language, complexity, and user preference.
    """
    def __init__(self, models: list, model_selection_model_path: str = "model_selection_model.joblib"):
        self.models = models
        self.model_selection_model = self.load_model_selection_model(model_selection_model_path)
        self.model_selection_model_path = model_selection_model_path
        logging.info(f"ModelRouter initialized with models: {models} and model selection model: {self.model_selection_model}")

        # Initialize encoders
        self.language_encoder = OneHotEncoder(handle_unknown='ignore')
        self.user_preference_encoder = OneHotEncoder(handle_unknown='ignore')
        self.scaler = StandardScaler()

        # Fit encoders (replace with your actual data)
        self.language_encoder.fit([['python'], ['javascript'], ['java']])
        self.user_preference_encoder.fit([['performance'], ['accuracy'], ['cost']])

    def load_model_selection_model(self, model_path: str):
        """Loads the model selection model from disk."""
        if os.path.exists(model_path):
            logging.info(f"Loading model selection model from {model_path}")
            return joblib.load(model_path)
        else:
            logging.warning(f"Model selection model not found at {model_path}. Using default routing.")
            return None

    def select(self, language: str, complexity: int, user_preference: str = None):
        """
        Selects the best model based on language, complexity, and user preference.
        """
        logging.info(f"Selecting model for language: {language}, complexity: {complexity}, and user preference: {user_preference}")

        if self.model_selection_model:
            # Prepare the input features for the model
            features = [language, complexity, user_preference]
            # Preprocess the features
            processed_features = self.preprocess_features(features)

            # Use the model to predict the best model
            model_index = self.model_selection_model.predict(processed_features)[0]
            selected_model = self.models[model_index]
            logging.info(f"Model selection model predicted model: {selected_model.name}")
            return selected_model
        else:
            # Fallback to the default routing logic if no model selection model is available
            if language == "python" and complexity > 10:
                logging.info("Selecting advanced model for Python")
                return self.models[0]  # Example: Select the first model for Python and high complexity
            else:
                logging.info("Selecting default model")
                return self.models[0]  # Default: Select the first model

    def preprocess_features(self, features: list):
        """Preprocesses the input features for the model selection model."""
        logging.info(f"Preprocessing features: {features}")
        language, complexity, user_preference = features

        # One-hot encode categorical features
        language_encoded = self.language_encoder.transform([[language]]).toarray()
        user_preference_encoded = self.user_preference_encoder.transform([[user_preference]]).toarray()

        # Scale numerical features
        complexity_scaled = self.scaler.fit_transform([[complexity]])

        # Combine the features
        processed_features = np.concatenate([language_encoded, user_preference_encoded, complexity_scaled], axis=1)

        return processed_features

    def __repr__(self):
         return f"ModelRouter(models={[model.name for model in self.models]})"
