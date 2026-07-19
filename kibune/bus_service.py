from gtfs_loader import GTFSLoader
from gtfs_rt import GTFSRealtime
from status import status_text


class BusService:

    def __init__(self,
             vehicle_url,
             trip_update_url):

        self.loader = GTFSLoader()

        self.rt = GTFSRealtime(
            vehicle_url,
            trip_update_url
        )

    def get_buses(self):

        result = self.rt.get_vehicles()

        vehicles = result["vehicles"]

        timestamp = result["timestamp"]

        buses = []

        for vehicle in vehicles:

            MIN_LAT = 35.0849952915226 
            MAX_LAT = 35.12747656307029

            MIN_LON = 135.75295853107568
            MAX_LON = 135.78188347291538

            lat = vehicle["lat"]
            lon = vehicle["lon"]

            #if not (MIN_LAT <= lat <= MAX_LAT and
            #        MIN_LON <= lon <= MAX_LON):
            #    continue

            if vehicle["schedule_relationship"] == "ADDED":

                trip_id = self.loader.get_trip_from_pattern(
                    vehicle["pattern_id"]
                )

            else:

                trip_id = vehicle["trip_id"]

            route,\
            destination,\
            route_color,\
            route_text_color = \
                self.loader.get_route_and_destination(
                    trip_id
                )
            

            stop = self.loader.get_stop_name(
                vehicle["stop_id"]
            )

            status = status_text(
                self.loader,
                vehicle["trip_id"],
                vehicle["stop_id"],
                vehicle["current_status"]
            )

            buses.append({

                "vehicle_id": vehicle["vehicle_id"],

                "route": route,

                "destination": destination,

                "stop": stop,

                "status": status,

                "lat": vehicle["lat"],

                "lon": vehicle["lon"],

                "occupancy": vehicle["occupancy"],

                "bearing": vehicle["bearing"],

                "route_color": route_color,

                "route_text_color": route_text_color

            })

        return {

            "timestamp": timestamp,

            "vehicles": buses

        }