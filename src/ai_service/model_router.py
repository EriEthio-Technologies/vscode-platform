import logging
import joblib  # For loading the trained model
import os
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier, VotingClassifier
import numpy as np
import pandas as pd

class ModelRouter:
    """
    Routes requests to the best model based on language, complexity, and user preference.

    The ModelRouter uses a machine learning model to predict the best model to use for a given
    code generation task. The model is trained on a dataset of code examples with features such
    as language, complexity, and user preference.

    Attributes:
        models (list): A list of available models.
        model_selection_model_path (str): The path to the trained model selection model.
        model_selection_model: The trained model selection model (Pipeline).
        model_mapping (dict): A mapping between model names and their corresponding objects.
        preprocessor (ColumnTransformer): The preprocessor for the input features.
    """
    def __init__(self, models: list, model_selection_model_path: str = "model_selection_model.joblib"):
        """
        Initializes the ModelRouter.

        Args:
            models (list): A list of available models.
            model_selection_model_path (str): The path to the trained model selection model.
        """
        self.models = models
        self.model_selection_model = self.load_model_selection_model(model_selection_model_path)
        self.model_selection_model_path = model_selection_model_path
        self.model_mapping = {model.name: model for model in models}  # Map model names to model objects
        logging.info(f"ModelRouter initialized with models: {[m.name for m in self.models]} and model selection model: {self.model_selection_model}")

        # Define the column transformer
        # The column transformer is used to preprocess the features.
        # Categorical features are one-hot encoded, and numerical features are scaled.
        categorical_features = ['language', 'user_preference']
        numerical_features = ['complexity']

        self.preprocessor = ColumnTransformer([
            ('onehot', OneHotEncoder(handle_unknown='ignore'), categorical_features),
            ('scaler', StandardScaler(), numerical_features)
        ], remainder='passthrough') # Add remainder='passthrough'

    def load_model_selection_model(self, model_path: str):
        """
        Loads the model selection model from disk.

        Args:
            model_path (str): The path to the trained model selection model.

        Returns:
            The trained model selection model (Pipeline), or None if the model is not found.
        """
        if os.path.exists(model_path):
            logging.info(f"Loading model selection model from {model_path}")
            try:
                model = joblib.load(model_path)
                # Check if the loaded object is a Pipeline
                if isinstance(model, Pipeline):
                    return model
                else:
                    logging.error(f"Model at {model_path} is not a Pipeline. Using default routing.")
                    return None
            except Exception as e:
                logging.error(f"Error loading model from {model_path}: {e}", exc_info=True)
                return None
        else:
            logging.warning(f"Model selection model not found at {model_path}. Using default routing.")
            return None

    def select(self, language: str, complexity: int, user_preference: str = None):
        """
        Selects the best model based on language, complexity, and user preference.

        Args:
            language (str): The programming language of the code.
            complexity (int): The complexity of the code.
            user_preference (str): The user's preference for the model (e.g., performance, accuracy, cost).

        Returns:
            The selected model (ActualModel).
        """
        logging.info(f"Selecting model for language: {language}, complexity: {complexity}, and user preference: {user_preference}")

        if self.model_selection_model:
            try:
                # Prepare the input features for the model
                features = {'language': language, 'complexity': complexity, 'user_preference': user_preference}
                # Convert features to DataFrame
                features_df = pd.DataFrame([features])

                # Preprocess the features
                processed_features = self.preprocess_features(features_df)

                # Use the model to predict the best model
                model_name = self.model_selection_model.predict(processed_features)[0]
                selected_model = self.model_mapping.get(model_name)  # Use model_mapping to get the model object

                if selected_model:
                    logging.info(f"Model selection model predicted model: {selected_model.name}")
                    return selected_model
                else:
                    logging.warning(f"Predicted model '{model_name}' not found in available models. Using default routing.")
                    return self.default_routing(language, complexity)
            except Exception as e:
                logging.error(f"Error during model selection: {e}", exc_info=True)
                return self.default_routing(language, complexity)
        else:
            # Fallback to the default routing logic if no model selection model is available
            return self.default_routing(language, complexity)

    def preprocess_features(self, features_df: pd.DataFrame):
        """
        Preprocesses the input features for the model selection model.

        Args:
            features_df (pd.DataFrame): A DataFrame of input features.

        Returns:
            The preprocessed features (numpy array).
        """
        logging.info(f"Preprocessing features: {features_df}")

        try:
            # Transform the features using the preprocessor
            processed_features = self.preprocessor.transform(features_df)
            return processed_features
        except Exception as e:
            logging.error(f"Error during feature preprocessing: {e}", exc_info=True)
            return None

    def default_routing(self, language: str, complexity: int):
        """
        Selects a default model based on language and complexity.

        Args:
            language (str): The programming language of the code.
            complexity (int): The complexity of the code.

        Returns:
            The selected model (ActualModel).
        """
        logging.info(f"Using default routing for language: {language} and complexity: {complexity}")
        if language == "python" and complexity > 10:
            logging.info("Selecting advanced model for Python")
            return self.models[0]  # Example: Select the first model for Python and high complexity
        else:
            logging.info("Selecting default model")
            return self.models[0]  # Default: Select the first model

    def __repr__(self):
         return f"ModelRouter(models={[model.name for model in self.models]})"
