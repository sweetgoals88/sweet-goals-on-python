API_ENDPOINT = "http://localhost:3000/api/device"

EXTERNAL_READINGS_FILE = "./external-readings.csv"
INTERNAL_READINGS_FILE = "./internal-readings.csv"
KEY_FILE_LOCATION = "./key.txt"

API_ENDPOINTS = {
    "LOAD_EXTERNAL_READING": f"{API_ENDPOINT}/load-external-reading",
    "LOAD_INTERNAL_READING": f"{API_ENDPOINT}/load-internal-reading",
}
