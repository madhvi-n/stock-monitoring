# Store monitoring project

### Requirements
A company monitors several stores in the US and needs to monitor if the store is online or not.
All stores are supposed to be online during their business hours.
Due to some unknown reasons, a store might go inactive for a few hours.
Store owners want to get a report of how often this happened in the past.
The task is to build backend APIs that will help store owners achieve this goal.


### Data sources
- A poll data which is generated every hour with the schema `(store_id, timestamp_utc, status)`

- We have business hours of the stores `(store_id, dayOfWeek(0=Monday, 6=Sunday), start_time_local, end_time_local)`
  - These times are in the local time zone
  - If data is missing for a store, assume it is open 24*7

- Timezone of these stores with the schema `(store_id, timezone_str)`
  - If data is missing for a store, assume it is America/Chicago

### System Requirements
- Precompute the data every hour since the data keeps changing
- Save the CSV data into a relevant database and use it to generate uptime and downtime reports

### Output
- We want to output a report to the user that has the following schema
`(store_id, uptime_last_hour, uptime_last_day, update_last_week, downtime_last_hour, downtime_last_day, downtime_last_week)`
  - Uptime and downtime should only include observations within business hours.
  - You need to extrapolate uptime and downtime based on the periodic polls we have ingested, to the entire time interval. eg, business hours for a store are 9 AM to 12 PM on Monday, we only have 2 observations for this store on a particular date (Monday) in our data at 10:14 AM and 11:15 AM
  - we need to fill the entire business hours interval with uptime and downtime from these 2 observations based on some sane interpolation logic


### API Requirements
1. `/trigger_report` endpoint that will trigger report generation from the data provided (stored in DB)
Output - `report_id` (random string)

2. `report_id` will be used for polling the status of report completion
/`get_report` endpoint that will return the status of the report or the csv
Input - `report_id`
Output -
if report generation is not complete, return “Running” as the output
if report generation is complete, return “Complete” along with the CSV file with the schema described above.


# Requirements
- Backend
    - Python 3.8+
    - virtualenv
    - WSL

# Installation

Clone the repository and enter the root directory
```
git clone https://github.com/madhvi-n/store-monitoring.git
cd store-monitoring
```


Create a virtual environment and activate it
```
virtualenv venv
source venv/bin/activate
```

Making sure your virtual environment is activated, install the dependencies using `pip`
```
pip install -r requirements.txt
```

You can set the secret key for django project in 2 ways
- Edit the `reddit_clone/settings.py` file and add a key manually, some random string.
- Edit the venv file to export `SECRET_KEY`


After installing dependencies, migrate Django apps.(You will find the list of apps when you run the command `python manage.py runserver`)
```
python manage.py migrate
```

Finally start your Django server
```
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` or `localhost:8000` for running web server
Alternatively you can access the admin interface on `http://127.0.0.1:8000/admin/` or `localhost:8000/admin`

Access python shell
```
python manage.py shell
```


### Generating data using management commands

```
python manage.py import_stores_data #add stores to database with their timezones
python manage.py import_business_hours # add business hours for stores in database
python.manage.py import_poll_data # add poll data in database
python.manage.py generate_store_report # can be used to generate store reports
```

### Running celery tasks
- Instead of generating reports directly from api endpoints, it could be more efficient to use Celery to create reports once poll data has been ingested into the database. This can be achieved by chaining tasks in Celery so that report generation only occurs after poll data has been successfully inserted.

- To optimize user performance and reduce latency, reports can be cached. When the `trigger_report` API is called, the ID of the last generated report can be fetched and returned. Alternatively, cached data can be used to return the most recent report generated for this API.

- Since reports will be generated periodically every hour, a Celery task can be enabled to remove old reports. This will help to keep the system running smoothly and prevent it from becoming cluttered with outdated reports.


### To make the system distributed and scalable, we could consider the following steps:
- Use a distributed message broker: Instead of relying on a single server to handle all the tasks, we can use a distributed message broker such as RabbitMQ or Apache Kafka. This will help to distribute the load across multiple servers, making the system more scalable.

- Use multiple worker nodes: Instead of relying on a single worker node to process all the tasks, we can use multiple worker nodes to handle the tasks in parallel. This will help to improve the system's throughput and make it more scalable.

- Use a load balancer: To distribute the load across multiple worker nodes, we can use a load balancer such as NGINX or HAProxy. The load balancer will help to distribute the tasks evenly across the worker nodes, ensuring that no single node becomes overloaded.

 - Use a distributed caching solution: To improve the system's performance and reduce latency, we can use a distributed caching solution such as Redis. This will help to reduce the number of requests that need to hit the database, improving the system's overall performance.

- Monitor and scale the system: To ensure that the system is running smoothly, we need to monitor its performance and scale it up or down as needed. This can be achieved using tools such as Prometheus and Kubernetes, which can automatically scale the system based on predefined metrics such as CPU usage or request rate.

By implementing these steps, we can create a distributed and scalable system that can handle a large number of requests and process them efficiently


#### Celery commands
`celery -A stores worker -l info`
`celery -A stores beat -l info`
