from bus_service import BusService

URL = "https://api.odpt.org/api/v4/gtfs/realtime/odpt_KyotoBus_AllLines_vehicle?acl:consumerKey=bc7329b88817086c8f5f7e2cbcfc2571a8a68a231f07bf86e5502af7127283c8"

service = BusService(URL)

buses = service.get_buses()

print("取得:", len(buses))

for bus in buses[:5]:

    print(bus)