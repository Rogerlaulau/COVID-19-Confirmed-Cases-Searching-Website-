# Covid-19 Data Visualisation

It is a website that provides the most updated information about Covid-19 development in Hong Kong on a daily basis. Visitors could input any locations of their choices in the search bar and obtain the locations of confirmed cases within 1 km. By clicking the button Map, text results could be visualised on a map immediately, with the input location as the center. Go to Navigation Bar and click "All Locations" to view all confirmed cases in the past 14 days.

### # languages: Python, HTML, CSS, Javascript

### # packages: folium, HKAddressParser, Flask, pandas

This project involves backend development, frontend development, API, hosting service, data extraction, data transformation (physical address to latitude & longitudes), data loading, algorithm of convert coordinate system into grid system for quick search, data visualisation.

## The steps are as explained below:

- source the latest data from government API on confirmed cases.
- convert from physical address to coordinates (lats and longs).
- convert coordinate system to grid system in memory by splitting coordinates system into blocks
- create endpoints for returning the home page to frontend.
- create "/search/<location>" for processing the near locations of confirmed cases by the searched location.
- create "/map/<location>" for returning html (map) to frontend based on the searched location.
Note: in order not to ask visitor to enter the same location again, localStorage of browser is used to saved the searched location. Thus, once the button Map is clicked, the info is obtained from localStorage and send to the backend.
- create endpoint "/map/all" to return the all locations on map
- create endpoint "/comment" to return the comment.html
- create endpoint "/comment/submit" for receiving and storing the comment from visitors.
- to show the distance of each confirmed case from the searched location, a math equation is used to calculated it.

---

## Note:

- Note that, package folium is user-friendly to create map with lats and longs.
- HKAddressParser is brilliant to identify an accurate location and return latitudes and longitudes. An API from HK government is called to get the coordinates.
- Nginx, a reverse proxy is set and bind to my domain from freenom.