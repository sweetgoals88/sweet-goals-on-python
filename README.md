# Sweet Goals on Raspberry Pi

This is the Python version of the Solar Sync project (a product developed by the Algorithm Avengers team, later
referred to as Sweet Goals).

Among the requirements for the code it is possible to find the following:
* The Raspberry Pi must read external sensor data (i. e., temperature, light, current, voltage and wattage) every 5 seconds and save it along a timestamp in a local .CSV file
* New readings are appended to the end of the local .CSV file
* The Raspberry Pi must send a summary of its previous readings to the API once for every 10 minute window of the day
* The summary doesn't necessarily have to be sent at times that are multiples of ten (i. e., 6:10, 6:20, 6:30, etc.), but they should be sent as closely as possible
* A new summary is created by taking the readings in the local .CSV file, which are averaged and aggregated into a single "representative" reading
* The representative reading is sent as a JSON object to the API, which interprets it as the summary of the readings done in the last 10 minute window
* Once a new summary is sent, the local .CSV file is truncated to zero 

* The Raspberry Pi has an embedded device key whose location is indicated in the KEY_FILE_LOCATION variable
* When it first boots, the Raspberry Pi must read its key and validate it is a 32 character long hexadecimal string
* If the key is not valid, the Raspberry Pi must shut down and append an appropriate log to the logging file indicated by the LOG_FILE_LOCATION variable
* After validating its key, the Raspberry Pi must send a request to the appropriate API endpoint to indicate it is running

