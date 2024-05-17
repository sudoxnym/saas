[![Add to HACS](https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge&logo=home%20assistant&labelColor=202020&color=41BDF5)](https://hacs.xyz/docs/faq/custom_repositories)<br>
<h1>SAAS - Sleep As Android Status</h1>
<h2>Description:</h2></br>
Sleep As Android Status is my solution for wake/sleep state within HA. It listens for the Sleep As Android MQTT Messages, so it does require being on the same network. As of 0.0.4 Buttons that link with the Companion app have been added.</br></br>
<h3>This integration works best with a Xioami MiBand (7 or older) mixed with the Notify app and Sleep As Android configured.</h3>

<h3>This integration will create 8 Sensors, 8 Buttons, 1 service, and 1 device per user:</h3></br>

<h3>Sensors</h3>
Message Received *State</br>
Wake Status</br>
Sound</br>
Disturbance</br>
Alarm</br>
Lullaby</br>
Sleep Tracking</br>
Sleep Statge</br>

This should intelligently and dynamically allow for state changes in the Wake Status Sensor.</br></br>

<h3>Buttons</h3>
Alarm Dismiss</br>
Alarm Snooze</br>
Lullaby Stop</br>
Sleep Tracking Pause</br>
Sleep Tracking Resum</br>
Sleep Tracking Start</br>
Sleep Tracking Start with Optimal Alarm</br>
Sleep Tracking Stop</br>

<h3>Service</h3>
Set alarm service</br>
<pre>
service: saas.saas_example_alarm_set
data:
  message: Example Message!
  day: monday
  hour: 7
  minute: 30
</pre>






<h2>Installation:</h2>


  &nbsp;&nbsp;Add https://www.github.com/sudoxnym/saas to your Custom Repositories in HACS</br>
  
  &nbsp;&nbsp;Search and Download SAAS - Sleep As Android Status</br>
  &nbsp;&nbsp;Restart Home Assistant</br>
  &nbsp;&nbsp;[![Add To My Home Assistant](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=saas)<br>
  &nbsp;&nbsp;Add Integration: SAAS - Sleep As Android Status</br></br>


<h2>Configuration:</h3>

  &nbsp;&nbsp;Name: Name of user</br>
  &nbsp;&nbsp;Topic: MQTT Topic from Sleep As Android</br>
  &nbsp;&nbsp;QoS: Quality of Service</br></br>

  &nbsp;&nbsp;Awake Duration: This is for tuning. Time in seconds in which awake states = true to indicate awake. Sensor usually updates within 30 seconds or so after the duration, not entirely sure why the delay.</br>
  &nbsp;&nbsp;Asleep Duration: This is for tuning. Time in seconds in which sleep states = true to indicate asleep Sensor usually updates within 30 seconds or so after the duration, not entirely sure why the delay.</br>
  &nbsp;&nbsp;Awake States: States to indicate being awake</br>
  &nbsp;&nbsp;Asleep States: States to indicate being asleep</br>
  &nbsp;&nbsp;Mobile App: Target for buttons </br></br>

Please report any issues.</br>
This is my first integration.
Built this in less than a week, with no prior knowledge of Python.
