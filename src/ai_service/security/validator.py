# src/ai_service/security/validator.py
# Copyright (c) 2023 Your Company. All rights reserved.

class CodeValidator:
    def __init__(self):
        self.semgrep = SemgrepEngine()
        self.license_check = LicenseCompliance()

    def validate(self, code: str) -> bool:
        return (
            self.semgrep.scan(code).safe and
            self.license_check.verify(code)
        )

def validate_input(data: dict) -> bool:
    """
    Validate the input data.

    Args:
        data (dict): The input data to validate.

    Returns:
        bool: True if the input is valid, False otherwise.
    """
    if "name" in data and "email" in data:
        return True
    return False
