PRAGMA foreign_keys = ON;

CREATE TABLE Users(
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(40) NOT NULL,
    first_name VARCHAR(20),
    last_name VARCHAR(20),
    email VARCHAR(40) NOT NULL,
    [filename] VARCHAR(64) NOT NULL DEFAULT "defaultProPic.png",
    [password] VARCHAR(256) NOT NULL
);

CREATE TABLE Locations(
    location_id INTEGER PRIMARY KEY AUTOINCREMENT,
    country_name VARCHAR(100) NOT NULL,
    state_name VARCHAR(100) NOT NULL,
    city_name VARCHAR(100) NOT NULL,
    [address] VARCHAR(100),
    longitude REAL NOT NULL,
    latitude REAL NOT NULL,
    UNIQUE(longitude, latitude)
);

CREATE TABLE Reviews(
    review_id INTEGER PRIMARY KEY AUTOINCREMENT,
    content VARCHAR(2000),
    overall REAL NOT NULL,
    sidewalk_quality INTEGER,
    slope INTEGER,
    road_dist INTEGER,
    sidewalk INTEGER CHECK(sidewalk IN (0, 1)),
    public_trans INTEGER CHECK(public_trans IN (0, 1)),
    created DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE OwnsReview(
    user_id INTEGER NOT NULL,
    review_id INTEGER NOT NULL,
    PRIMARY KEY(user_id, review_id),
    FOREIGN KEY(user_id) REFERENCES Users(user_id) ON DELETE CASCADE,
    FOREIGN KEY(review_id) REFERENCES Reviews(review_id) ON DELETE CASCADE
);

CREATE TABLE ReviewLocation(
    location_id INTEGER NOT NULL,
    review_id INTEGER NOT NULL,
    PRIMARY KEY(location_id, review_id),
    FOREIGN KEY(location_id) REFERENCES Locations(location_id) ON DELETE CASCADE,
    FOREIGN KEY(review_id) REFERENCES Reviews(review_id) ON DELETE CASCADE
);