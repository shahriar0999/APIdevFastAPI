from pydantic import BaseModel
from typing import Optional

class Feature(BaseModel):
    location: str
    area: str
    bedroom: int
    bathroom: int
    sqrtFeet: int

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    ratings: Optional[float] = None
