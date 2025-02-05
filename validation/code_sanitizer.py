# ai-service/validation/code_sanitizer.py
import semgrep

class CodeSanitizer:
    def __init__(self):
        self.semgrep = semgrep

    def sanitize(self, code: str) -> bool:
        """Check for security vulnerabilities."""
        results = self.semgrep.scan(code)
        return len(results) == 0  # Return True if no issues found
