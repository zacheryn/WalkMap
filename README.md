# WalkMap

A webite that allows users to easily determine the walkability of an area. The website will collect information such as sidewalk quality, if there are steep slopes, how much space between sidewalks and streets, etc. This information will be displayed on an interactive map created using `React` and the `react-leaflet` component. The other pages will be rendered using `Flask`. On the back-end, all the information stored for the website handled with a `SQLite` database. The react portion of the site interacts with the database through a custom RESTful API create with `Flask`.

The website also allows users to submit reviews on areas which is how we keep track of local data.
