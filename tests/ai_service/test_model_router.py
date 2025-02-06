import unittest
from unittest.mock import MagicMock
import joblib
import pandas as pd
from sklearn.pipeline import Pipeline
from ai_service.model_router import ModelRouter
from ai_service.models import ActualModel
import numpy as np
import os

class TestModelRouter(unittest.TestCase):
    def setUp(self):
        # Create mock models
        self.mock_model1 = ActualModel(name="deepseek_33b", model_id="EleutherAI/gpt-j-6B")
        self.mock_model2 = ActualModel(name="qwen_72b", model_id="EleutherAI/gpt-j-6B")
        self.mock_model3 = ActualModel(name="kimi_22b", model_id="EleutherAI/gpt-j-6B")
        self.models = [self.mock_model1, self.mock_model2, self.mock_model3]

        # Create a mock model selection model (Pipeline)
        self.mock_pipeline = MagicMock(spec=Pipeline)
        self.mock_pipeline.predict.return_value = ["deepseek_33b"]  # Always predict the first model

        # Save the mock pipeline to a file
        self.model_path = "test_model.joblib"
        joblib.dump(self.mock_pipeline, self.model_path)

        # Initialize ModelRouter with the mock model and model selection model
        self.router = ModelRouter(models=self.models, model_selection_model_path=self.model_path)

    def tearDown(self):
        # Remove the mock model file
        if os.path.exists(self.model_path):
            os.remove(self.model_path)

    def test_load_model_selection_model(self):
        # Test that the model selection model is loaded correctly
        self.assertIsInstance(self.router.model_selection_model, Pipeline)

    def test_load_model_selection_model_not_found(self):
        # Test that the model selection model is None if the file is not found
        router = ModelRouter(models=self.models, model_selection_model_path="non_existent_model.joblib")
        self.assertIsNone(router.model_selection_model)

    def test_select(self):
        # Test that the select method returns a model
        selected_model = self.router.select(language="python", complexity=5, user_preference="performance")
        self.assertIsInstance(selected_model, ActualModel)
        self.assertEqual(selected_model.name, "deepseek_33b")  # Because mock_pipeline always predicts 0

    def test_select_default_routing(self):
        # Test that the select method returns the default model if no model selection model is available
        router = ModelRouter(models=self.models, model_selection_model_path="non_existent_model.joblib")
        selected_model = router.select(language="python", complexity=15, user_preference="accuracy")
        self.assertIsInstance(selected_model, ActualModel)
        self.assertEqual(selected_model.name, "deepseek_33b")  # Default routing for python and complexity > 10

    def test_preprocess_features(self):
         # Test that the preprocess_features method returns a numpy array
        features = {'language': "python", 'complexity': 5, 'user_preference': "performance"}
        # Convert features to DataFrame
        features_df = pd.DataFrame([features])
        processed_features = self.router.preprocess_features(features_df)
        self.assertIsInstance(processed_features, np.ndarray)

    def test_select_model_not_found(self):
        # Test that the select method returns the default model if the predicted model is not found
        self.mock_pipeline.predict.return_value = ["non_existent_model"]
        router = ModelRouter(models=self.models, model_selection_model_path=self.model_path)
        selected_model = router.select(language="python", complexity=5, user_preference="performance")
        self.assertIsInstance(selected_model, ActualModel)
        self.assertEqual(selected_model.name, "deepseek_33b")  # Default routing

    def test_select_error_during_model_selection(self):
        # Test that the select method returns the default model if there is an error during model selection
        self.mock_pipeline.predict.side_effect = Exception("Test exception")
        router = ModelRouter(models=self.models, model_selection_model_path=self.model_path)
        selected_model = router.select(language="python", complexity=5, user_preference="performance")
        self.assertIsInstance(selected_model, ActualModel)
        self.assertEqual(selected_model.name, "deepseek_33b")  # Default routing

    def test_preprocess_features_error(self):
        # Test that the preprocess_features method returns None if there is an error during feature preprocessing
        router = ModelRouter(models=self.models, model_selection_model_path=self.model_path)
        router.preprocessor.transform = MagicMock(side_effect=Exception("Test exception"))
        features = {'language': "python", 'complexity': 5, 'user_preference': "performance"}
        features_df = pd.DataFrame([features])
        processed_features = router.preprocess_features(features_df)
        self.assertIsNone(processed_features)

    def test_default_routing_python_high_complexity(self):
        # Test that the default routing selects the advanced model for Python and high complexity
        selected_model = self.router.default_routing(language="python", complexity=15)
        self.assertIsInstance(selected_model, ActualModel)
        self.assertEqual(selected_model.name, "deepseek_33b")  # First model is considered advanced

    def test_default_routing_default_model(self):
        # Test that the default routing selects the default model for other cases
        selected_model = self.router.default_routing(language="javascript", complexity=5)
        self.assertIsInstance(selected_model, ActualModel)
        self.assertEqual(selected_model.name, "deepseek_33b")  # First model is the default

    def test_select_with_valid_model_name(self):
        # Test that the select method returns the correct model when a valid model name is predicted
        self.mock_pipeline.predict.return_value = ["qwen_72b"]
        selected_model = self.router.select(language="python", complexity=5, user_preference="performance")
        self.assertIsInstance(selected_model, ActualModel)
        self.assertEqual(selected_model.name, "qwen_72b")

if __name__ == '__main__':
    unittest.main()
