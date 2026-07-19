import pandas as pd


class GTFSLoader:

    def __init__(self, gtfs_folder="gtfs"):

        self.stop_times = pd.read_csv(f"{gtfs_folder}/stop_times.txt", encoding="utf-8-sig")
        self.stops = pd.read_csv(f"{gtfs_folder}/stops.txt", encoding="utf-8-sig")
        self.routes = pd.read_csv(f"{gtfs_folder}/routes.txt", encoding="utf-8-sig")
        self.trips = pd.read_csv(f"{gtfs_folder}/trips.txt", encoding="utf-8-sig")

        self.stop_dict = dict(
            zip(self.stops["stop_id"], self.stops["stop_name"])
        )
        self.pattern_dict = {}

        for _, row in self.trips.iterrows():

            pattern = str(row["jp_pattern_id"])

            if pattern != "" and not pattern != pattern:

                self.pattern_dict[pattern] = row["trip_id"]

        for _, row in self.routes.iterrows():

            self.route_dict = {}

            for row in self.routes:
                self.route_dict[row["route_id"]] = {
                    "route_short_name": row["route_short_name"],
                    "route_long_name": row["route_long_name"],
                }

            self.route_dict[row["route_id"]] = {

                "route_short_name": row["route_short_name"],

                "route_color": row.get("route_color", "FFFFFF"),

                "route_text_color": row.get("route_text_color", "000000")

            }

        self.trip_dict = {}

        self.stop_sequence = {}

        grouped = self.stop_times.sort_values(
            "stop_sequence"
        ).groupby("trip_id")

        for trip_id, group in grouped:

            self.stop_sequence[trip_id] = list(
                group["stop_id"]
            )

        for _, row in self.trips.iterrows():

            self.trip_dict[row["trip_id"]] = {
                "route_id": row["route_id"],
                "headsign": row["trip_headsign"]
            }

        print("GTFS Static Loaded")

    def get_stop_name(self, stop_id):

        return self.stop_dict.get(stop_id, "")

    def get_route_name(self, route_id):

        return self.route_dict.get(route_id, "")

    def get_trip_info(self, trip_id):

        return self.trip_dict.get(trip_id, None)

    def get_route_and_destination(self, trip_id):

        trip = self.get_trip_info(trip_id)

        if trip is None:
            return "", "", "FFFFFF", "000000"
        
        route_id = trip["route_id"]

        route_info = self.route_dict[route_id]

        route = route_info["route_short_name"]

        destination = trip["headsign"]

        if "(" in destination:
            destination = destination.split("(")[0].strip()

        if "（" in destination:
            destination = destination.split("（")[0].strip()
        
        return (
            route,
            destination,
            route_info["route_color"],
            route_info["route_text_color"]
        )
    
    def get_trip_from_pattern(self, pattern_id):

        return self.pattern_dict.get(pattern_id)

    def get_previous_stop(self, trip_id, stop_id):

        stops = self.stop_sequence.get(trip_id)

        if stops is None:
            return ""

        try:

            index = stops.index(stop_id)

        except ValueError:

            return ""

        if index == 0:

            return ""

        previous_stop = stops[index - 1]

        return self.get_stop_name(previous_stop)
    