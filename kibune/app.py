from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware


from bus_service import BusService

VEHICLE_URL = "https://api.odpt.org/api/v4/gtfs/realtime/odpt_KyotoBus_AllLines_vehicle?acl:consumerKey=bc7329b88817086c8f5f7e2cbcfc2571a8a68a231f07bf86e5502af7127283c8"

TRIP_UPDATE_URL = "https://api.odpt.org/api/v4/gtfs/realtime/odpt_KyotoBus_AllLines_trip_update?acl:consumerKey=bc7329b88817086c8f5f7e2cbcfc2571a8a68a231f07bf86e5502af7127283c8"

service = BusService(
    VEHICLE_URL,
    TRIP_UPDATE_URL
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# staticフォルダ公開
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def root():

    return FileResponse("static/index.html")


@app.get("/api/buses")
def buses():

    return service.get_buses()