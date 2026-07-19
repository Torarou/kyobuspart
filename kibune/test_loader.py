from gtfs_loader import GTFSLoader

loader = GTFSLoader()

# 存在する trip_id に置き換えてください
trip_id = "0002_1_0100009891"

route, destination = loader.get_route_and_destination(trip_id)

print("Route:", route)
print("Destination:", destination)

# 存在する stop_id に置き換えてください
stop_id = "6271_1"

print("Stop:", loader.get_stop_name(stop_id))