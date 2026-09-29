"""Constants for qBittorrent API v5"""
from typing import Final
from datetime import timedelta
import voluptuous as vol
import logging

DOMAIN: Final = "qbittorrent_api_v5"

#Defaults
DEFAULT_NAME = "qBittorrent" #This is the base sensor and display name, that will have the target hostname added for uniqueness
DEFAULT_URL = "http://192.168.1.1:8080"
DEFAULT_VERIFY_SSL = False
DEFAULT_SENSOR_SCAN_INTERVAL = 60
DEFAULT_EVENT_SCAN_INTERVAL = 10
DEFAULT_EVENT_COMPLETE = True
DEFAULT_EVENT_ADDED = False
DEFAULT_EVENT_REMOVED = False

#Events
CONF_EVENT_COMPLETE = "torrent_complete"
CONF_EVENT_ADDED = "torrent_added"
CONF_EVENT_REMOVED = "torrent_removed"
CONF_EVENT_SCAN_INTERVAL= "event_scan_interval"

EVENT_COMPLETED = DOMAIN + "_" + CONF_EVENT_COMPLETE
EVENT_ADDED = DOMAIN + "_" + CONF_EVENT_ADDED
EVENT_REMOVED = DOMAIN + "_" + CONF_EVENT_REMOVED

#Sensors
SENSOR_TYPE_CURRENT_STATUS = "current_status"
SENSOR_TYPE_DOWNLOAD_SPEED = "download_speed"
SENSOR_TYPE_UPLOAD_SPEED = "upload_speed"
SENSOR_TYPE_DOWNLOADING_TOTAL = "downloading"
SENSOR_TYPE_LONGEST_ETA = "eta"

#Transfer limits (numbers)
#The entities expose these limits in KiB/s, but qBittorrent's application preferences store them in bytes/s
#(despite the WebUI API docs saying KiB/s), with -1 meaning "no limit"
NUMBER_TYPE_DOWNLOAD_LIMIT = "download_limit"
NUMBER_TYPE_UPLOAD_LIMIT = "upload_limit"
NUMBER_TYPE_ALT_DOWNLOAD_LIMIT = "alternative_download_limit"
NUMBER_TYPE_ALT_UPLOAD_LIMIT = "alternative_upload_limit"

#Maps each number entity to its qBittorrent preference key
NUMBER_TYPE_PREFERENCE_KEY = {
    NUMBER_TYPE_DOWNLOAD_LIMIT: "dl_limit",
    NUMBER_TYPE_UPLOAD_LIMIT: "up_limit",
    NUMBER_TYPE_ALT_DOWNLOAD_LIMIT: "alt_dl_limit",
    NUMBER_TYPE_ALT_UPLOAD_LIMIT: "alt_up_limit",
}

#A speed limit of zero or below is treated as "unlimited" by qBittorrent
UNLIMITED_SPEED_VALUE = -1
BYTES_PER_KIBIBYTE = 1024
MAX_SPEED_LIMIT_KIBIBYTES = 100 * 1024 * 1024  # 100 GiB/s, a generous ceiling for the number entities

#Switches
SWITCH_TYPE_ALTERNATIVE_SPEED_LIMITS = "alternative_speed_limits"

#Services
ACTION_RESUME_DOWLOADS = 'action_resume_downloads'
ACTION_PAUSE_DOWLOADS = 'action_pause_downloads'
ACTION_GET_TORRENT_INFO = 'action_get_torrent_info'
ACTION_DELETE_TORRENT = 'action_delete_torrent'
ACTION_SERVICE_SHUTDOWN = 'action_service_shutdown'

#Logging
LOGGER = logging.getLogger(__package__)
