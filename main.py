from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse, PlainTextResponse  # Add PlainTextResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
from fastapi.middleware.cors import CORSMiddleware

# Add this line before defining your FastAPI app

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:8000"],  # Adjust this to match your frontend URL
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)



# Configure Jinja2Templates
templates_dir = os.path.join(os.path.dirname(__file__), "templates")
templates = Jinja2Templates(directory=templates_dir)

# Serve static files from the 'static' directory

static_dir = os.path.join(os.path.dirname(__file__), "static")


app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    # Render HTML template using Jinja
    return templates.TemplateResponse("home.html", {"request": request})

@app.post("/book-shipment/", response_class=PlainTextResponse)
async def book_shipment(request: Request):
    form_data = await request.form()
    for field in form_data.keys():
        print(f"Field: {field}, Value: {form_data[field]}")

    message = f"Your shipment will be collected on {form_data['pickup_date']} at {form_data['pickup_time']} by our delivery executive."
    return message


@app.get("/home", response_class=HTMLResponse)
async def read_home(request: Request):
    # Render HTML template using Jinja
    return templates.TemplateResponse("home.html", {"request": request})

@app.get("/home.html", response_class=HTMLResponse)
async def redirect_about():
    return RedirectResponse(url="/home")  # Redirect to the /about route

@app.get("/about", response_class=HTMLResponse)
async def read_about(request: Request):
    # Render HTML template using Jinja
    return templates.TemplateResponse("about.html", {"request": request})

@app.get("/about.html", response_class=HTMLResponse)
async def redirect_about():
    return RedirectResponse(url="/about")  # Redirect to the /about route


@app.get("/booked", response_class=HTMLResponse)
async def read_contact(request: Request):
    # Render HTML template using Jinja
    return templates.TemplateResponse("booked.html", {"request": request}) 

@app.get("/booked.html", response_class=HTMLResponse)
async def redirect_about():
    return RedirectResponse(url="/booked")  # Redirect to the /about route


@app.get("/bookshipment", response_class=HTMLResponse)
async def read_contact(request: Request):
    # Render HTML template using Jinja
    return templates.TemplateResponse("bookshipment.html", {"request": request}) 

@app.get("/bookshipment.html", response_class=HTMLResponse)
async def redirect_about():
    return RedirectResponse(url="/bookshipment")  # Redirect to the /about route


@app.get("/create_account", response_class=HTMLResponse)
async def read_contact(request: Request):
    # Render HTML template using Jinja
    return templates.TemplateResponse("create_account.html", {"request": request}) 

@app.get("/create_account.html", response_class=HTMLResponse)
async def redirect_about():
    return RedirectResponse(url="/create_account")  # Redirect to the /about route


@app.get("/forgetpwd", response_class=HTMLResponse)
async def read_contact(request: Request):
    # Render HTML template using Jinja
    return templates.TemplateResponse("forgetpwd.html", {"request": request}) 

@app.get("/forgetpwd.html", response_class=HTMLResponse)
async def redirect_about():
    return RedirectResponse(url="/forgetpwd")  # Redirect to the /about route


@app.get("/login", response_class=HTMLResponse)
async def read_contact(request: Request):
    # Render HTML template using Jinja
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/login.html", response_class=HTMLResponse)
async def redirect_about():
    return RedirectResponse(url="/login")  # Redirect to the /about route


@app.get("/profile", response_class=HTMLResponse)
async def read_contact(request: Request):
    # Render HTML template using Jinja
    return templates.TemplateResponse("profile.html", {"request": request}) 

@app.get("/profile.html", response_class=HTMLResponse)
async def redirect_about():
    return RedirectResponse(url="/profile")  # Redirect to the /about route


@app.get("/service", response_class=HTMLResponse)
async def read_contact(request: Request):
    # Render HTML template using Jinja
    return templates.TemplateResponse("service.html", {"request": request}) 

@app.get("/service.html", response_class=HTMLResponse)
async def redirect_about():
    return RedirectResponse(url="/service")  # Redirect to the /about route




@app.get("/trackshipment", response_class=HTMLResponse)
async def read_contact(request: Request):
    # Render HTML template using Jinja
    return templates.TemplateResponse("trackshipment.html", {"request": request}) 

@app.get("/trackshipment.html", response_class=HTMLResponse)
async def redirect_about():
    return RedirectResponse(url="/trackshipment")  # Redirect to the /about route



