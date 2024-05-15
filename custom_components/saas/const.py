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

CONF_NOTIFY_TARGET = "notify_target"    # Notify Target

DEFAULT_AWAKE_DURATION = 10 # Default Awake Duration
DEFAULT_SLEEP_DURATION = 10    # Default Sleep Duration
DEFAULT_AWAKE_STATES = ["Awake", "Sleep Tracking Stopped"] # Default Awake States
DEFAULT_SLEEP_STATES = ["Not Awake", "Rem", "Light Sleep", "Deep Sleep", "Sleep Tracking Started"]# Default Sleep States

SENSOR_TYPES = {
    "state": {"name": "State", "device_class": None},
    "awake": {"name": "Awake", "device_class": "motion"},
}

AVAILABLE_STATES = [
    'Unknown',
    'Alarm Alert Dismiss',
    'Alarm Alert Start',
    'Alarm Rescheduled',
    'Alarm Skip Next',
    'Alarm Snooze Canceled',
    'Alarm Snooze Clicked',
    'Antisnoring',
    'Apnea Alarm',
    'Awake',
    'Before Alarm',
    'Before Smart Period',
    'Deep Sleep',
    'Light Sleep',
    'Lullaby Start',
    'Lullaby Stop',
    'Lullaby Volume Down',
    'Not Awake',
    'Rem',
    'Show Skip Next Alarm',
    'Sleep Tracking Paused',
    'Sleep Tracking Resumed',
    'Sleep Tracking Started',
    'Sleep Tracking Stopped',
    'Smart Period',
    'Sound Event Baby',
    'Sound Event Cough',
    'Sound Event Laugh',
    'Sound Event Snore',
    'Sound Event Talk',
    'Time for Bed'
]
STATE_MAPPING = {
    "unknown": "Unknown",
    "sleep_tracking_started": "Sleep Tracking Started",
    "sleep_tracking_stopped": "Sleep Tracking Stopped",
    "sleep_tracking_paused": "Sleep Tracking Paused",
    "sleep_tracking_resumed": "Sleep Tracking Resumed",
    "alarm_snooze_clicked": "Alarm Snoozed",
    "alarm_snooze_canceled": "Snooze Canceled",
    "time_to_bed_alarm_alert": "Time for Bed",
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

REVERSE_STATE_MAPPING = {v: k for k, v in STATE_MAPPING.items()}

SLEEP_STAGE_MAPPING = {
    "unknown": "Unknown",
    "rem": "REM",
    "deep_sleep": "Deep Sleep",
    "light_sleep": "Light Sleep",
    "awake": "Awake",
    "not_awake": "Not Awake"
}
SOUND_MAPPING = {
    'sound_event_snore': "Snore Detected",
    'sound_event_talk': "Talk Detected",
    'sound_event_cough': "Cough Detected",
    'sound_event_baby': "Baby Cry Detected",
    'sound_event_laugh': "Laugh Detected"
}

LULLABY_MAPPING = {
    "lullaby_start": "Lullaby Start",
    "lullaby_stop": "Lullaby Stop",
    "lullaby_volume_down": "Lullaby Volume Down",
}

DISTURBANCE_MAPPING = {
    'apnea_alarm': "Apnea Alarm",
    'antisnoring': "Antisnoring"
}

ALARM_EVENT_MAPPING = {
    'before_alarm': "Before Alarm",
    'alarm_snooze_clicked': "Alarm Snoozed",
    'alarm_snooze_canceled': "Snooze Canceled",
    'time_to_bed_alarm_alert': "Time for Bed",
    'alarm_alert_start': "Alarm Alert Started",
    'alarm_alert_dismiss': "Alarm Dismissed",
    'alarm_skip_next': "Skip Next Alarm",
    'show_skip_next_alarm': "Show Skip Next Alarm",
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
