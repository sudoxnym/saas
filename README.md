[![Add to HACS](https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge&logo=home%20assistant&labelColor=202020&color=41BDF5)](https://hacs.xyz/docs/faq/custom_repositories)<br>
<h1>SAAS - Sleep As Android Status</h1>
<h4>Description:</h4></br>
Sleep As Android Status is my solution for wake/sleep state within HA. It listens for the Sleep As Android MQTT Messages, so it does require being on the same network.</br></br>

<h7>When finished this integration will create 7 entities and 1 device per user:</h7></br></br>
Message Received *State</br>
Wake Status</br>
Sound</br>
Disturbance</br>
Alarm</br>
Lullaby</br>
Sleep Tracking</br>


This should intelligently and dynamically allow for state changes in the Wake Status Sensor.</br></br>


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

  &nbsp;&nbsp;Awake Duration: Time in seconds in which awake states = true to indicate awake</br>
  &nbsp;&nbsp;Asleep Duration: Time in seconds in which sleep states = true to indicate asleep</br>
  &nbsp;&nbsp;Awake States: States to indicate being awake</br>
  &nbsp;&nbsp;Asleep States: States to indicate being asleep</br></br>

Please report any issues.</br>
This is my first integration.
Built this in less than a week, with no prior knowledge of Python.
