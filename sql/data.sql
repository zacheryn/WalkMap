PRAGMA foreign_keys = ON;

INSERT INTO Users(username, first_name, last_name, email, [password])
VALUES ('test_user', 'John', 'Doe', 'zacheryn@umich.edu', 'sha512$a45ffdcc71884853a2cba9e6bc55e812$c739cef1aec45c6e345c8463136dc1ae2fe19963106cf748baf87c7102937aa96928aa1db7fe1d8da6bd343428ff3167f4500c8a61095fb771957b4367868fb8'),
       ('other_user', 'Jane', 'Doe', 'zacheryn@umich.edu', 'sha512$a45ffdcc71884853a2cba9e6bc55e812$c739cef1aec45c6e345c8463136dc1ae2fe19963106cf748baf87c7102937aa96928aa1db7fe1d8da6bd343428ff3167f4500c8a61095fb771957b4367868fb8');

INSERT INTO Locations(country_name, state_name, city_name, building_name, longitude, latitude)
VALUES ('United States', 'Michigan', 'Ann Arbor', NULL, -83.732124, 42.279594),
       ('United States', 'Michigan', 'Ann Arbor', 'University of Michigan - Central Campus', -83.738220, 42.278046),
       ('United States', 'Michigan', 'Ann Arbor', 'University of Michigan - North Campus', -83.71615878050201, 42.29243500051665),
       ('United States', 'Michigan', 'Ann Arbor', 'Michigan Stadium', -83.74884016750399, 42.26618116426456)

INSERT INTO Reviews(content, overall, sidewalk_quality, slope, road_dist, sidewalk, public_trans)
VALUES ('Great city to walk around in!', 4.0, 4, 5, 3, 1, 1),
       ('The walkability of this city is fantastic.', 4.33, 5, 5, 3, 1, 1),
       ('The campus was quite welcoming', 5.0, 5, 5, 5, 1, 1),
       ('The campus was nice.', 5.0, 5, 5, 5, 1, 1),
       ('North campus is a little hilly.', 3.67, 5, 2, 4, 1, 1),
       ('North campus was quite enjoyable.', 4.33, 5, 3, 5, 1, 1);

INSERT INTO OwnsReview(user_id, review_id)
VALUES (1, 1),
       (2, 2),
       (1, 3),
       (2, 4),
       (1, 5),
       (2, 6);

INSERT INTO ReviewLocation(location_id, review_id)
VALUES (1, 1),
       (1, 2),
       (2, 3),
       (2, 4),
       (3, 5),
       (3, 6);
