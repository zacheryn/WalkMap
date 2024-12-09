import React, { useState, useEffect } from "react";
import dayjs from "dayjs";
import relativeTime from "dayjs/plugin/relativeTime";
import utc from "dayjs/plugin/utc";
import { MapContainer, TileLayer, Marker, useMapEvents, useMap, Popup } from "react-leaflet";
import { Icon } from "leaflet"
import { OpenStreetMapProvider, GeoSearchControl } from 'leaflet-geosearch'
import { FaStar } from "react-icons/fa";
import { use } from "chai";
import { func } from "prop-types";

dayjs.extend(relativeTime);
dayjs.extend(utc);

var first = false

export default function App() {
    // States
    const [locationsState, setLocationsState] = useState([]);
    // const [newCenter, setNewCenter] = useState([]);

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
        const [newReviewState, setNewReviewState] = useState({quality: 0, slope: 0, dist: 0, content: ""});

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

        function deleteReview(id, index) {
            useEffect(() => {
                let ignoreStaleRequest = false;
                fetch("/api/review/delete/?reviewid=" + id.toString(), {
                    method: "DELETE",
                    credentials: "same-origin"
                })
                .then((response) => {
                    if (!response.ok) throw Error(response.statusText);
                    return response.json();
                })
                .then((status) => {
                    if (!ignoreStaleRequest) {
                        if (status = 204) {
                            let nextReviews = reviewsState;
                            nextReviews.splice(index, 1);
                            setReviewsState(nextReviews);
                        }
                    }
                })
                .catch((error) => console.log(error));

                return () => {
                    ignoreStaleRequest = true;
                };
            }, [id])
        }

        // Form for the user to add a review
        function addReview(e){
            e.preventDefault()
            const overall = (newReviewState.quality + newReviewState.slope + newReviewState.dist) / 3
            fetch("/api/review/add/?locationid=" + location.location.location_id.toString(), {
                method: "POST",
                headers: { 'Content-Type': 'application/json' },
                credentials: "same-origin",
                body: JSON.stringify({
                    content: newReviewState.content,
                    overall: overall.toPrecision(3),
                    quality: newReviewState.quality,
                    slope: newReviewState.slope,
                    dist: newReviewState.dist
                })
            })
            .then((response) => {
                if (!response.ok) throw Error(response.statusText);
                return response.json();
            })
            .then((data) => {
                if (data.status_code == undefined) {
                    setReviewsState(...reviewsState, data.review);
                    setOverallAvgState(data.overall);
                    setQualityAvgState(data.sidewalk_quality);
                    setSlopeAvgState(data.slope);
                    setDistAvgState(data.road_dist);
                    setNewReviewState({quality: 0, slope: 0, dist: 0, content: ""});
                }
            })
            .catch((error) => console.log(error));

            return () => {
                ignoreStaleRequest = true;
            };
        }

        return (
            <Marker position={[location.location.latitude, location.location.longitude]} icon={customIcon}>
                <Popup maxHeight="200px">
                    <div><b>{location.location.country_name}, {location.location.state_name}, {location.location.city_name}, {location.location.building_name}</b></div>
                    <div><b>Overall:</b> {overallAvgState} / 5.0</div>
                    <div><b>Sidewalk Quality:</b> {qualityAvgState} / 5.0</div>
                    <div><b>Slope:</b> {slopeAvgState} / 5.0</div>
                    <div><b>Distance from Road:</b> {distAvgState} / 5.0</div>
                    <br/>
                    {reviewsState.map((review, i) => {
                        if(review.is_owner){
                            return (
                                <p key={review.review_id}>
                                    <a href={"/user/" + review.username}>
                                        <b>{review.username}</b>
                                    </a>
                                    {" " + review.content}
                                    <button
                                    onClick={(e) => {
                                        e.preventDefault();
                                        deleteReview(review.review_id, i);
                                    }}
                                    >delete</button>
                                </p>
                            );
                        }
                        return (
                            <p key={review.review_id}>
                                <a href={"/user/" + review.username}>
                                    <b>{review.username}</b>
                                </a>
                                {" " + review.content}
                            </p>
                        );
                    })}
                    <br/>
                    <div>
                        <form onSubmit={addReview}>
                            <div>
                                <label><span>Quality:</span></label>
                                {[...Array(5)].map((_, i) => {
                                    return (
                                        <input
                                            type="radio"
                                            key={i}
                                            name="quality"
                                            value={i + 1}
                                            onClick={(e) => {
                                                setNewReviewState({...newReviewState, ["quality"]: Number(e.target.value)});
                                            }}
                                        />
                                    );
                                })}
                            </div>
                            <div>
                                <label><span>Slope:</span></label>
                                {[...Array(5)].map((_, i) => {
                                    return (
                                        <input
                                            type="radio"
                                            key={i}
                                            name="slope"
                                            value={i + 1}
                                            onClick={(e) => {
                                                setNewReviewState({...newReviewState, ["slope"]: Number(e.target.value)});
                                            }}
                                        />
                                    );
                                })}
                            </div>
                            <div>
                                <label><span>Distance from road:</span></label>
                                {[...Array(5)].map((_, i) => {
                                    return (
                                        <input
                                            type="radio"
                                            key={i}
                                            name="dist"
                                            value={i + 1}
                                            onClick={(e) => {
                                                setNewReviewState({...newReviewState, ["dist"]: Number(e.target.value)});
                                            }}
                                        />
                                    );
                                })}
                            </div>
                            <div>
                                <label><span>Content:</span></label>
                                <input
                                    type="text"
                                    id="content"
                                    name="content"
                                    value={newReviewState.content}
                                    placeholder="What do you have to say?"
                                    onKeyDown={(e) => { e.key === 'Enter' && e.preventDefault(); }}
                                    onChange={(e) => {
                                        e.preventDefault()
                                        setNewReviewState({...newReviewState, ["content"]: e.target.value});
                                    }}
                                />
                            </div>
                            <div>
                                <input type="submit" value="Submit"/>
                            </div>
                        </form>
                    </div>
                </Popup>
            </Marker>
        );
    }

    // function Search(){
    //     const [country, setCountry] = useState("");
    //     const [state, setState] = useState("");
    //     const [city, setCity] = useState("");
    //     const [address, setAddress] = useState("");
    //     const [building, setBuilding] = useState("");

    // }

    // make new leaflet element
    const Search = (props) => {
        const map = useMap() // access to leaflet map
        const { provider } = props

        useEffect(() => {
            const searchControl = new GeoSearchControl({
                provider,
            })

            map.addControl(searchControl) // this is how you add a control in vanilla leaflet
            return () => map.removeControl(searchControl)
        }, [props])

        return null // don't want anything to show up from this comp
    }

    return (
        <>
        {/* <Search /> */}
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

            <Search provider={new OpenStreetMapProvider()} />

            {locationsState.map((location) => {
                return (
                    <LocationMarker key={location.location_id} location={location} />
                );
            })}
        </MapContainer>
        </>
    );
}