@app.get("/api/buses")
def get_buses():

    buses = service.get_buses()

    result = []

    for bus in buses:

        bus["color"] = occupancy_color(
            bus["occupancy"]
        )

        result.append(bus)

    return result