from gtfs_rt import GTFSRealtime

URL = "https://api.odpt.org/api/v4/gtfs/realtime/odpt_KyotoBus_AllLines_vehicle?acl:consumerKey=bc7329b88817086c8f5f7e2cbcfc2571a8a68a231f07bf86e5502af7127283c8"

rt = GTFSRealtime(URL)

vehicles = rt.get_vehicles()

print("取得台数:", len(vehicles))

for vehicle in vehicles[:10]:
    print(vehicle)