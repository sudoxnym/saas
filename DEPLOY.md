# 🧪 Deploying SAAS - Sleep As Android Status via HACS

## 🛠️ Pre-requisites

- Home Assistant (2023.x or newer recommended)
- HACS installed (https://hacs.xyz/)
- MQTT broker set up and working
- Android device running Sleep As Android

## 🚀 Installation Steps

1. In HACS, go to "Integrations"
2. Click the 3-dot menu > Custom repositories
3. Paste: `https://github.com/sudoxnym/saas`
4. Set Category to "Integration"
5. Click "Add"
6. Refresh, search for `SAAS - Sleep As Android Status`, and install
7. Restart Home Assistant
8. Go to Settings > Devices & Services > Add Integration > search "SAAS"
9. Configure the integration with your MQTT topic and states

## 🧪 Testing

- Trigger sleep/wake events from Sleep As Android
- Confirm sensor states update in Home Assistant
- Optional: Use HA Companion App to link button services

## 📄 More

See the [README](./README.md) for configuration, supported devices, and example automations.
