<p align="center">
  <a href="https://hacs.xyz/docs/faq/custom_repositories">
    <img src="https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge&logo=home%20assistant&labelColor=202020&color=41BDF5" alt="Add to HACS">
  </a>
</p>

<h1>🌙 SAAS - Sleep As Android Status</h1>

<h2>📖 Description:</h2>
<p>
Sleep As Android Status is my solution for wake/sleep state within HA. It listens for the Sleep As Android MQTT Messages, so it does require being on the same network. As of 0.0.4 Buttons that link with the Companion app have been added.
</p>

<h4>💡 This integration works best with a Xioami MiBand (7 or older) mixed with the Notify app and Sleep As Android configured.</h4>

<h3>🧱 This integration will create:</h3>

<ul>
  <li>
    <details>
      <summary><strong>📡 8 Sensors</strong></summary>
      <ul>
        <li>Message Received *State</li>
        <li>Wake Status</li>
        <li>Sound</li>
        <li>Disturbance</li>
        <li>Alarm</li>
        <li>Lullaby</li>
        <li>Sleep Tracking</li>
        <li>Sleep Stage</li>
      </ul>
      <p>This should intelligently and dynamically allow for state changes in the Wake Status Sensor.</p>
    </details>
  </li>
  <li>
    <details>
      <summary><strong>🎛️ 8 Buttons</strong></summary>
      <ul>
        <li>Alarm Dismiss</li>
        <li>Alarm Snooze</li>
        <li>Lullaby Stop</li>
        <li>Sleep Tracking Pause</li>
        <li>Sleep Tracking Resume</li>
        <li>Sleep Tracking Start</li>
        <li>Sleep Tracking Start with Optimal Alarm</li>
        <li>Sleep Tracking Stop</li>
      </ul>
    </details>
  </li>
  <li>
    <details>
      <summary><strong>🛠️ 1 Service</strong></summary>
      <pre>
service: saas.saas_example_alarm_set
data:
  message: Example Message!
  day: monday
  hour: 7
  minute: 30
      </pre>
    </details>
  </li>
  <li>
    <details>
      <summary><strong>🔗 1 Device per user</strong></summary>
      <p>One HA device is created per configured user instance to link sensors, services, and buttons.</p>
    </details>
  </li>
</ul>

<details>
  <summary><strong>✅ Known working</strong></summary>
  <ul>
    <li>📟 Xioami Mi Band 7</li>
    <li>📟 Xioami Mi Band 8 and 9 may work, but they have a different OS that jumps through hoops to work.</li>
    <li>⌚ Garmin Fenix 7X with Garmin Alternative, <b>NOT</b> the free one.</li>
    <li>⌚ Xioami Amazfit GTR Mini — may require root. I am rooted so I just did what's in this guide, but there may be alternative ways to get the key.</li>
  </ul>
</details>

<h2>🧪 Installation:</h2>
<ul>
  <li>Add https://www.github.com/sudoxnym/saas to your Custom Repositories in HACS</li>
  <li>Search and Download SAAS - Sleep As Android Status</li>
  <li>Restart Home Assistant</li>
  <li>
    <a href="https://my.home-assistant.io/redirect/config_flow_start/?domain=saas">
      <img src="https://my.home-assistant.io/badges/config_flow_start.svg" alt="Add to HA">
    </a>
  </li>
  <li>Add Integration: SAAS - Sleep As Android Status</li>
</ul>

<h2>⚙️ Configuration:</h2>
<ul>
  <li>Name: Name of user</li>
  <li>Topic: MQTT Topic from Sleep As Android</li>
  <li>QoS: Quality of Service</li>
  <li>Awake Duration: Time in seconds in which awake states = true to indicate awake. <s>Sensor usually updates within 30 seconds or so after the duration, not entirely sure why the delay.</s> <b>FIXED</b></li>
  <li>Asleep Duration: Time in seconds in which sleep states = true to indicate asleep. <s>Sensor usually updates within 30 seconds or so after the duration, not entirely sure why the delay.</s> <b>FIXED</b></li>
  <li>Awake States: States to indicate being awake</li>
  <li>Asleep States: States to indicate being asleep</li>
  <li>Mobile App: Target for buttons <b>REQUIRES COMPANION APP</b></li>
