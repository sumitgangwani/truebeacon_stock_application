Readme file for full-stack application:

# Full-Stack Application

## Overview

This is a Full-Stack application that implements a web-based system with user authentication, data visualization, and order placement functionalities.

## Tech Stack

- programming Language: python
- backend framework: flask
- database: sqlite
- template: jinja2
- charting library: chart.js

## Getting Started

### Prerequisites

The python dependencies should be installed using a virtualenv. The list of dependencies has been specified in requirements.txt and should be installed using pip.

Tasks completed:

Minimum Requirements:

1. The data should be inserted into a SQL database (SQLite)
2. GET /historical-data API, must be created which queries the database and returns the data. The API should have query parameters for *symbol,* *from_data* and *to_date* and should return data for a symbol between the input dates for the input symbol
3. The front-end should call the API and the returned time-series data should be displayed as a chart with prices on Y-axis and date on the X-axis. There should be an input to filter for symbol, and date selector inputs for from_date and to_date for the chart.

![image](https://github.com/sumitgangwani/truebeacon_stock_application/assets/67985559/8fe41397-b62d-4441-a3a9-f2566f8faa3d)


Additional Requirements:

1. Register
![image](https://github.com/sumitgangwani/truebeacon_stock_application/assets/67985559/51340b94-c12c-48e2-8669-646818c990b7)
![image](https://github.com/sumitgangwani/truebeacon_stock_application/assets/67985559/a8a255af-d7af-42b2-beab-a778cab61047)


2. Login
![image](https://github.com/sumitgangwani/truebeacon_stock_application/assets/67985559/b6c0d14a-aa2e-464c-a068-9bc3927df2a9)


3. View Dashboard
    1. Display Table with data - holdings_response.json
![image](https://github.com/sumitgangwani/truebeacon_stock_application/assets/67985559/48ba6647-f93a-4b77-b47f-d043faa46976)

    2. Displays Chart with -historical_prices.csv
![image](https://github.com/sumitgangwani/truebeacon_stock_application/assets/67985559/8fe41397-b62d-4441-a3a9-f2566f8faa3d)
    4. Display Profile information - profile_response.json
![image](https://github.com/sumitgangwani/truebeacon_stock_application/assets/67985559/adca3d4d-bcf0-4024-a05b-477474f9173c)




5. Place Order 
    1. Simple form with inputs for Symbol, price and quantity with a button to submit trade which calls an API that returns place_order_response.json
   ![image](https://github.com/sumitgangwani/truebeacon_stock_application/assets/67985559/e68058b8-87a5-4ab9-84d5-2ddcdea7d5da)


  
Front End Requirements (Additional Requirements):

1. Login Page    
2. Register Page    
3. Dashboard Page

Backend Requirements (Additional Requirements):

1. Create endpoints for user authentication
2. Create endpoints that return mock responses (please note that i was fetching from json link and due to excessive api hits, the data was not getting fetched for a while so i had replaced the funcationality of fetching the data from json link to fetching data from database (i have stored the mock responses there too))

