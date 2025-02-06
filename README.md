# vscode-platform

## Overview

This project provides a platform for code generation using machine learning models.

## Getting Started

### Prerequisites

*   Python 3.9 or higher
*   pip
*   A virtual environment (recommended)

### Installation

1.  Clone the repository:

    ```bash
    git clone <repository_url>
    cd vscode-platform
    ```

2.  Create a virtual environment:

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Linux/macOS
    venv\Scripts\activate  # On Windows
    ```

3.  Install the dependencies:

    ```bash
    pip install -r requirements.txt
    ```

### Training the Model Selection Model

1.  Collect and prepare training data following the guidelines in [docs/data_collection.md](docs/data_collection.md).

2.  Create a CSV file named `model_selection_data.csv` with training data for the model selection model. The CSV file should have columns for `language`, `complexity`, `user_preference`, and `model`.

    ```csv
    language,complexity,user_preference,model
    python,5,performance,deepseek_33b
    python,15,performance,qwen_72b
    ...
    ```

3.  Run the training script:

    ```bash
    python scripts/train_model_selection_model.py
    ```

    This will train the model selection model and save it to `model_selection_model.joblib`.

### Running the Code Generation Platform

1.  Update the `language_encoder` and `user_preference_encoder` in `src/ai_service/model_router.py` to fit your actual data.

2.  Run the code generation platform:

    ```bash
    # Your command to run the platform
    ```

## Contributing

Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details on how to contribute to this project.

