const map = L.map("map").setView([35.11406751221653, 135.76076912373455], 15);

L.tileLayer(
    "https://tile.openstreetmap.org/{z}/{x}/{y}.png",
    {
        attribution:
            '&copy; OpenStreetMap contributors'
    }
).addTo(map);

const markers = {};

function occupancyColor(status){

    switch(status){

        case 0: // EMPTY
            return "#66CCFF";

        case 1: // MANY_SEATS_AVAILABLE
            return "#00CC00";

        case 3: // STANDING_ROOM_ONLY
            return "#FF9900";

        case 5: // FULL
            return "#FF3333";

        case 7: // NO_DATA_AVAILABLE
            return "#999999";

        default:
            return "#999999";
    }
}

function createIcon(bus){

    const color = occupancyColor(bus.occupancy);
    return L.divIcon({

        className: "",

        html: `
        <div class="bus-label">

            <div class="bus-info">

                <div class="bus-header">

                    <div
                        class="route-box
                        ${bus.route.includes("直行")
                            ? "route-direct"
                            : bus.route.includes("快速")
                                ? "route-rapid"
                                : bus.route.includes("　")
                                ? "route-ko"
                                    : ""}">

                        ${bus.route}

                    </div>

                    <div
                        class="destination-box"

                        style="
                            background:#${bus.route_color || "FFFFFF"};
color:#${bus.route_text_color || "000000"};
                        ">

                        ${bus.destination}

                    </div>

                </div>

                <div class="status-box">

                    ${bus.status}

                </div>

            </div>

            <div class="bus-rotation"
                style="transform: rotate(${bus.bearing}deg);">

                <div class="bus-arrow"
                    style="border-bottom-color:${color};">
                </div>

                <div class="bus-marker"
                    style="background:${color};">
                    ${bus.vehicle_id}
                </div>

            </div>

        </div>
        `,

        iconSize:[120,70],
        iconAnchor:[60,35]

    });

}

async function updateBus(){

    const response = await fetch("/api/buses");

    const json = await response.json();

    const buses = json.vehicles;

    const alive = new Set();

    buses.forEach(bus=>{

        alive.add(bus.vehicle_id);

        if(markers[bus.vehicle_id]){

            markers[bus.vehicle_id]
                .setLatLng([bus.lat,bus.lon]);

            markers[bus.vehicle_id]
                .setIcon(createIcon(bus));

        }

        else{

            markers[bus.vehicle_id]=L.marker(

                [bus.lat,bus.lon],

                {

                    icon:createIcon(bus)

                }

            ).addTo(map);

        }

    });

    Object.keys(markers).forEach(id=>{

        if(!alive.has(id)){

            map.removeLayer(markers[id]);

            delete markers[id];

        }

    });

    const date = new Date(json.timestamp * 1000).toLocaleTimeString("ja-JP");

        document.getElementById("timestamp").textContent =
    "更新: " + date;

}

updateBus();

setInterval(updateBus,15000);