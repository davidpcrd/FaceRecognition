from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Union

class Vector(BaseModel):
    vector: List[float] = Field(..., min_items=128, max_items=128)

class _face(BaseModel):
    x: int
    y: int
    w: int
    h: int

class _name_dist(BaseModel):
    name: str
    distance: float

class Result(BaseModel):
    name: str
    distance: float
    chrono: float
    others: Dict[int, _name_dist]
    face: Optional[_face]

class Results(BaseModel):
    results : List[Result]