# vscode-platform

## Description

This project provides a platform for code generation and AI-assisted development.

## Core Components

*   **`/src/ai_service`**: This directory contains the core AI service logic for the `vscode-platform` project. It includes:
    *   `api.py`: Defines the API endpoints for code generation, model selection, and settings management.
    *   `core/generation.py`: Implements the code generation logic, including model routing and interaction with the vector database.
    *   `model_router.py`: Implements the `ModelRouter` class, which selects the best model based on language, complexity, and user preference.
    *   `models.py`: Defines the `ActualModel` class and initializes the available models.
    *   `vector_database.py`: Implements the `VectorDatabase` class for storing and retrieving code context.
    *   `utils.py`: Contains utility functions for encoding, calculating cyclomatic complexity, and sanitizing code.


*   **`/src/ai_service`**: This directory contains the core AI service logic for the `vscode-platform` project. It includes:
    *   `api.py`: Defines the API endpoints for code generation, model selection, and settings management.
    *   `core/generation.py`: Implements the code generation logic, including model routing and interaction with the vector database.
    *   `model_router.py`: Implements the `ModelRouter` class, which selects the best model based on language, complexity, and user preference.
    *   `models.py`: Defines the `ActualModel` class and initializes the available models.
    *   `vector_database.py`: Implements the `VectorDatabase` class for storing and retrieving code context.
    *   `utils.py`: Contains utility functions for encoding, calculating cyclomatic complexity, and sanitizing code.

// ...existing code...
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

2.  Run the code generation platform:    ```bash    # Your command to run the platform    ```### Managing Outdated FilesTo keep the `src/ai_service` directory clean and manageable, you can use the `delete_outdated_ai_service.py` script to remove files that haven't been modified in a specified period.#### Usage1.  Navigate to the project root directory.2.  Run the script with the directory and number of days as arguments:    ```bash    python src/delete_outdated_ai_service.py src/ai_service 30    ```    This command will delete files in the `src/ai_service` directory that haven't been modified in the last 30 days.#### Explanation*   `src/delete_outdated_ai_service.py`: The script that deletes outdated files.*   `src/ai_service`: The directory to clean.*   `30`: The number of days after which a file is considered outdated.This script helps maintain the project by removing old and unused files, ensuring that the codebase remains relevant and efficient.### Deleting the ai-service/ai_service DirectoryAfter consolidating the contents of `/workspaces/vscode-platform/src/ai_service` and `/workspaces/vscode-platform/ai-service/ai_service`, you can use the `delete_outdated_ai_service.py` script to delete the now-empty directory.#### Usage1.  Navigate to the project root directory.2.  Run the script:    ```bash    python src/delete_outdated_ai_service.py    ```    The script will prompt you to confirm the deletion of the `/workspaces/vscode-platform/ai-service/ai_service` directory. Type `y` to confirm or `n` to cancel.#### Explanation*   `src/delete_outdated_ai_service.py`: The script that deletes the specified directory.**Important:** Ensure that you have consolidated the necessary files before running this script, as it will permanently delete the directory.## ContributingPlease see [CONTRIBUTING.md](CONTRIBUTING.md) for details on how to contribute to this project.* Review [source code changes](https://github.com/microsoft/vscode/pulls)* Review the [documentation](https://github.com/microsoft/vscode-docs) and make pull requests for anything from typos to additional and new contentIf you are interested in fixing issues and contributing directly to the code base,please see the document [How to Contribute](https://github.com/microsoft/vscode/wiki/How-to-Contribute), which covers the following:* [How to build and run from source](https://github.com/microsoft/vscode/wiki/How-to-Contribute)* [The development workflow, including debugging and running tests](https://github.com/microsoft/vscode/wiki/How-to-Contribute#debugging)* [Coding guidelines](https://github.com/microsoft/vscode/wiki/Coding-Guidelines)* [Submitting pull requests](https://github.com/microsoft/vscode/wiki/How-to-Contribute#pull-requests)* [Finding an issue to work on](https://github.com/microsoft/vscode/wiki/How-to-Contribute#where-to-contribute)* [Contributing to translations](https://aka.ms/vscodeloc)## Feedback* Ask a question on [Stack Overflow](https://stackoverflow.com/questions/tagged/vscode)* [Request a new feature](CONTRIBUTING.md)* Upvote [popular feature requests](https://github.com/microsoft/vscode/issues?q=is%3Aopen+is%3Aissue+label%3Afeature-request+sort%3Areactions-%2B1-desc)* [File an issue](https://github.com/microsoft/vscode/issues)* Connect with the extension author community on [GitHub Discussions](https://github.com/microsoft/vscode-discussions/discussions) or [Slack](https://aka.ms/vscode-dev-community)* Follow [@code](https://twitter.com/code) and let us know what you think!See our [wiki](https://github.com/microsoft/vscode/wiki/Feedback-Channels) for a description of each of these channels and information on some other available community-driven channels.## Related ProjectsMany of the core components and extensions to VS Code live in their own repositories on GitHub. For example, the [node debug adapter](https://github.com/microsoft/vscode-node-debug) and the [mono debug adapter](https://github.com/microsoft/vscode-mono-debug) repositories are separate from each other. For a complete list, please visit the [Related Projects](https://github.com/microsoft/vscode/wiki/Related-Projects) page on our [wiki](https://github.com/microsoft/vscode/wiki).## Bundled ExtensionsVS Code includes a set of built-in extensions located in the [extensions](extensions) folder, including grammars and snippets for many languages. Extensions that provide rich language support (code completion, Go to Definition) for a language have the suffix `language-features`. For example, the `json` extension provides coloring for `JSON` and the `json-language-features` extension provides rich language support for `JSON`.## Development ContainerThis repository includes a Visual Studio Code Dev Containers / GitHub Codespaces development container.* For [Dev Containers](https://aka.ms/vscode-remote/download/containers), use the **Dev Containers: Clone Repository in Container Volume...** command which creates a Docker volume for better disk I/O on macOS and Windows.  * If you already have VS Code and Docker installed, you can also click [here](https://vscode.dev/redirect?url=vscode://ms-vscode-remote.remote-containers/cloneInVolume?url=https://github.com/microsoft/vscode) to get started. This will cause VS Code to automatically install the Dev Containers extension if needed, clone the source code into a container volume, and spin up a dev container for use.* For Codespaces, install the [GitHub Codespaces](https://marketplace.visualstudio.com/items?itemName=GitHub.codespaces) extension in VS Code, and use the **Codespaces: Create New Codespace** command.Docker / the Codespace should have at least **4 Cores and 6 GB of RAM (8 GB recommended)** to run full build. See the [development container README](.devcontainer/README.md) for more information.## Code of ConductThis project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/). For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.## LicenseCopyright (c) Microsoft Corporation. All rights reserved.Licensed under the [MIT](LICENSE.txt) license.
2.  Run the code generation platform:

    ```bash
    # Your command to run the platform
    ```

