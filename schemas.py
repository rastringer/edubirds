from pydantic import BaseModel
from typing import Optional

class CourseCreate(BaseModel):
    title: str
    institution: str 
    description: Optional[str] = ""  # Keep it optional to save bandwidth if not needed


class CourseResponse(CourseCreate):
    id: str 
    title: str
    institution: str
    created: str
    
    class Config:
        from_attributes = True  # Allows returning dicts or ORM models directly

class MaterialCreate(BaseModel):
    course_id: str
    title: str
    content_type: str # 'text' or 'video', 'audio' etc

class MaterialResponse(MaterialCreate):
    id: str
    size_kb: int
