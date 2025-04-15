<p align="center">
  <a href="https://hacs.xyz/docs/faq/custom_repositories">
    <img src="https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge&logo=home%20assistant&labelColor=202020&color=41BDF5" alt="add to hacs">
  </a>
</p>

<h1>🌙 saas - Sleep As Android status</h1>

<h2>🚨 breaking changes 🚨</h2>  
due to changes in **Home Assistant** 2025.12, you **must** remove your existing **SAAS** integration entries and re-add them after updating to this version.

---

<h2>📖 description:</h2>
<p>
sleep as android status is my solution for wake/sleep state within HA. it listens for the Sleep As Android MQTT messages, so it does require being on the same network. as of 0.0.4, buttons that link with the companion app have been added.
</p>

<h4>💡 this integration works best with a **Xiaomi Mi Band** (7 or older) mixed with the notify app and Sleep As Android configured.</h4>

<h3>🧱 this integration will create:</h3>

<ul>
  <li>
    <details>
      <summary><strong>📡 8 sensors</strong></summary>
      <ul>
        <li>message received *state*</li>
        <li>wake status</li>
        <li>sound</li>
        <li>disturbance</li>
        <li>alarm</li>
        <li>lullaby</li>
        <li>sleep tracking</li>
        <li>sleep stage</li>
      </ul>
      <p>this should intelligently and dynamically allow for state changes in the wake status sensor.</p>
    </details>
  </li>
  <li>
    <details>
      <summary><strong>🎛️ 8 buttons</strong></summary>
      <ul>
        <li>alarm dismiss</li>
        <li>alarm snooze</li>
        <li>lullaby stop</li>
        <li>sleep tracking pause</li>
        <li>sleep tracking resume</li>
        <li>sleep tracking start</li>
        <li>sleep tracking start with optimal alarm</li>
        <li>sleep tracking stop</li>
      </ul>
    </details>
  </li>
  <li>
    <details>
      <summary><strong>🛠️ 1 service</strong></summary>
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
      <summary><strong>🔗 1 device per user</strong></summary>
      <p>one HA device is created per configured user instance to link sensors, services, and buttons.</p>
    </details>
  </li>
</ul>

<details>
  <summary><strong>✅ known working</strong></summary>
  <ul>
    <li>📟 **Xiaomi Mi Band 7**</li>
    <li>📟 **Xiaomi Mi Band 8** and **Mi Band 9** may work, but they have a different os that jumps through hoops to work.</li>
    <li>⌚ **Garmin Fenix 7X** with garmin alternative, **not** the free one.</li>
    <li>⌚ **Xiaomi Amazfit GTR Mini** — may require root. i am rooted so i just did what's in this guide, but there may be alternative ways to get the key.</li>
  </ul>
</details>

<h2>🧪 installation:</h2>
<ul>
  <li>add <code>https://www.github.com/sudoxnym/saas</code> to your custom repositories in HACS</li>
  <li>search and download **SAAS - Sleep As Android status**</li>
  <li>restart Home Assistant</li>
  <li>
    <a href="https://my.home-assistant.io/redirect/config_flow_start/?domain=saas">
      <img src="https://my.home-assistant.io/badges/config_flow_start.svg" alt="add to ha">
    </a>
  </li>
  <li>add integration: **SAAS - Sleep As Android status**</li>
</ul>

<h2>⚙️ configuration:</h2>
<ul>
  <li>name: name of user</li>
  <li>topic: MQTT topic from Sleep As Android</li>
  <li>qos: quality of service</li>
  <li>awake duration: time in seconds in which awake states = true to indicate awake. <b>fixed</b></li>
  <li>asleep duration: time in seconds in which sleep states = true to indicate asleep. <b>fixed</b></li>
  <li>awake states: states to indicate being awake</li>
  <li>asleep states: states to indicate being asleep</li>
  <li>mobile app: target for buttons <b>requires companion app</b></li>
</ul>

<details>
  <summary><strong>📲 set up Notify for Mi Band 7</strong></summary>
  <ol>
    <li>pair **Mi Band 7** as you normally would with <a href="https://play.google.com/store/apps/details?id=com.xiaomi.wearable&hl=en_US">Mi Fitness</a></li>
    <li>obtain auth key for Notify app using ADB</li>
  </ol>

  <pre>
adb shell
grep -E "authKey=[a-z0-9]*," /sdcard/Android/data/com.xiaomi.wearable/files/log/XiaomiFit.device.log |
awk -F ", " '{print $17}' | grep authKey | tail -1 | awk -F "=" '{print $2}'
  </pre>

  <p>credit: <a href="https://www.reddit.com/r/miband/comments/15j0rfq/comment/kxlyzc6/">iamfosscad</a></p>

  <ol start="3">
    <li>uninstall **Mi Fitness**</li>
    <li>download/install <a href="https://play.google.com/store/apps/details?id=com.mc.miband1&hl=en_US">Notify for Mi Band</a></li>
    <li>follow prompts, input auth key, select Mi Fitness is not installed</li>
    <li>enable Sleep As Android in Notify settings</li>
  </ol>
</details>

<details>
  <summary><strong>🔐 extracting the Zepp <code>authKey</code> on a rooted android device</strong></summary>
  <pre>
su
cd /data/data/com.huami.watch.hmwatchmanager/databases/
ls origin_db_*
sqlite3 origin_db_1234567890 "SELECT AUTHKEY FROM DEVICE;"
  </pre>

  <ul>
    <li>⚠️ do not unpair before extracting</li>
    <li>use with caution – root required</li>
    <li>modified apps are available on <a href="https://geekdoing.com">GeekDoing</a> and <a href="https://freemyband.com">FreeMyBand</a></li>
  </ul>
</details>

<h3>🛌 <a href="https://play.google.com/store/apps/details?id=com.urbandroid.sleep&hl=en_US">sleep as android setup</a></h3>
<ol>
  <li>open the app and follow setup</li>
  <li>settings wheel > services > automation > MQTT</li>
</ol>

<pre>
(tcp/ssl)://(MQTT User):(MQTT Pass)@(HA URL):(port)
</pre>

<ul>
  <li>topic: must match config</li>
  <li>client id: any unique id</li>
</ul>

<ol start="4">
  <li>enable automatic tracking</li>
  <li>sensor: sonar or accelerometer</li>
  <li>wearables > **Xiaomi Mi Band** > test sensor</li>
</ol>

<details>
  <summary><strong>📦 changes</strong></summary>
  <b>0.2.0</b>
  <ul>
    <li>added services.yaml to resolve known NoneType error</li>
    <li>fixed deprecation warnings for future Home Assistant releases</li>
    <li>breaking changes: remove and re-add existing integration entries after update</li>
  </ul>

  <b>0.1.0</b>
  <ul>
    <li>fixed wake status timing</li>
    <li>bug fixes on sound sensor</li>
    <li>accurate updates to alarmevent, disturbance, sound</li>
    <li>organized readme</li>
  </ul>

  <b>0.0.6a</b>
  <ul>
    <li>initial beta release</li>
    <li>added persistent states</li>
    <li>alarm event sensor attributes</li>
  </ul>
</details>

<details>
  <summary><strong>🚨 known issues</strong></summary>
  <p>💬 no known issues at this time.</p>
</details>
