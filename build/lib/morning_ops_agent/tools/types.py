from typing import TypedDict, Optional

class ToolResult(TypedDict):
    ok: bool
    data: Optional[dict]
    error: Optional[str]