"""Constants for the SAAS - Sleep As Android Stats integration."""

DOMAIN = "saas"

INTEGRATION_NAME = "SAAS - Sleep As Android Stats"
MODEL = "SAAS - Version 0.0.1"

CONF_NAME = "name" # Name of the Integration
CONF_TOPIC = "topic_template"   # MQTT Topic for Sleep As Android Events
CONF_QOS = "qos"    # Quality of Service
CONF_AWAKE_DURATION = "awake_duration" # Awake Duration
CONF_SLEEP_DURATION = "sleep_duration"  # Sleep Duration

CONF_AWAKE_STATES = "awake_states"  # Awake States
CONF_SLEEP_STATES = "sleep_states" # Sleep States

DEFAULT_AWAKE_DURATION = 10 # Default Awake Duration
DEFAULT_SLEEP_DURATION = 10    # Default Sleep Duration
DEFAULT_AWAKE_STATES = ["awake", "sleep_tracking_stopped"] # Default Awake States
DEFAULT_SLEEP_STATES = ["not_awake", "rem", "light_sleep", "deep_sleep", "sleep_tracking_started"]    # Default Sleep States

SENSOR_TYPES = {
    "state": {"name": "State", "device_class": None},
    "awake": {"name": "Awake", "device_class": "motion"},
}

AVAILABLE_STATES = [
    'unknown',
    'alarm_alert_dismiss',
    'alarm_alert_start',
    'alarm_rescheduled',
    'alarm_skip_next',
    'alarm_snooze_canceled',
    'alarm_snooze_clicked',
    'antisnoring',
    'apnea_alarm',
    'awake',
    'before_alarm',
    'before_smart_period',
    'deep_sleep',
    'light_sleep',
    'lullaby_start',
    'lullaby_stop',
    'lullaby_volume_down',
    'not_awake',
    'rem',
    'show_skip_next_alarm',
    'sleep_tracking_paused',
    'sleep_tracking_resumed',
    'sleep_tracking_started',
    'sleep_tracking_stopped',
    'smart_period',
    'sound_event_baby',
    'sound_event_cough',
    'sound_event_laugh',
    'sound_event_snore',
    'sound_event_talk',
    'time_to_bed_alarm_alert'
]
STATE_MAPPING = {
    "unknown": "Unknown",
    "sleep_tracking_started": "Sleep Tracking Started",
    "sleep_tracking_stopped": "Sleep Tracking Stopped",
    "sleep_tracking_paused": "Sleep Tracking Paused",
    "sleep_tracking_resumed": "Sleep Tracking Resumed",
    "alarm_snooze_clicked": "Alarm Snoozed",
    "alarm_snooze_canceled": "Snooze Canceled",
    "time_to_bed_alarm_alert": "Time To Bed Alarm Alert",
    "alarm_alert_start": "Alarm Alert Started",
    "alarm_alert_dismiss": "Alarm Dismissed",
    "alarm_skip_next": "Skip Next Alarm",
    "show_skip_next_alarm": "Show Skip Next Alarm",
    "rem": "REM",
    "smart_period": "Smart Period",
    "before_smart_period": "Before Smart Period",
    "lullaby_start": "Lullaby Start",
    "lullaby_stop": "Lullaby Stop",
    "lullaby_volume_down": "Lullaby Volume Down",
    "deep_sleep": "Deep Sleep",
    "light_sleep": "Light Sleep",
    "awake": "Awake",
    "not_awake": "Not Awake",
    "apnea_alarm": "Apnea Alarm",
    "antisnoring": "Antisnoring",
    "before_alarm": "Before Alarm",
    "sound_event_snore": "Snore Detected",
    "sound_event_talk": "Talk Detected",
    "sound_event_cough": "Cough Detected",
    "sound_event_baby": "Baby Cry Detected",
    "sound_event_laugh": "Laugh Detected",
    "alarm_rescheduled": "Alarm Rescheduled"
}

SOUND_MAPPING = {
    'sound_event_snore': "Snore Detected",
    'sound_event_talk': "Talk Detected",
    'sound_event_cough': "Cough Detected",
    'sound_event_baby': "Baby Cry Detected",
    'sound_event_laugh': "Laugh Detected"
}

DISTURBANCE_MAPPING = {
    'apnea_alarm': "Apnea Alarm",
    'antisnoring': "Antisnoring"
}

ALARM_EVENT_MAPPING = {
    'before_alarm': "Before Alarm",
    'alarm_snooze_clicked': "Alarm Snoozed",
    'alarm_snooze_canceled': "Snooze Canceled",
    'time_to_bed_alarm_alert': "Time To Bed Alarm Alert",
    'alarm_alert_start': "Alarm Alert Started",
    'alarm_alert_dismiss': "Alarm Dismissed",
    'alarm_skip_next': "Skip Next Alarm",
    'show_skip_next_alarm': "Show Skip Next Alarm",
    'rem': "REM",
    'smart_period': "Smart Period",
    'before_smart_period': "Before Smart Period",
    "alarm_rescheduled": "Alarm Rescheduled"
}

SLEEP_TRACKING_MAPPING = {
    'sleep_tracking_started': "Sleep Tracking Started",
    'sleep_tracking_stopped': "Sleep Tracking Stopped",
    'sleep_tracking_paused': "Sleep Tracking Paused",
    'sleep_tracking_resumed': "Sleep Tracking Resumed"
}