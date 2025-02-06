import tiktoken
import subprocess
import logging
import re

def encode(text: str) -> list[int]:
    """
    Encodes a string of text into tokens using the tiktoken library.
    """
    logging.info(f"Encoding text: {text[:50]}...")
    enc = tiktoken.get_encoding("cl100k_base")
    return enc.encode(text)

def calculate_cyclomatic_complexity(code: str) -> int:
    """
    Calculates the cyclomatic complexity of a given code snippet.
    """
    logging.info("Calculating cyclomatic complexity...")
    try:
        # Save the code to a temporary file
        with open("temp_code.py", "w") as f:
            f.write(code)

        # Run lizard command on the temporary file
        result = subprocess.run(["lizard", "temp_code.py"], capture_output=True, text=True)

        # Extract the complexity value from the output
        output_lines = result.stdout.splitlines()
        if len(output_lines) > 1:
            complexity = int(output_lines[1].split()[2])
        else:
            complexity = 1  # Default value if parsing fails

        logging.info(f"Cyclomatic complexity: {complexity}")
        return complexity
    except Exception as e:
        logging.error(f"Error calculating cyclomatic complexity: {e}", exc_info=True)
        return 1

def sanitize(code: str) -> str:
    """
    Sanitizes a given code snippet by removing potentially harmful or unwanted content.
    """
    logging.info("Sanitizing code...")
    try:
        # Remove any comments
        code = re.sub(r"#.*", "", code)

        # Remove any docstrings
        code = re.sub(r"\"\"\"[\s\S]*?\"\"\"", "", code)
        code = re.sub(r"\'\'\'[\s\S]*?\'\'\'", "", code)

        # Remove any blank lines
        code = "\n".join([line for line in code.splitlines() if line.strip()])

        logging.info("Code sanitized successfully.")
        return code
    except Exception as e:
        logging.error(f"Error sanitizing code: {e}", exc_info=True)
        return code
