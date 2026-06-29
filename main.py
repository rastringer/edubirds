from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse 
from routes.courses import router as courses_router
from config import settings
from models import Course 

app = FastAPI(
        title="Edubirds API",
        version="0.1.0",
        docs_url=None, # disable docs for smaller payload 
    )

app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(courses_router) 



@app.get("/health")
async def health():
    return {"status" : "ok"}

@app.get("/", response_class=HTMLResponse)
async def root():
    """
    Serves a minimal HTML form for institutions to add courses.
    Optimized: Inline CSS/JS to avoid extra HTTP requests.
    """
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Add Course - Low Bandwidth</title>
        <style>
            body { font-family: sans-serif; max-width: 600px; margin: 2rem auto; padding: 1rem; line-height: 1.5; }
            h1 { font-size: 1.5rem; color: #333; }
            label { display: block; margin-top: 1rem; font-weight: bold; }
            input, textarea { width: 100%; padding: 0.5rem; margin-top: 0.25rem; border: 1px solid #ccc; border-radius: 4px; }
            button { background-color: #2ecc71; color: white; border: none; padding: 0.75rem 1.5rem; 
                     margin-top: 1.5rem; cursor: pointer; border-radius: 4px; font-size: 1rem; }
            button:hover { background-color: #27ae60; }
            #status { margin-top: 1rem; padding: 0.5rem; border-radius: 4px; display: none; }
            .success { background-color: #d4edda; color: #155724; }
            .error { background-color: #f8d7da; color: #721c24; }
            
            /* Critical for low bandwidth: Prevent layout shifts */
            .hidden { display: none; }
        </style>
    </head>
    <body>
        <h1>New Course Registration</h1>
        <form id="courseForm">
            <label for="institution">Institution Name:</label>
            <input type="text" id="institution" name="institution" required placeholder="e.g. Gaza Education Hub">

            <label for="title">Course Title:</label>
            <input type="text" id="title" name="title" required placeholder="e.g. Intro to Biology">

            <label for="description">Short Description (Optional):</label>
            <textarea id="description" name="description" rows="3"></textarea>

            <button type="submit" id="submitBtn">Create Course</button>
        </form>

        <div id="status"></div>

        <script>
            document.getElementById('courseForm').addEventListener('submit', async function(e) {
                e.preventDefault();
                
                const btn = document.getElementById('submitBtn');
                const statusDiv = document.getElementById('status');
                const originalText = btn.innerText;

                // Disable button to prevent double submission on slow connections
                btn.disabled = true;
                btn.innerText = 'Sending...';
                statusDiv.style.display = 'none';

                const payload = {
                    institution: document.getElementById('institution').value.trim(),
                    title: document.getElementById('title').value.trim(),
                    description: document.getElementById('description').value.trim()
                };

                try {
                    const response = await fetch('/admin/courses', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify(payload)
                    });

                    if (response.ok) {
                        const data = await response.json();
                        statusDiv.innerHTML = '<strong>Success!</strong> Course ID: ' + data.id;
                        statusDiv.className = 'success';
                        statusDiv.style.display = 'block';
                        document.getElementById('courseForm').reset();
                    } else {
                        const errorData = await response.json();
                        throw new Error(errorData.detail || 'Unknown error');
                    }
                } catch (error) {
                    statusDiv.innerHTML = '<strong>Error:</strong> ' + error.message;
                    statusDiv.className = 'error';
                    statusDiv.style.display = 'block';
                } finally {
                    btn.disabled = false;
                    btn.innerText = originalText;
                }
            });
        </script>
    </body>
    </html>
    """