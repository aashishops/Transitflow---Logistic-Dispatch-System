from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os

app = FastAPI()

# Configure Jinja2Templates
templates_dir = os.path.join(os.path.dirname(__file__), "templates")
templates = Jinja2Templates(directory=templates_dir)

# Serve static files from the 'static' directory

static_dir = os.path.join(os.path.dirname(__file__), "static")
print("LOL"*10)
print(static_dir)

app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    # Render HTML template using Jinja
    return templates.TemplateResponse("home.html", {"request": request})

@app.get("/about", response_class=HTMLResponse)
async def read_about(request: Request):
    # Render HTML template using Jinja
    return templates.TemplateResponse("about.html", {"request": request})
