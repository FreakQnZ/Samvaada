from pydantic import BaseModel
from typing import List, Optional

class AskRequest(BaseModel):
    user_input: str
    messages: Optional[List[str]] = []
