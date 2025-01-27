from fastapi import FastAPI, Request, Body
from fastapi.responses import HTMLResponse, RedirectResponse, PlainTextResponse  # Add PlainTextResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
from fastapi.middleware.cors import CORSMiddleware
from fastapi import HTTPException
from app.model.generateid import generate_id
from app.model.crud import insert_values,delete_record,read_table,update_records, read_specific_column
from pydantic import BaseModel
from typing import Optional
from fastapi import Form

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
    courier_id = generate_id("CO",4)
    print(courier_id)
    for field in form_data.keys():
        print(f"Field: {field}, Value: {form_data[field]}")
   
    insert_values("PACKAGE",[courier_id,"C001",form_data["home_city"],form_data["delivery_city"],form_data["description"],form_data["weight"],form_data["dimensions"],"I"])
    print("Inserted")
    read_table("PACKAGE")
    message = f"Your shipment will be collected on {form_data['pickup_date']} at {form_data['pickup_time']} by our delivery executive."
    return message

@app.get("/trackshipment", response_class=HTMLResponse)
async def read_contact(request: Request):
    # Debugging: Print rows to check if it's None or contains data
    rows = read_specific_column("Package", "Customer_ID", "C001", ["Courier_ID" ,"Origin","Destination" ,"Description" ,"Weight","Dimensions" ,"Courier_Status"])
    print("Rows:", rows)  # Debugging: Print rows
    if rows is None:
        rows = []  # Provide a default empty list if rows is None
        print(rows)
    return templates.TemplateResponse("trackshipment.html", {"request": request, "rows": rows})

class CourierIdRequest(BaseModel):
    courierId: str

@app.post("/deleteShipment")
async def delete_shipment(request: Request, request_body: CourierIdRequest = Body(...)):
    courier_id = request_body.courierId
    delete_record("Package", f"Courier_ID = '{courier_id}'")
    return {"message": "Shipment canceled successfully."}


@app.get("/cancelshipment", response_class=HTMLResponse)
async def read_cancel(request: Request):
    # Debugging: Print rows to check if it's None or contains data
    rows = read_specific_column("Package", "Customer_ID", "C001", ["Courier_ID" ,"Origin","Destination" ,"Description" ,"Weight","Dimensions" ,"Courier_Status"])
    print("Rows:", rows)  # Debugging: Print rows
    if rows is None:
        rows = []  # Provide a default empty list if rows is None
        print(rows)
    return templates.TemplateResponse("cancelshipment.html", {"request": request, "rows": rows})


@app.post("/updateShipment")
async def update_shipment(request: Request, request_body: CourierIdRequest = Body(...)):
    courier_id = request_body.courierId
    print("Courier ID:", courier_id)
    # Add your logic here for updating the shipment
    return {"message": "Shipment updated successfully."}

@app.get("/updateshipment", response_class=HTMLResponse)
async def read_update(request: Request):
    # Assume this function returns rows from the database
    rows = read_specific_column("Package", "Customer_ID", "C001",
                                ["Courier_ID", "Origin", "Destination", "Description", "Weight", "Dimensions",
                                 "Courier_Status"])
    print("Rows:", rows)
    if rows is None:
        rows = []
        print(rows)
    return templates.TemplateResponse("updateshipment.html", {"request": request, "rows": rows})

@app.get("/updaterecord", response_class=HTMLResponse)
async def update_record(request: Request, courier_id: Optional[str] = None):
    # Check if courier ID is provided
    if courier_id is None:
        print("NO COURIER ID")
        # Raise HTTPException with 400 status code for bad request
        raise HTTPException(status_code=400, detail="Courier ID is missing")

    # Fetch row data based on the courier ID
    row_data = read_specific_column("Package", "Courier_ID", courier_id,
                                ["Origin", "Destination", "Description", "Weight", "Dimensions",
                                 "Courier_Status"])
    print(courier_id)
    print("data to be uploaded")
    print(row_data)
    if row_data is None:
        # Handle the case where no row data is found
        raise HTTPException(status_code=404, detail="Row data not found")

    return templates.TemplateResponse("updaterecord.html", {"request": request, "row_data": row_data})

@app.post("/toupdateShipment", response_class=HTMLResponse)
async def to_update_shipment(request: Request):
    form_data = await request.form()

    # Print field-value pairs
    for field in form_data.keys():
        print(f"Field: {field}, Value: {form_data[field]}")

    print("DONE")

    # Convert form data keys to a list
    fields_list = list(form_data.keys())

    # Construct a dictionary with field-value pairs
    update_values = {field: form_data[field] for field in fields_list}
    print(update_values)

    # Update the record
    update_records("Package", update_values, "Courier_ID = :courier_id", 'CO2086')

    print("Updated")
  
    html_content = """
    <html>
    <head>
        <title>Shipment Update</title>
    </head>
    <body>
        <h1>Shipment updated successfully</h1>
        <p>Thank you for updating the shipment.</p>
    </body>
    </html>
    """
    return html_content
    





@app.get("/updaterecord.html", response_class=HTMLResponse)
async def redirect_to_update_record():
    return RedirectResponse(url="/updaterecord?courier_id=CO2086")

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
async def redirect_service():
    return RedirectResponse(url="/service")  # Redirect to the /about route


@app.get("/trackshipment.html", response_class=HTMLResponse)
async def redirect_track():
    return RedirectResponse(url="/trackshipment")  


@app.get("/cancelshipment.html", response_class=HTMLResponse)
async def redirect_cancel():
    return RedirectResponse(url="/cancelshipment")  

@app.get("/updateshipment.html", response_class=HTMLResponse)
async def read_update():
    return RedirectResponse(url="/updateshipment")  

@app.get("/updaterecord.html", response_class=HTMLResponse)
async def read_update_record():
    return RedirectResponse(url="/updaterecord")  