## Contributing

Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details on how to contribute to this project.

* Review [source code changes](https://github.com/microsoft/vscode/pulls)
* Review the [documentation](https://github.com/microsoft/vscode-docs) and make pull requests for anything from typos to additional and new content

If you are interested in fixing issues and contributing directly to the code base,
please see the document [How to Contribute](https://github.com/microsoft/vscode/wiki/How-to-Contribute), which covers the following:

* [How to build and run from source](https://github.com/microsoft/vscode/wiki/How-to-Contribute)
* [The development workflow, including debugging and running tests](https://github.com/microsoft/vscode/wiki/How-to-Contribute#debugging)
* [Coding guidelines](https://github.com/microsoft/vscode/wiki/Coding-Guidelines)
* [Submitting pull requests](https://github.com/microsoft/vscode/wiki/How-to-Contribute#pull-requests)
* [Finding an issue to work on](https://github.com/microsoft/vscode/wiki/How-to-Contribute#where-to-contribute)
* [Contributing to translations](https://aka.ms/vscodeloc)

## Feedback

* Ask a question on [Stack Overflow](https://stackoverflow.com/questions/tagged/vscode)* [Request a new feature](CONTRIBUTING.md)* Upvote [popular feature requests](https://github.com/microsoft/vscode/issues?q=is%3Aopen+is%3Aissue+label%3Afeature-request+sort%3Areactions-%2B1-desc)* [File an issue](https://github.com/microsoft/vscode/issues)* Connect with the extension author community on [GitHub Discussions](https://github.com/microsoft/vscode-discussions/discussions) or [Slack](https://aka.ms/vscode-dev-community)* Follow [@code](https://twitter.com/code) and let us know what you think!See our [wiki](https://github.com/microsoft/vscode/wiki/Feedback-Channels) for a description of each of these channels and information on some other available community-driven channels.## Related ProjectsMany of the core components and extensions to VS Code live in their own repositories on GitHub. For example, the [node debug adapter](https://github.com/microsoft/vscode-node-debug) and the [mono debug adapter](https://github.com/microsoft/vscode-mono-debug) repositories are separate from each other. For a complete list, please visit the [Related Projects](https://github.com/microsoft/vscode/wiki/Related-Projects) page on our [wiki](https://github.com/microsoft/vscode/wiki).## Bundled ExtensionsVS Code includes a set of built-in extensions located in the [extensions](extensions) folder, including grammars and snippets for many languages. Extensions that provide rich language support (code completion, Go to Definition) for a language have the suffix `language-features`. For example, the `json` extension provides coloring for `JSON` and the `json-language-features` extension provides rich language support for `JSON`.## Development ContainerThis repository includes a Visual Studio Code Dev Containers / GitHub Codespaces development container.* For [Dev Containers](https://aka.ms/vscode-remote/download/containers), use the **Dev Containers: Clone Repository in Container Volume...** command which creates a Docker volume for better disk I/O on macOS and Windows.  * If you already have VS Code and Docker installed, you can also click [here](https://vscode.dev/redirect?url=vscode://ms-vscode-remote.remote-containers/cloneInVolume?url=https://github.com/microsoft/vscode) to get started. This will cause VS Code to automatically install the Dev Containers extension if needed, clone the source code into a container volume, and spin up a dev container for use.* For Codespaces, install the [GitHub Codespaces](https://marketplace.visualstudio.com/items?itemName=GitHub.codespaces) extension in VS Code, and use the **Codespaces: Create New Codespace** command.Docker / the Codespace should have at least **4 Cores and 6 GB of RAM (8 GB recommended)** to run full build. See the [development container README](.devcontainer/README.md) for more information.## Code of ConductThis project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/). For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.## LicenseCopyright (c) Microsoft Corporation. All rights reserved.Licensed under the [MIT](LICENSE.txt) license.
