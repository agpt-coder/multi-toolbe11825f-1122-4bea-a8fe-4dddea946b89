from typing import Optional

from email_validator import EmailNotValidError
from email_validator import validate_email as external_validate_email
from pydantic import BaseModel


class ValidateEmailResponse(BaseModel):
    """
    Provides the result of the email validation process, including a validity flag and suggestions or errors if any.
    """

    is_valid: bool
    suggestions: Optional[str] = None
    errors: Optional[str] = None


def validate_email(email: str) -> ValidateEmailResponse:
    """
    Validates an email address for proper format and potential deliverability issues.

    Args:
        email (str): The email address to be validated.

    Returns:
        ValidateEmailResponse: Provides the result of the email validation process, including a validity flag and suggestions or errors if any.

    Example:
        To validate a valid email:
        > result = validate_email('example@example.com')
        > print(result.is_valid, result.suggestions, result.errors)
        > True, None, None

        To validate an invalid email:
        > result = validate_email('invalid-email')
        > print(result.is_valid, result.suggestions, result.errors)
        > False, None, 'The email address is not valid according to the user's email domain's DNS records.'
    """
    try:
        result = external_validate_email(email)
        return ValidateEmailResponse(is_valid=True)
    except EmailNotValidError as e:
        error_message = str(e)
        suggestions = None
        if "suggestion" in e.args[0]:
            suggestions = e.args[0]["suggestion"]
        return ValidateEmailResponse(
            is_valid=False, suggestions=suggestions, errors=error_message
        )
