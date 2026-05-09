from pydantic import BaseModel
from typing import Optional, List, Dict, Any, Union


class ExceptionModel(BaseModel):
    status: int
    message: str
    detail: Optional[Union[Dict[str, Any], List[Any], str]] = None
