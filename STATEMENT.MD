### Problem Statement
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



### API Requirements
1. `/trigger_report` endpoint that will trigger report generation from the data provided

2. `report_id` will be used for polling the status of report completion
/`get_report` endpoint that will return the status of the report or the csv
Input - `report_id`
Output -
if report generation is not complete, return “Running” as the output
if report generation is complete, return “Complete” along with the CSV file with the schema described above.
