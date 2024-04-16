from typing import List

from pydantic import BaseModel


class CheckPasswordStrengthResponse(BaseModel):
    """
    Provides an assessment of the password's strength and suggestions for improvement.
    """

    strength: str
    suggestions: List[str]


def check_password_strength(password: str) -> CheckPasswordStrengthResponse:
    """
    Assesses the strength of a given password and provides suggestions for improvement.

    Args:
        password (str): The password to be analyzed for strength.

    Returns:
        CheckPasswordStrengthResponse: Provides an assessment of the password's strength and suggestions for improvement.
    """
    min_length = 8
    has_uppercase = any((c.isupper() for c in password))
    has_lowercase = any((c.islower() for c in password))
    has_digit = any((c.isdigit() for c in password))
    has_special_char = any((not c.isalnum() for c in password))
    strength = "weak"
    suggestions = []
    if (
        len(password) >= min_length
        and has_uppercase
        and has_lowercase
        and has_digit
        and has_special_char
    ):
        strength = "strong"
    elif len(password) >= min_length and (has_uppercase or has_lowercase) and has_digit:
        strength = "fair"
    else:
        strength = "weak"
        if len(password) < min_length:
            suggestions.append(
                f"Increase password length to at least {min_length} characters."
            )
        if not has_uppercase:
            suggestions.append("Include at least one uppercase letter.")
        if not has_lowercase:
            suggestions.append("Include at least one lowercase letter.")
        if not has_digit:
            suggestions.append("Include at least one digit.")
        if not has_special_char:
            suggestions.append("Include at least one special character.")
    return CheckPasswordStrengthResponse(strength=strength, suggestions=suggestions)
