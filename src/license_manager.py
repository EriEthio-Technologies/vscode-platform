import hashlib
import uuid
import datetime

class LicenseManager:
    def __init__(self, secret_key: str):
        self.secret_key = secret_key

    def generate_license_key(self, user_id: str, expiration_date: str, usage_limit: int) -> str:
        """
        Generates a license key for a given user ID with an expiration date and usage limit.

        Args:
            user_id (str): The user ID for which to generate the license key.
            expiration_date (str): The expiration date of the license key in YYYY-MM-DD format.
            usage_limit (int): The usage limit for the license key.

        Returns:
            str: The generated license key.
        """
        raw_key = f"{user_id}:{self.secret_key}:{expiration_date}:{usage_limit}:{uuid.uuid4()}"
        license_key = hashlib.sha256(raw_key.encode()).hexdigest()
        return license_key

    def validate_license_key(self, user_id: str, license_key: str, current_date: str, usage_count: int) -> bool:
        """
        Validates a given license key for a user ID with the current date and usage count.

        Args:
            user_id (str): The user ID to validate.
            license_key (str): The license key to validate.
            current_date (str): The current date in YYYY-MM-DD format.
            usage_count (int): The current usage count.

        Returns:
            bool: True if the license key is valid, False otherwise.
        """
        expiration_date = datetime.datetime.strptime(current_date, "%Y-%m-%d").date()
        if usage_count > usage_limit or expiration_date > datetime.datetime.strptime(expiration_date, "%Y-%m-%d").date():
            return False

        expected_key = self.generate_license_key(user_id, expiration_date, usage_limit)
        return expected_key == license_key

# Example usage
if __name__ == "__main__":
    secret_key = "your_secret_key"
    user_id = "user123"
    expiration_date = "2023-12-31"
    usage_limit = 100
    current_date = "2023-01-01"
    usage_count = 10

    license_manager = LicenseManager(secret_key)

    # Generate a license key
    license_key = license_manager.generate_license_key(user_id, expiration_date, usage_limit)
    print(f"Generated License Key: {license_key}")


    # Validate the license key
    is_valid = license_manager.validate_license_key(user_id, license_key, current_date, usage_count)
    print(f"Is License Key Valid? {is_valid}")

