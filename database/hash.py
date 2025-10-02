# hash.py
import bcrypt


def hash_password(password: str) -> str:
    """
    Hash a password with a custom salt using bcrypt.

    Args:
        password (str): The plain password.
    Returns:
        str: Hashed password (utf-8 string) to store in database.
    """
    # Combine password and custom salt
    # encode("utf-8") is a Python string method that converts a string into bytes using the UTF-8 encoding.
    # Hash with bcrypt
    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    return hashed.decode("utf-8")


def verify_password(password: str, hashed_password: str) -> bool:
    """
    Verify if a password matches the hashed password using the same salt.

    Args:
        password (str): Password entered by user.
        hashed_password (str): Hashed password stored in database.

    Returns:
        bool: True if password matches, False otherwise.
    """
    password_with_salt = (password).encode("utf-8")
    return bcrypt.checkpw(password_with_salt, hashed_password.encode("utf-8"))
