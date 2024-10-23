import React, { useState, useEffect } from "react";
import dayjs from "dayjs";
import relativeTime from "dayjs/plugin/relativeTime";
import utc from "dayjs/plugin/utc";
import { MapContainer, TileLayer, Marker, useMapEvents, useMap } from "react-leaflet";

dayjs.extend(relativeTime);
dayjs.extend(utc);

var first = false

export default function App() {
    const [locationsState, setLocationsState] = useState([])
    
    function GetLocations(bounds) {
        let ignoreStaleRequest = false;
        fetch("/api/location/list/?latmin=" + bounds._southWest.lat.toString()
              + "&latmax=" + bounds._northEast.lat.toString()
              + "&longmin=" + bounds._southWest.lng.toString()
              + "&longmax=" + bounds._northEast.lng.toString(), {
            method: "GET",
            headers: {
                Accept: "application/json",
                "Content-Type": "application/json",
            },
            credentials: "same-origin"
        })
        .then((response) => {
            if (!response.ok) throw Error(response.statusText);
            return response.json();
        })
        .then((data) => {
            if (!ignoreStaleRequest) {
                // this had was data?.status_code before
                if (data.status_code === undefined) {
                    setLocationsState(data.locations);
                }
            }
        })
        .catch((error) => console.log(error));

        return () => {
            ignoreStaleRequest = true;
        };
    }
    
    function FirstBounds() {
        if(!first){
            console.log("first")
            first = true
            const map = useMap()
            GetLocations(map.getBounds())
        }
        return null
    }
    
    function MapEvents() {
        console.log("move")
        const map = useMapEvents({
            moveend: () => GetLocations(map.getBounds()),
            zoomend: () => GetLocations(map.getBounds())
        });
        return null;
    }
    return (
        <MapContainer
          center={[42.27976830712081, -83.74467699423975]}
          zoom={13}
          doubleClickZoom={false}
        >
            <FirstBounds />
            <MapEvents />
            <TileLayer
                attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            />
        </MapContainer>
    );
}