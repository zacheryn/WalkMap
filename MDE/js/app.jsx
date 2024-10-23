import React, { useState, useEffect } from "react";
import dayjs from "dayjs";
import relativeTime from "dayjs/plugin/relativeTime";
import utc from "dayjs/plugin/utc";
import { MapContainer, TileLayer, Marker, useMapEvents } from "react-leaflet";

dayjs.extend(relativeTime);
dayjs.extend(utc);

function makeACall(bounds, zoom) {
    console.log(`Current map zoom is ${zoom}`);
    
    console.log("make a call to the server with the bounds:", bounds);
}

const MapEvents = () => {
    const map = useMapEvents({
        moveend: () => makeACall(map.getBounds(), map.getZoom()),
        zoomend: () => makeACall(map.getBounds(), map.getZoom())
    });
    return null;
}

export default function App() {
    return (
        <MapContainer center={[42.27976830712081, -83.74467699423975]} zoom={13} doubleClickZoom={false}>
            <MapEvents />
            <TileLayer
                attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            />
        </MapContainer>
    );
}