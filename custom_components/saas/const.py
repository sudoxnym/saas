"""Constants for the SAAS - Sleep As Android Stats integration."""

DOMAIN = "saas"

INTEGRATION_NAME = "SAAS - Sleep As Android Stats"
MODEL = "SAAS - Version 0.0.1"

CONF_NAME = "name" # Name of the Integration
CONF_TOPIC = "topic_template"   # MQTT Topic for Sleep As Android Events
CONF_QOS = "qos"    # Quality of Service
CONF_AWAKE_DURATION = "awake_duration" # Awake Duration
CONF_ASLEEP_DURATION = "asleep_duration"  # Asleep Duration
CONF_AWAKE_STATES = "awake_states"  # Awake States
CONF_SLEEP_STATES = "sleep_states" # Sleep States

DEFAULT_AWAKE_DURATION = 10 # Default Awake Duration
DEFAULT_ASLEEP_DURATION = 10    # Default Asleep Duration
DEFAULT_AWAKE_STATES = ["awake", "sleep_tracking_started"] # Default Awake States
DEFAULT_SLEEP_STATES = ["not_awake", "rem", "light_sleep", "deep_sleep", "sleep_tracking_stopped"]    # Default Sleep States

SENSOR_TYPES = {
    "received": {"name": "State", "device_class": None},
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