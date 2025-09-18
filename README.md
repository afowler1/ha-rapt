# RAPT Device Integration for Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)
[![GitHub release (latest by date)](https://img.shields.io/github/v/release/afowler1/ha-rapt)](https://github.com/afowler1/ha-rapt/releases)

This custom Home Assistant integration provides a **read-only** interface for RAPT devices through the RAPT portal API. Monitor your fermentation temperatures, specific gravity, chamber controls, and device diagnostics directly in Home Assistant.

## ⚠️ Important Safety Disclaimer

**THIS INTEGRATION IS READ-ONLY AND WILL NEVER SUPPORT WRITE OPERATIONS**

According to [RAPT's official API documentation](https://docs.rapt.io/integrations/api-secrets):
- **API access is unsupported** - KegLand will not provide assistance with API-related issues
- **Misuse can brick your devices** - Incorrect API usage can destroy devices and void your warranty
- **All API requests are tracked** - KegLand monitors all API activity
- **Severe abuse results in permanent bans** - Your devices could become "all but useless"

This integration is designed to be **completely safe** by only reading device data, never sending commands or changing settings. However, you use this integration **at your own risk**.

**Supported Devices:**
- **Temperature Controllers**: Basic temperature monitoring and control diagnostics
- **Hydrometers**: Specific gravity tracking, temperature readings, and fermentation monitoring  
- **Fermentation Chambers**: Advanced temperature control with heating/cooling systems, PID controls, compressor management, and comprehensive diagnostics
- **BrewZillas**: Professional brewing systems with pump control, distillation mode, temperature management, and extensive brewing-specific features

## Features

## Features

### 🛡️ Safety First
- **100% Read-Only**: No write operations - cannot damage or brick your devices
- **No Control Commands**: Only monitors data, never sends control signals
- **Safe by Design**: Impossible to void warranties through integration misuse

### 📊 Monitoring Capabilities
- 🌡️ **Temperature Monitoring**: Real-time temperature readings from all RAPT device types
- 🎯 **Target Temperature Control**: Monitor set temperature targets and ranges (controllers & chambers)
- 🔥 **Heating/Cooling Systems**: View utilization, runtime, and cycle counts (controllers & chambers)
- 📊 **Specific Gravity Tracking**: Monitor specific gravity and gravity velocity (hydrometers)
- 🔋 **Battery Monitoring**: Track hydrometer battery levels
- ⚙️ **Advanced Chamber Controls**: PID settings, compressor management, auxiliary systems (fermentation chambers)
- � **Temperature Alarms**: Monitor high/low temperature alarm settings (chambers)
- �📊 **Runtime Statistics**: Track heating, cooling, compressor, and total runtime across all devices
- 📡 **Connection Monitoring**: Device connection status and signal strength
- ℹ️ **Comprehensive Diagnostics**: Firmware versions, system states, and device configuration
- 🏠 **Multi-Device Support**: Automatically discovers all RAPT devices (controllers, hydrometers, chambers)
- 🔄 **Automatic Token Management**: Handles authentication and token refresh automatically
- ⚡ **Optimized Performance**: Efficient API usage with 60-second update intervals
- 🔒 **Secure Storage**: API secrets stored using Home Assistant's secure storage system

## Prerequisites

Before installing this integration, you need to:

1. Have a RAPT account at [app.rapt.io](https://app.rapt.io)
2. Own one or more RAPT devices (temperature controllers, hydrometers, fermentation chambers, or BrewZillas)
3. Generate an API secret from your RAPT account

### Getting Your API Secret

1. Log into your RAPT account at [https://app.rapt.io](https://app.rapt.io)
2. Navigate to **Account** → **API Secrets**
3. Click **Generate New API Secret**
4. Give your secret a meaningful name (e.g., "Home Assistant Integration")
5. Copy the generated API secret - you'll need this during setup
6. **Important**: Save this secret securely as it won't be shown again

## Installation

### Method 1: HACS (Recommended)

1. **Install HACS** if you haven't already:
   - Follow the [HACS installation guide](https://hacs.xyz/docs/setup/prerequisites)

2. **Add Custom Repository**:
   - In Home Assistant, go to **HACS** → **Integrations**
   - Click the three dots menu (⋮) → **Custom repositories**
   - Add repository URL: `https://github.com/afowler1/ha-rapt`
   - Category: **Integration**
   - Click **Add**

3. **Install the Integration**:
   - Search for "RAPT Devices" in HACS
   - Click **Download**
   - Restart Home Assistant

4. **Configure the Integration**:
   - Go to **Settings** → **Devices & Services**
   - Click **Add Integration**
   - Search for "RAPT Devices"
   - Enter your API secret when prompted
   - Click **Submit**
   
   ⚠️ **Remember**: This integration is read-only and safe - it cannot modify your device settings or cause any damage.

### Method 2: Manual Installation

1. **Download the Integration**:
   ```bash
   # Clone or download this repository
   git clone https://github.com/afowler1/ha-rapt.git
   ```

2. **Copy Files**:
   - Copy the `custom_components/rapt` folder to your Home Assistant's `custom_components` directory
   - Your directory structure should look like:
   ```
   config/
   ├── custom_components/
   │   └── rapt/
   │       ├── __init__.py
   │       ├── manifest.json
   │       ├── config_flow.py
   │       ├── coordinator.py
   │       ├── api.py
   │       ├── sensor.py
   │       ├── const.py
   │       └── strings.json
   └── configuration.yaml
   ```

3. **Restart Home Assistant**

4. **Configure the Integration**:
   - Go to **Settings** → **Devices & Services**
   - Click **Add Integration**
   - Search for "RAPT Devices"
   - Enter your API secret when prompted

## Configuration

### Initial Setup

1. **Add Integration**:
   - Navigate to **Settings** → **Devices & Services**
   - Click **Add Integration**
   - Search for "RAPT Devices"

2. **Enter API Secret**:
   - Paste your API secret from the RAPT portal
   - Click **Submit**

3. **Verify Connection**:
   - The integration will test the connection to RAPT's API
   - If successful, your temperature controller devices will appear

### Configuration Options

The integration automatically discovers your RAPT temperature controllers. No additional configuration is required after the initial setup.

## How It Works

Once configured, the RAPT integration will:

1. **Automatically discover** all RAPT devices associated with your account (controllers, hydrometers, fermentation chambers, BrewZillas)
2. **Create sensors** for each device with comprehensive measurements and diagnostics
3. **Update data** every 60 seconds (optimized for comprehensive device support)
4. **Handle authentication** token refresh automatically (tokens expire after 50 minutes)

### Device Discovery

The integration supports dynamic device discovery:

- **Initial Setup**: All existing devices are discovered during integration setup
- **New Devices**: Automatically detected during regular update cycles
- **Manual Discovery**: Use the `rapt.discover_devices` service to immediately scan for new devices

To manually trigger device discovery:
1. Go to **Developer Tools** → **Services** in Home Assistant
2. Select the `rapt.discover_devices` service
3. Click **Call Service**

## Available Entities

### Temperature Controller Sensors

| Entity | Description | Unit | Device Class |
|--------|-------------|------|--------------|
| `sensor.rapt_controller_temperature` | Current temperature reading | °C | Temperature |
| `sensor.rapt_controller_target_temperature` | Target/setpoint temperature | °C | Temperature |
| `sensor.rapt_controller_heating_utilization` | Heating utilization percentage | % | Power Factor |
| `sensor.rapt_controller_connection_status` | Device connection state | - | Diagnostic |
| `sensor.rapt_controller_signal_strength` | WiFi signal strength | dBm | Signal Strength |
| `sensor.rapt_controller_total_runtime` | Total device runtime | s | Duration |
| `sensor.rapt_controller_cooling_runtime` | Cooling runtime | s | Duration |
| `sensor.rapt_controller_heating_runtime` | Heating runtime | s | Duration |
| `sensor.rapt_controller_firmware_version` | Device firmware version | - | Diagnostic |

### Hydrometer Sensors

| Entity | Description | Unit | Device Class |
|--------|-------------|------|--------------|
| `sensor.rapt_hydrometer_temperature` | Current temperature reading | °C | Temperature |
| `sensor.rapt_hydrometer_gravity` | Specific gravity reading | - | - |
| `sensor.rapt_hydrometer_gravity_velocity` | Rate of gravity change | - | - |
| `sensor.rapt_hydrometer_battery` | Battery level | % | Battery |
| `sensor.rapt_hydrometer_signal_strength` | WiFi signal strength | dBm | Signal Strength |
| `sensor.rapt_hydrometer_firmware_version` | Device firmware version | - | Diagnostic |
| `sensor.rapt_hydrometer_paired_device_type` | Type of paired device | - | Diagnostic |
| `sensor.rapt_hydrometer_active_status` | Device active status | - | Diagnostic |

### Fermentation Chamber Sensors

| Entity | Description | Unit | Device Class |
|--------|-------------|------|--------------|
| `sensor.rapt_chamber_temperature` | Current temperature reading | °C | Temperature |
| `sensor.rapt_chamber_target_temperature` | Target/setpoint temperature | °C | Temperature |
| `sensor.rapt_chamber_min_target_temperature` | Minimum target temperature | °C | Temperature |
| `sensor.rapt_chamber_max_target_temperature` | Maximum target temperature | °C | Temperature |
| `sensor.rapt_chamber_heating_utilization` | Heating utilization percentage | % | Power Factor |
| `sensor.rapt_chamber_total_runtime` | Total device runtime | s | Duration |
| `sensor.rapt_chamber_cooling_runtime` | Cooling system runtime | s | Duration |
| `sensor.rapt_chamber_heating_runtime` | Heating system runtime | s | Duration |
| `sensor.rapt_chamber_compressor_runtime` | Compressor runtime | s | Duration |
| `sensor.rapt_chamber_auxiliary_runtime` | Auxiliary system runtime | s | Duration |
| `sensor.rapt_chamber_cooling_starts` | Number of cooling cycles | - | - |
| `sensor.rapt_chamber_heating_starts` | Number of heating cycles | - | - |
| `sensor.rapt_chamber_compressor_starts` | Number of compressor cycles | - | - |
| `sensor.rapt_chamber_auxiliary_starts` | Number of auxiliary cycles | - | - |
| `sensor.rapt_chamber_high_temp_alarm` | High temperature alarm setting | °C | Temperature |
| `sensor.rapt_chamber_low_temp_alarm` | Low temperature alarm setting | °C | Temperature |
| `sensor.rapt_chamber_connection_status` | Device connection state | - | Diagnostic |
| `sensor.rapt_chamber_status` | Device operational status | - | Diagnostic |
| `sensor.rapt_chamber_signal_strength` | WiFi signal strength | dBm | Signal Strength |
| `sensor.rapt_chamber_firmware_version` | Device firmware version | - | Diagnostic |
| `sensor.rapt_chamber_pid_enabled` | PID control status | - | Diagnostic |
| `sensor.rapt_chamber_pid_proportional` | PID proportional value | - | Diagnostic |
| `sensor.rapt_chamber_pid_integral` | PID integral value | - | Diagnostic |
| `sensor.rapt_chamber_pid_derivative` | PID derivative value | - | Diagnostic |
| `sensor.rapt_chamber_cooling_enabled` | Cooling system status | - | Diagnostic |
| `sensor.rapt_chamber_heating_enabled` | Heating system status | - | Diagnostic |
| `sensor.rapt_chamber_fan_enabled` | Fan system status | - | Diagnostic |
| `sensor.rapt_chamber_light_setting` | Light control setting | - | Diagnostic |
| `sensor.rapt_chamber_control_device_type` | External sensor type | - | Diagnostic |
| `sensor.rapt_chamber_control_device_temperature` | External sensor temperature | °C | Temperature |

## Usage Examples

### Basic Temperature Monitoring

Monitor your fermentation temperature:

```yaml
# Example automation: Alert when temperature is out of range
automation:
  - alias: "RAPT Temperature Alert"
    trigger:
      - platform: numeric_state
        entity_id: sensor.rapt_device_temperature
        above: 22
    action:
      - service: notify.mobile_app_your_phone
        data:
          message: "Fermentation temperature is {{ states('sensor.rapt_device_temperature') }}°C - above target!"
```

### Dashboard Card

Create a temperature monitoring card:

```yaml
# Example Lovelace card
type: entities
title: Fermentation Monitor
entities:
  - sensor.rapt_device_temperature
  - sensor.rapt_device_target_temperature
  - sensor.rapt_device_heating_status
  - sensor.rapt_device_cooling_status
```

### Temperature History Chart

```yaml
# Example history graph card
type: history-graph
title: Temperature History
hours_to_show: 24
entities:
  - sensor.rapt_device_temperature
  - sensor.rapt_device_target_temperature
```

## API Rate Limits

The integration respects RAPT's API rate limits:
- **Update Interval**: 60 seconds between requests
- **API Limit**: 4 requests per minute (we use 1 per minute to be safe)
- **Token Validity**: 50 minutes (auto-refreshed at 45 minutes)

## Troubleshooting

### Common Issues

1. **"Invalid API Secret" Error**:
   - Verify your API secret is correct
   - Ensure you copied the full secret without extra spaces
   - Try generating a new API secret

2. **"Cannot Connect" Error**:
   - Check your internet connection
   - Verify RAPT services are online at [status.rapt.io](https://status.rapt.io)
   - Check Home Assistant logs for detailed error messages

3. **No Sensor Data**:
   - Ensure your RAPT device is online and sending data
   - Check that you have temperature controller devices (not just hydrometers)
   - Wait a few minutes for the first data update

4. **Entities Not Appearing**:
   - Restart Home Assistant after installation
   - Check **Settings** → **Devices & Services** → **RAPT Temperature Controller**
   - Look for error messages in the Home Assistant logs

### Enable Debug Logging

To get detailed logs for troubleshooting:

1. Add to your `configuration.yaml`:
   ```yaml
   logger:
     logs:
       custom_components.rapt: debug
   ```

2. Restart Home Assistant
3. Check **Settings** → **System** → **Logs** for detailed debug information

### Getting Help

If you're still having issues:

1. Check the [GitHub Issues](https://github.com/yourusername/ha-rapt-integration/issues) for similar problems
2. Enable debug logging and include relevant log entries
3. Create a new issue with:
   - Home Assistant version
   - Integration version
   - Error messages from logs
   - Steps to reproduce the issue

## Security & Privacy

- **API Secret Storage**: Your API secret is stored securely using Home Assistant's encrypted storage
- **Data Usage**: This integration only reads data from RAPT - it cannot control your devices
- **Network Traffic**: All communication is encrypted HTTPS to RAPT's servers
- **No External Dependencies**: No data is sent to third parties

## Limitations

- **Read-Only**: This integration cannot control your RAPT devices, only monitor them
- **Internet Required**: Requires internet connection to access RAPT's cloud API
- **RAPT Service Dependency**: Integration availability depends on RAPT's service uptime
- **Rate Limited**: Updates are limited to every 60 seconds to respect API limits

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Thanks to RAPT for providing the API
- Home Assistant community for integration development resources

## Changelog

### v1.0.0
- Initial release
- Basic temperature controller monitoring
- Automatic token management
- Rate-limited API calls
- HACS compatibility