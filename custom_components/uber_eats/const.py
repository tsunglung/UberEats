"""Constants of the Uber Eats component."""
from datetime import timedelta

DEFAULT_NAME = "Uber Eats"
DOMAIN = "uber_eats"
PLATFORMS = [ "binary_sensor", "button", "image", "sensor" ]
DATA_KEY = "data_uber_eats"

ATTR_ETA = "eta"
ATTR_RESTAURANT_NAME = "restaurant_name"
ATTR_COURIER_NAME = "courier_name"
ATTR_COURIER_PHONE = "courier_phone"
ATTR_COURIER_DESCRIPTION = "courier_description"
ATTR_TITLE_SUMMARY = "title_summary"
ATTR_SUBTITLE_SUMMARY = "subtitle_summary"
ATTR_LATITUDE = "latitude"
ATTR_LONGITUDE = "longitude"
ATTR_HTTPS_RESULT = "https_result"
ATTR_LIST = [
    ATTR_ETA,
    ATTR_RESTAURANT_NAME,
    ATTR_COURIER_NAME,
    ATTR_COURIER_DESCRIPTION,
    ATTR_LATITUDE,
    ATTR_LONGITUDE,
    ATTR_SUBTITLE_SUMMARY,
    ATTR_TITLE_SUMMARY,
    ATTR_HTTPS_RESULT
]

DEFAULT_SCAN_INTERVAL = timedelta(minutes=1)

CONF_ACCOUNT = "account"
CONF_COOKIE = "cookie"
CONF_LOCALCODE = "localcode"
ATTRIBUTION = "Powered by Uber Eats Data"
MANUFACTURER = "Uber Eats"
DEFAULT_LOCALCODE = "tw"
UBER_EATS_COORDINATOR = "uber_eats_coordinator"
UBER_EATS_DATA = "uber_eats_data"
UBER_EATS_NAME = "uber_eats_name"
UBER_EATS_ORDERS = "orders"
UPDATE_LISTENER = "update_listener"
DEFAULT_LOCALCODE = "tw"

HA_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36 OPR/38.0.2220.41"
BASE_URL = 'https://www.ubereats.com/api/getActiveOrdersV1'

REQUEST_TIMEOUT = 10  # seconds

LOCALCODES = {
    "en": "America/Los_Angeles",
    "tw": "Asia/Taipei"
}
