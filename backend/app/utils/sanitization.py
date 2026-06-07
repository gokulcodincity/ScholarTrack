import html
from typing import Annotated
from pydantic import AfterValidator

def sanitize_text(v: str) -> str:
    if isinstance(v, str):
        return html.escape(v.strip())
    return v

SanitizedStr = Annotated[str, AfterValidator(sanitize_text)]
