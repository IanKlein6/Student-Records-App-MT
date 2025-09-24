# app/schemas/types.py

from typing import Annotated, Optional
from pydantic import EmailStr, StringConstraints
from pydantic.functional_validators import BeforeValidator

Str50 = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=50)]
Str255 = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=255)]

def _normalize_email(v: Optional[str]) -> Optional[str]:
    return v.strip().lower() if isinstance(v, str) else v

NormalizedEmail = Annotated[EmailStr, BeforeValidator(_normalize_email)]