</ul>

<details>
<summary><strong>📲 Set Up Notify for Mi Band 7</strong></summary>
<ol>
  <li>Pair MiBand 7 as you normally would with <a href="https://play.google.com/store/apps/details?id=com.xiaomi.wearable&hl=en_US">Mi Fitness</a></li>
  <li>Obtain auth key for Notify app using ADB</li>
</ol>

<pre>
adb shell
grep -E "authKey=[a-z0-9]*," /sdcard/Android/data/com.xiaomi.wearable/files/log/XiaomiFit.device.log |
awk -F ", " '{print $17}' | grep authKey | tail -1 | awk -F "=" '{print $2}'
</pre>

<p>Credit: <a href="https://www.reddit.com/r/miband/comments/15j0rfq/comment/kxlyzc6/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button">iamfosscad</a></p>

<ol start="3">
  <li>Uninstall Mi Fitness</li>
  <li>Download/Install <a href="https://play.google.com/store/apps/details?id=com.mc.miband1&hl=en_US">Notify for Mi Band</a></li>
  <li>Follow prompts, input auth key, select Mi Fitness is not installed</li>
  <li>Enable Sleep as Android in Notify settings</li>
</ol>
</details>

<details>
<summary><strong>🔐 Extracting the Zepp <code>authKey</code> on a Rooted Android Device</strong></summary>
<pre>
su
cd /data/data/com.huami.watch.hmwatchmanager/databases/
ls origin_db_*
sqlite3 origin_db_1234567890 "SELECT AUTHKEY FROM DEVICE;"
</pre>

<ul>
  <li>⚠️ Do Not Unpair before extracting</li>
  <li>Use with caution – root required</li>
  <li>Modified apps are available on <a href="https://geekdoing.com">GeekDoing</a> and <a href="https://freemyband.com">freemyband.com</a></li>
</ul>
</details>

<h3>🛌 <a href="https://play.google.com/store/apps/details?id=com.urbandroid.sleep&hl=en_US">Sleep as Android Setup</a></h3>
<ol>
  <li>Open the app and follow setup</li>
  <li>Settings wheel > Services > Automation > MQTT</li>
</ol>

<pre>
(tcp/ssl)://(MQTT User):(MQTT Pass)@(HA URL):(port)
</pre>

<ul>
  <li>Topic: must match config</li>
  <li>Client ID: any unique ID</li>
</ul>

<ol start="4">
  <li>Enable automatic tracking</li>
  <li>Sensor: Sonar or Accelerometer</li>
  <li>Wearables > Xiaomi Mi Band > Test sensor</li>
</ol>

<details>
  <summary><strong>📦 Changes</strong></summary>
  <b>0.0.6a</b>
  <ul>
    <li>Initial Beta Release</li>
    <li>Added persistent states</li>
    <li>Alarm Event sensor attributes</li>
  </ul>

  <b>0.1.0</b>
  <ul>
    <li>Fixed Wake Status Timing</li>
    <li>Bug fixes on Sound sensor</li>
    <li>Accurate updates to AlarmEvent, Disturbance, Sound</li>
    <li>Organized README</li>
  </ul>
</details>

<details>
  <summary><strong>🚨 Known Issues</strong></summary>
  <pre>
Logger: homeassistant.helpers.service
Source: /usr/src/homeassistant/homeassistant/helpers/service.py:708
Failed to load integration: saas
NoneType: None
  </pre>
  <p>💬 No known effects. Just an error message, everything works as expected.</p>
  <p>This is my first integration.</p>
</details>
