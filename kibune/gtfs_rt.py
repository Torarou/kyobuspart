import requests

from proto import gtfs_realtime_pb2


class GTFSRealtime:

    def __init__(self,
                 vehicle_url,
                 trip_update_url):

        self.vehicle_url = vehicle_url

        self.trip_update_url = trip_update_url
    
    def get_vehicle_feed(self):

        response = requests.get(self.vehicle_url)

        response.raise_for_status()

        feed = gtfs_realtime_pb2.FeedMessage()

        feed.ParseFromString(response.content)

        return feed
    
    def get_trip_feed(self):

        response = requests.get(self.trip_update_url)

        response.raise_for_status()

        feed = gtfs_realtime_pb2.FeedMessage()

        feed.ParseFromString(response.content)
        
        return feed
    

    def get_vehicles(self):

        
        vehicle_feed = self.get_vehicle_feed()

        trip_feed = self.get_trip_feed()

        timestamp = trip_feed.header.timestamp

        pattern_map = {}

        for entity in trip_feed.entity:

            if not entity.HasField("trip_update"):
                continue

            tu = entity.trip_update

            pattern_id = None

            if entity.id.startswith("RE_"):

                parts = entity.id.split("_")

                if len(parts) >= 3:

                    pattern_id = f"{parts[1]}_{parts[2]}"

            pattern_map[tu.vehicle.id] = pattern_id

            vehicles = []

        for entity in vehicle_feed.entity:

            if not entity.HasField("vehicle"):
                continue

            vehicle = entity.vehicle

            data = {
                "vehicle_id": vehicle.vehicle.id,
                "trip_id": vehicle.trip.trip_id,
                "lat": vehicle.position.latitude,
                "lon": vehicle.position.longitude,
                "stop_id": vehicle.stop_id,
                "occupancy": vehicle.occupancy_status,
                "current_status": vehicle.current_status,
                "bearing": vehicle.position.bearing,
                "schedule_relationship":vehicle.trip.schedule_relationship,
                "timestamp": timestamp,
                "pattern_id":pattern_map.get(vehicle.vehicle.id)
            }

            vehicles.append(data)

        return {

            "timestamp": timestamp,

            "vehicles": vehicles

        }
