from typing import TypedDict, Optional

class ToolResult(TypedDict):
    ok: bool
    data: Optional[str]
    error: Optional[str]
