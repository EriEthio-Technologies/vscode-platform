class CodeContext:
    """
    Mock implementation of the CodeContext class.
    """
    def __init__(self, project_id: str = "default_project", language: str = "python"):
        self.project_id = project_id
        self.language = language

    def __repr__(self):
        return f"CodeContext(project_id='{self.project_id}', language='{self.language}')"
