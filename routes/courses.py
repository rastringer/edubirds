from fastapi import APIRouter, Query
from models import COURSE_DB
from schemas import CourseCreate
from uuid import uuid4
from datetime import datetime

router = APIRouter() 

@router.get("/courses", response_model=list[dict])
async def list_courses(institution: str | None = None):
    """Lightweight listing, no descriptions yet, just IDs / titles"""
    result = COURSE_DB["courses"]
    if institution:
        result = [c for c in result if c.get("institution") == institution]
    
    return [{"id": c["id"], "title": c["title"]} for c in result]

@router.get("/courses/{course_id}/materials")
async def get_course_materials(course_id: str, 
                               video_quality: str = Query(default="low", pattern="^(low|high)$")):
    """Prioritizes text first, offers quality tiers for video"""
    materials = COURSE_DB["materials"].get(course_id, [])

    # Filter to appropriate video quality when applicable
    filtered = []
    for m in materials:
        if m["content_type"] == "text":
            filtered.append(m) 
        elif m["content_type"] == "video" and m.get(f"url_{video_quality}"):
            filtered.append({**m, "url": m[f"url_{video_quality}"]})

    return {"course_id": course_id, "materials": filtered}

@router.post("/admin/courses", response_model=dict, status_code=201)
async def create_course(course_data: CourseCreate):
    """
    Admin endpoint: Institutions add courses.
    
    - Validates input automatically (raises 422 if title/institution missing)
    - Prevents empty strings via Pydantic validators if configured
    - Returns clean JSON with ID for frontend routing
    """
    course_id = str(uuid4())
    created_at = datetime.utcnow().isoformat()

    # Build the course object
    new_course = {
        "id": course_id,
        "title": course_data.title,
        "institution": course_data.institution,
        "created": created_at,
        # Add optional description if your schema has it
        "description": getattr(course_data, 'description', "") 
    }

    # Save to DB
    COURSE_DB["courses"].append(new_course)

    return {
        "status": "created", 
        "id": course_id,
        "message": f"Course '{course_data.title}' added for {course_data.institution}"
    }

@router.post("/admin/materials")
async def add_material(data: dict):
    """Admin endpoint - add course content"""
    material = {
        "id": str(uuid4()),
        "course_id": data["course_id"],
        "title": data["title"],
        "content_type": data["content_type"],
        "size_kb": len(data.get("content_text", "").encode()) // 1024,
    }
    if data["content_type"] == "text":
        material["content_text"] = data.get("content_text", "")
    else:
        material["url"] = data.get("content_url", "")

    if material["course_id"] not in COURSE_DB["materials"]:
        COURSE_DB["materials"][material["course_id"]] = []
    COURSE_DB["materials"][material["course_id"]].append(material)

    return {"status": "added", "material_id": material["id"]}
