from typing import Annotated

from pydantic import StringConstraints

# Non-blank text: strip surrounding whitespace, then require >= 1 char so that
# both "" and whitespace-only "   " are rejected. Per-field max_length stays on
# the field's Field(...).
NonBlankStr = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]
