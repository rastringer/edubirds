
from datetime import datetime
from typing import Optional

# Need database for prod, JSON will do for now
COURSE_DB = {
        "courses": [],
        "materials": {}  # course_id -> [materials]
        }

class Course:
    def __init__(self, id: str, title: str, institution: str, created: datetime = None):
        self.id = id
        self.title = title
        self.institution = institution
        self.created = created or datetime.utcnow()

class Material:
    def __init__(self, id: str, course_id: str, title: str, content_type: str,
                 content_url: str = "", content_text: str = "", size_kb: int = 0):
        """content_type: 'text' | 'video_low' | 'video_high'"""
        self.id = id
        self.course_id = course_id
        self.title = title
        self.content_type = content_type
        self.content_url = content_url
        self.content_text = content_text  # For text-only fallback
        self.size_kb = size_kb
