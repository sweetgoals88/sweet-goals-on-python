API_ENDPOINT = "http://localhost:3000/api/device"

EXTERNAL_READINGS_FILE = "./external-readings.csv"
INTERNAL_READINGS_FILE = "./internal-readings.csv"
KEY_FILE_LOCATION = "./key.txt"

API_ENDPOINTS = {
    "LOAD_EXTERNAL_READING": f"{API_ENDPOINT}/load-external-reading",
    "LOAD_INTERNAL_READING": f"{API_ENDPOINT}/load-internal-reading",
    "REPORT_STATUS": f"{API_ENDPOINT}/report-status"
}

# Number of seconds between device readings
INTERNAL_READING_INTERVAL = 3

# Number of minutes before device data is sent to the database
INTERNAL_SENDING_INTERVAL = 3

# Number of seconds between solar panel readings
EXTERNAL_READING_INTERVAL = 5

# Number of minutes before solar panel data is sent to the database
EXTERNAL_SENDING_INTERVAL = 15

# Number of times the device can try to connect to the database (i. e., reporting
# itself as operational) before shutting down
NUMBER_OF_ATTEMPTS_FOR_OPERATIONAL = 5

# Time used to compute the total current (Irms) read by the SCT
SECONDS_TO_READ_CURRENT = 1

# Time ellapsed between individual SCT readings when computing the total current (Irms)
MILLISECONDS_TO_READ_CURRENT = 10
