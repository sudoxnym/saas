[![Add to HACS](https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge&logo=home%20assistant&labelColor=202020&color=41BDF5)](https://hacs.xyz/docs/faq/custom_repositories)
<h1>SAAS - Sleep As Android Status</h1>
<h2>Description:</h2>
Sleep As Android Status is my solution for wake/sleep state within HA. It listens for the Sleep As Android MQTT Messages, so it does require being on the same network. As of 0.0.4 Buttons that link with the Companion app have been added.</br>
<h3>This integration works best with a Xioami MiBand (7 or older) mixed with the Notify app and Sleep As Android configured.</h3>
<h3>This integration will create 8 Sensors, 8 Buttons, 1 service, and 1 device per user:</h3>
<h3>Sensors</h3>
Message Received *State</br>
Wake Status</br>
Sound</br>
Disturbance</br>
Alarm</br>
Lullaby</br>
Sleep Tracking</br>
Sleep Statge</br></br>
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

Add https://www.github.com/sudoxnym/saas to your Custom Repositories in HACS</br>
  
Search and Download SAAS - Sleep As Android Status</br>
Restart Home Assistant</br>
[![Add To My Home Assistant](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=saas)<br>
Add Integration: SAAS - Sleep As Android Status</br></br>

<h2>Configuration:</h2>

Name: Name of user</br>
Topic: MQTT Topic from Sleep As Android</br>
QoS: Quality of Service</br></br>

Awake Duration: This is for tuning. Time in seconds in which awake states = true to indicate awake. <s>Sensor usually updates within 30 seconds or so after the duration, not entirely sure why the delay.</s> <b>FIXED</b></br>
Asleep Duration: This is for tuning. Time in seconds in which sleep states = true to indicate asleep. <s>Sensor usually updates within 30 seconds or so after the duration, not entirely sure why the delay.</s> <b>FIXED</b></br>
Awake States: States to indicate being awake</br>
Asleep States: States to indicate being asleep</br>
Mobile App: Target for buttons <b>REQUIRES COMPANION APP</b></br></br>

<h3>Set Up Notify for <a href="https://www.amazon.com/Xiaomi-Activity-Tracker-High-Res-Bluetooth/dp/B0B2DK5YCP">MiBand 7</a> (as of May 29, 2024)</h3>
1. Pair MiBand 7 as you normally would with <a href="https://play.google.com/store/apps/details?id=com.xiaomi.wearable&hl=en_US">Mi Fitness</a> app </br>
2. Obtain auth key for Notify app. Connect to pc with usb and open your adb <a href="https://developer.android.com/tools/releases/platform-tools">SDK Platform-Pools</a>, or if you're more advanced, connect wirelessly</br>
Windows:</br>
&nbsp;&nbsp;2a. Open folder with adb in it</br>
&nbsp;&nbsp;2b. Right click a blank spot within the folder</br>
&nbsp;&nbsp;2c. Open in terminal</br>
&nbsp;&nbsp;2d. <pre>./adb shell</pre>
&nbsp;&nbsp;2e. <pre>grep -E "authKey=[a-z0-9]*," /sdcard/Android/data/com.xiaomi.wearable/files/log/XiaomiFit.device.log |
awk -F ", " '{print $17}' | grep authKey | tail -1 | awk -F "=" '{print $2}'</pre>
&nbsp;&nbsp;2f. Copy/clipboard the output. Disconnect phone, close ADB.</br>
&nbsp;&nbsp;&nbsp;&nbsp; Credit: <a href="https://www.reddit.com/r/miband/comments/15j0rfq/comment/kxlyzc6/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button">iamfosscad</a></br>
3. Uninstall Mi Fitness
4. Download/Install <a href="https://play.google.com/store/apps/details?id=com.mc.miband1&hl=en_US">Notify for Mi Band (up to 7)</a></br>
5. Follow the prompts, enable any permission it asks for, create the profile, input Auth Key, and select Mi Fitness is not installed</br>
6. Open the hamburger menu on the top left</br>
7. Search > Search for "Sleep"</br>
8. Turn on Sleep as Android</br>
9. Choose the four squares in the upper right</br>
10. Scroll to and choose "Custom triggers"</br>
11. Turn on Fell Asleep and set to Sleep as Android - Start sleep tracking</br>
12. Turn on Awoke and set to Sleep as Android - Stop sleep tracking</br>
13. Enjoy</br></br>

<h3><a href="https://play.google.com/store/apps/details?id=com.urbandroid.sleep&hl=en_US">Sleep as Android</a></h3>
1. Open the app and follow setup</br>
2. Settings wheel in top right > Services > Automation</br>
3. MQTT</br>
&nbsp;&nbsp;3a. URL
<pre>(tcp/ssl)://(MQTT User):(MQTT Pass)@(HA URL):(port)</pre>
&nbsp;&nbsp;3b. Topic > something recognizable. You need this exact topic in HA Integration Config.</br>
&nbsp;&nbsp;3c. Client ID > I set the same, not sure if it should be, but it works.</br>
&nbsp;&nbsp;3d. Test > Wait for "Success" toast message</br>
4. Back to app settings > Sleep tracking > </br>
&nbsp;&nbsp;4a. Automatic Sleep Tracking > After fall asleep</br>
&nbsp;&nbsp;4b. Sensor > Sonar (if placing phone on a bedside table) Accelerometer (if placing on bed next to you)</br>
&nbsp;&nbsp;4c. Wearables ></br>
&nbsp;&nbsp;&nbsp;&nbsp;4c1. Wearables > Xiaomi Mi Band > Test sensor</br>
&nbsp;&nbsp;&nbsp;&nbsp;4c2. Heart rate monitoring (optional)</br>
&nbsp;&nbsp;4d. Pair tracking (optional)</br>
5. Enjoy (optional)</br></br>

<h2>Changes:</h2>
<b>0.0.6a</b></br>
Initial Beta Release</br>
Added persistant states through HA restart</br>
Added attributes for the Alarm Event sensor</br>
<b>0.1.0</b></br>
Fixed Wake Status Timing <b>(HUGE)</b></br>
Fixed bug with Sound sensor</br>
Modified AlarmEvent, Disturbance, and Sound sensors to update to None accurately</br>
Organized Readme.md</br>

<h2>Known issues:</h2>
Error in logs: 
<pre>
Logger: homeassistant.helpers.service
Source: /usr/src/homeassistant/homeassistant/helpers/service.py:708
First occurred: 3:55:19 PM (1 occurrences)
Last logged: 3:55:19 PM

Failed to load integration: saas
NoneType: None</pre>
No known effects. Just an error message, everything works as expected.
Please report any issues.</br>
This is my first integration.
