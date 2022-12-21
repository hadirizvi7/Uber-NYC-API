# Uber NYC API

This API allows developers to fetch over 4.5 million Uber ride records that occurred in New York City between January and June of 2015. The data tracks the time of day that the ride occurred, the latitude/longitude, and the corresponding borough/zone. The API serves a number of GET endpoints to allow for efficient data retrieval. This functionality is achieved through the FastAPI framework for API development and PostgreSQL for data storage/persistence. 

## Source Data

The source data used for this project comes from the NYC Taxi & Limousine Commission (TLC), later obtained and published by FiveThirtyEight. You can find the corresponding repository [here] (https://github.com/fivethirtyeight/uber-tlc-foil-response).

## Database Setup

One of the primary steps is to transfer the source data from flat CSV files to a relational database such as PostgreSQL. This can be achieved in one of two ways:

1. **Built-in Database Functionality**

The user interface for many database technologies (including Postgres) allows developers to import different types of data. For example, Postico (Mac UI for Postgres) has a built-in option for importing CSV data.

2. **Computing Frameworks (ex. PySpark)**

For use cases that involve larger data sets, a tool such as PySpark may significantly optimize the data migration process. This is ideal for our scenario, as manually migrating these set of tables would be cumbersome in terms of completion time.

Once the data migration portion is handled, you can execute the application as follows:

### 1. Download the repository to your Local Device

```bash
git clone https://github.com/hadirizvi7/Uber-NYC-API.git
```

### 2. Install the necessary libraries/dependencies

```bash
pip3 install -r requirements.txt
```

### 3. Execute the included Shell Script (MacOS/Linux)

```bash
cd src
uvicorn main:app --reload
```

If everything goes as expected, you should be provided a local URL that redirects you to a Swagger UI instance (ex. 127.0.0.1:8000). You should also see a number of endpoints corresponding to the API functions present in `src/main.py`.

## Unit Testing

The PyTest framework was used in order to create unit tests that validated key functionality. Another noteworthy tool was the coverage library, which provides an in-depth report on code coverage across a given application. This library can be utilized as follows:

```bash
coverage run -m pytest
coverage html
```

This will create a folder within your current directory. You can then open `htmlcov/index.html` in your local browser to see the necessary coverage statistics.

After writing a number of different test cases, we were able to achieve 94% code coverage for this application.

## Next Steps

1. **Expansion of Data Set**

One significant limitation of this current application is the fact that there is no data beyond June of 2015. This indicates that any future analysis done with this data would not provide up-to-date insight. We could potentially remedy this by migrating more recent data via one of the two methods mentioned previously.

2. **Caching**

Developers will inevitably look for data trends around specific dates or time frames (ex. holidays). As a result, there will be a slight bias for some records over others. However, from an implementation standpoint, the time it takes to query for all records is uniform. We can account for this slight bias of records by incorporating caching. For example, a caching policy such as LRU would ensure that more recently used records are queried faster.

3. **Client Side Considerations**

Once this code is containerized and deployed, the frontend will only display the Swagger UI and the corresponding endpoints. While this is sufficient for other developers, we can enhance user experience by implementing a simple dashboard that uses event-driven programming. It would most likely include customizable visualizations so that the data can be viewed in a more qualitative manner. 