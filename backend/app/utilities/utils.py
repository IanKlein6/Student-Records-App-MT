# app/utilities/utils.py

"""File Doc: Small helper utilities.
The place for utility functions to be localized, that help abstract repetitive jobs.

Utilities:
    Str50 = checks that a string has a length of max 50, min length of 1, and strips all white spaces.
    Str225 = checks that a string has a length of max 255, min length of 1, and strips all white spaces.
    _normalize_email = function to normalized all emails, converts all chars to lowercase, and strips white spaces

"""

from typing import Annotated, Optional
from pydantic import EmailStr, StringConstraints
from pydantic.functional_validators import BeforeValidator

Str50 = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=50)]
"""String length max 50.

Checks that a string has a length of max 50, min length of 1, and strips all white spaces.
"""

Str255 = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=255)]
"""String length max 255.

Checks that a string has a length of max 255, min length of 1, and strips all white spaces.
"""

## Maybe add domain enforcement to email?? 
def _normalize_email(v: Optional[str]) -> Optional[str]:
    """Normalize email string to lowercase and trim whitespaces."""
    return v.strip().lower() if isinstance(v, str) else v

NormalizedEmail = Annotated[EmailStr, BeforeValidator(_normalize_email)]
"""EmailStr that is automatically normalized using _normalize_email."""