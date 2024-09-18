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
    [address] VARCHAR(100)
)