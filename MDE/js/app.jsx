import React, { useState, useEffect } from "react";
import dayjs from "dayjs";
import relativeTime from "dayjs/plugin/relativeTime";
import utc from "dayjs/plugin/utc";
import { MapContainer, TileLayer, Marker, useMapEvents, useMap, Popup } from "react-leaflet";
import { Icon } from "leaflet"
import { use } from "chai";

dayjs.extend(relativeTime);
dayjs.extend(utc);

var first = false

export default function App() {
    // States
    const [locationsState, setLocationsState] = useState([]);

    // The icon for markers
    const customIcon = new Icon({
        iconUrl: "./../static/images/marker.png",
        iconSize: [38, 38]
    })

    function GetLocations(bounds) {
        // Gets all locations from API that can be seen
        let ignoreStaleRequest = false;
        fetch("/api/location/list/?latmin=" + bounds._southWest.lat.toString()
              + "&latmax=" + bounds._northEast.lat.toString()
              + "&longmin=" + bounds._southWest.lng.toString()
              + "&longmax=" + bounds._northEast.lng.toString(), {
            method: "GET",
            credentials: "same-origin"
        })
        .then((response) => {
            if (!response.ok) throw Error(response.statusText);
            return response.json();
        })
        .then((data) => {
            if (!ignoreStaleRequest) {
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
        // Calls GetLocations() on initial load of map
        if(!first){
            first = true
            const map = useMap()
            GetLocations(map.getBounds())
        }
        return null
    }
    
    function MapEvents() {
        // Calls GetLocations() whenever map is moved or zoom is changed
        const map = useMapEvents({
            moveend: () => GetLocations(map.getBounds()),
            zoomend: () => GetLocations(map.getBounds())
        });
        return null;
    }

    function LocationMarker(location) {
        // Handles the Marker for a single location
        const [reviewsState, setReviewsState] = useState([]);
        const [overallAvgState, setOverallAvgState] = useState(0);
        const [qualityAvgState, setQualityAvgState] = useState(0);
        const [slopeAvgState, setSlopeAvgState] = useState(0);
        const [distAvgState, setDistAvgState] = useState(0);

        useEffect(() => {
            let ignoreStaleRequest = false;
            fetch("/api/review/list/?locationid=" + location.location.location_id.toString(), {
                method: "GET",
                credentials: "same-origin"
            })
            .then((response) => {
                if (!response.ok) throw Error(response.statusText);
                return response.json();
            })
            .then((data) => {
                if (!ignoreStaleRequest) {
                    if (data.status_code === undefined) {
                        setReviewsState(data.reviews);
                        setOverallAvgState(data.overall);
                        setQualityAvgState(data.sidewalk_quality);
                        setSlopeAvgState(data.slope);
                        setDistAvgState(data.road_dist);
                    }
                }
            })
            .catch((error) => console.log(error));

            return () => {
                ignoreStaleRequest = true;
            };
        }, [location])

        return (
            <Marker position={[location.location.latitude, location.location.longitude]} icon={customIcon}>
                <Popup>
                    <div>Overall: {overallAvgState} / 5.0</div>
                    <div>Sidewalk Quality: {qualityAvgState} / 5.0</div>
                    <div>Slope: {slopeAvgState} / 5.0</div>
                    <div>Distance from Road: {distAvgState} / 5.0</div>
                    <br/>
                    {reviewsState.map((review) => {
                        return (
                            <p key={review.review_id}>
                                <a href={"/users/" + review.username}>
                                    <b>{review.username}</b>
                                </a>
                                {" " + review.content}
                            </p>
                        );
                    })}
                </Popup>
            </Marker>
        );
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

            {locationsState.map((location) => {
                return (
                    <LocationMarker key={location.location_id} location={location} />
                );
            })}

        </MapContainer>
    );
}