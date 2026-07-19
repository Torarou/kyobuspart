from proto import gtfs_realtime_pb2


def status_text(loader, trip_id, stop_id, current_status):

    if not stop_id:
        return ""

    stop_name = loader.get_stop_name(stop_id)

    if current_status == gtfs_realtime_pb2.VehiclePosition.INCOMING_AT:
        return f"次は {stop_name}"

    elif current_status == gtfs_realtime_pb2.VehiclePosition.STOPPED_AT:
        return f"{stop_name} 停車中"

    elif current_status == gtfs_realtime_pb2.VehiclePosition.IN_TRANSIT_TO:
        previous = loader.get_previous_stop(trip_id, stop_id)
        return f"{previous} 発車"

    return ""