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
DEFAULT_AWAKE_STATES = ['{"event":"awake"}', '{"event":"sleep_tracking_stopped"}'] # Default Awake States
DEFAULT_SLEEP_STATES = ['{"event":"not_awake"}', '{"event":"rem"}', '{"event":"light_sleep"}', '{"event":"deep_sleep"}', '{"event":"sleep_tracking_started"}']    # Default Sleep States

SENSOR_TYPES = {
    "state": {"name": "State", "device_class": None},
    "awake": {"name": "Awake", "device_class": "motion"},
}

AVAILABLE_STATES = [
    'unknown',
    '{"event":"alarm_alert_dismiss"}',
    '{"event":"alarm_alert_start"}',
    '{"event":"alarm_rescheduled"}',
    '{"event":"alarm_skip_next"}',
    '{"event":"alarm_snooze_canceled"}',
    '{"event":"alarm_snooze_clicked"}',
    '{"event":"antisnoring"}',
    '{"event":"apnea_alarm"}',
    '{"event":"awake"}',
    '{"event":"before_alarm"}',
    '{"event":"before_smart_period"}',
    '{"event":"deep_sleep"}',
    '{"event":"light_sleep"}',
    '{"event":"lullaby_start"}',
    '{"event":"lullaby_stop"}',
    '{"event":"lullaby_volume_down"}',
    '{"event":"not_awake"}',
    '{"event":"rem"}',
    '{"event":"show_skip_next_alarm"}',
    '{"event":"sleep_tracking_paused"}',
    '{"event":"sleep_tracking_resumed"}',
    '{"event":"sleep_tracking_started"}',
    '{"event":"sleep_tracking_stopped"}',
    '{"event":"smart_period"}',
    '{"event":"sound_event_baby"}',
    '{"event":"sound_event_cough"}',
    '{"event":"sound_event_laugh"}',
    '{"event":"sound_event_snore"}',
    '{"event":"sound_event_talk"}',
    '{"event":"time_to_bed_alarm_alert"}'
]
# State mapping
STATE_MAPPING = {
    "unknown": "Unknown",
    '{"event":"sleep_tracking_started"}': "Sleep Tracking Started",
    '{"event":"sleep_tracking_stopped"}': "Sleep Tracking Stopped",
    '{"event":"sleep_tracking_paused"}': "Sleep Tracking Paused",
    '{"event":"sleep_tracking_resumed"}': "Sleep Tracking Resumed",
    '{"event":"alarm_snooze_clicked"}': "Alarm Snoozed",
    '{"event":"alarm_snooze_canceled"}': "Snooze Canceled",
    '{"event":"time_to_bed_alarm_alert"}': "Time To Bed Alarm Alert",
    '{"event":"alarm_alert_start"}': "Alarm Alert Started",
    '{"event":"alarm_alert_dismiss"}': "Alarm Dismissed",
    '{"event":"alarm_skip_next"}': "Skip Next Alarm",
    '{"event":"show_skip_next_alarm"}': "Show Skip Next Alarm",
    '{"event":"rem"}': "REM",
    '{"event":"smart_period"}': "Smart Period",
    '{"event":"before_smart_period"}': "Before Smart Period",
    '{"event":"lullaby_start"}': "Lullaby Start",
    '{"event":"lullaby_stop"}': "Lullaby Stop",
    '{"event":"lullaby_volume_down"}': "Lullaby Volume Down",
    '{"event":"deep_sleep"}': "Deep Sleep",
    '{"event":"light_sleep"}': "Light Sleep",
    '{"event":"awake"}': "Awake",
    '{"event":"not_awake"}': "Not Awake",
    '{"event":"apnea_alarm"}': "Apnea Alarm",
    '{"event":"antisnoring"}': "Antisnoring",
    '{"event":"before_alarm"}': "Before Alarm",
    '{"event":"sound_event_snore"}': "Snore Detected",
    '{"event":"sound_event_talk"}': "Talk Detected",
    '{"event":"sound_event_cough"}': "Cough Detected",
    '{"event":"sound_event_baby"}': "Baby Cry Detected",
    '{"event":"sound_event_laugh"}': "Laugh Detected",
    '{"event":"alarm_rescheduled"}': "Alarm Rescheduled"
}

# Sound mapping
SOUND_MAPPING = {
    '{"event":"sound_event_snore"}': "Snore Detected",
    '{"event":"sound_event_talk"}': "Talk Detected",
    '{"event":"sound_event_cough"}': "Cough Detected",
    '{"event":"sound_event_baby"}': "Baby Cry Detected",
    '{"event":"sound_event_laugh"}': "Laugh Detected",
}

# Disturbance mapping
DISTURBANCE_MAPPING = {
    '{"event":"apnea_alarm"}': "Apnea Alarm",
    '{"event":"antisnoring"}': "Antisnoring",
}

# Alarm event mapping
ALARM_EVENT_MAPPING = {
    '{"event":"before_alarm"}': "Before Alarm",
    '{"event":"alarm_snooze_clicked"}': "Alarm Snoozed",
    '{"event":"alarm_snooze_canceled"}': "Snooze Canceled",
    '{"event":"time_to_bed_alarm_alert"}': "Time To Bed Alarm Alert",
    '{"event":"alarm_alert_start"}': "Alarm Alert Started",
    '{"event":"alarm_alert_dismiss"}': "Alarm Dismissed",
    '{"event":"alarm_skip_next"}': "Skip Next Alarm",
    '{"event":"show_skip_next_alarm"}': "Show Skip Next Alarm",
    '{"event":"rem"}': "REM",
    '{"event":"smart_period"}': "Smart Period",
    '{"event":"before_smart_period"}': "Before Smart Period",
}

# Sleep tracking event mapping
SLEEP_TRACKING_MAPPING = {
    '{"event":"sleep_tracking_started"}': "Sleep Tracking Started",
    '{"event":"sleep_tracking_stopped"}': "Sleep Tracking Stopped",
    '{"event":"sleep_tracking_paused"}': "Sleep Tracking Paused",
    '{"event":"sleep_tracking_resumed"}': "Sleep Tracking Resumed",
}