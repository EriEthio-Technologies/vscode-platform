import logging
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier, VotingClassifier
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import pandas as pd

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def train_model_selection_model(data_path: str, output_path: str = "model_selection_model.joblib"):
    """
    Trains a model selection model using scikit-learn.

    The model selection model is trained on a dataset of code examples with features such
    as language, complexity, and user preference. The model is used to predict the best
    model to use for a given code generation task.

    Args:
        data_path (str): The path to the training data. The training data should be a CSV file
            with columns for 'language', 'complexity', 'user_preference', and 'model'.
        output_path (str): The path to save the trained model.
    """
    logging.info(f"Training model selection model with data from {data_path}")

    try:
        # Load the data
        data = pd.read_csv(data_path)

        # Define the features and labels
        features = ['language', 'complexity', 'user_preference']
        labels = 'model'

        # Split the data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(data[features], data[labels], test_size=0.2, random_state=42)

        # Define the column transformer
        # The column transformer is used to preprocess the features.
        # Categorical features are one-hot encoded, and numerical features are scaled.
        categorical_features = ['language', 'user_preference']
        numerical_features = ['complexity']

        preprocessor = ColumnTransformer([
            ('onehot', OneHotEncoder(handle_unknown='ignore'), categorical_features),
            ('scaler', StandardScaler(), numerical_features)
        ])

        # Create individual classifiers
        gb_classifier = GradientBoostingClassifier(random_state=42)
        rf_classifier = RandomForestClassifier(random_state=42)

        # Create the voting classifier
        voting_clf = VotingClassifier(estimators=[('gb', gb_classifier), ('rf', rf_classifier)], voting='hard')

        # Create the pipeline
        # The pipeline is used to chain the transformer and the classifier.
        model = Pipeline([
            ('preprocessor', preprocessor),
            ('classifier', voting_clf)
        ])

        # Train the model
        model.fit(X_train, y_train)

        # Evaluate the model
        accuracy = model.score(X_test, y_test)
        logging.info(f"Model accuracy: {accuracy}")

        # Save the model
        joblib.dump(model, output_path)
        logging.info(f"Model saved to {output_path}")

    except Exception as e:
        logging.error(f"Error during model training: {e}", exc_info=True)
        raise

if __name__ == '__main__':
    # Example usage
    train_model_selection_model(data_path='model_selection_data.csv', output_path='model_selection_model.joblib')
