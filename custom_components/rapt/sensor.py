"""RAPT sensor platform."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    UnitOfTemperature, 
    PERCENTAGE, 
    UnitOfTime,
    EntityCategory,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import RaptDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)

CONTROLLER_SENSOR_DESCRIPTIONS = [
    SensorEntityDescription(
        key="temperature",
        name="Temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        suggested_display_precision=1,
    ),
    SensorEntityDescription(
        key="targetTemperature",
        name="Target Temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        suggested_display_precision=1,
    ),
    SensorEntityDescription(
        key="heatingUtilisation",
        name="Heating Utilization",
        device_class=SensorDeviceClass.POWER_FACTOR,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=PERCENTAGE,
        suggested_display_precision=1,
    ),
    SensorEntityDescription(
        key="connectionState",
        name="Connection Status",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDescription(
        key="rssi",
        name="Signal Strength",
        device_class=SensorDeviceClass.SIGNAL_STRENGTH,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement="dBm",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDescription(
        key="totalRunTime",
        name="Total Runtime",
        device_class=SensorDeviceClass.DURATION,
        state_class=SensorStateClass.TOTAL,
        native_unit_of_measurement=UnitOfTime.SECONDS,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDescription(
        key="coolingRunTime",
        name="Cooling Runtime",
        device_class=SensorDeviceClass.DURATION,
        state_class=SensorStateClass.TOTAL,
        native_unit_of_measurement=UnitOfTime.SECONDS,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDescription(
        key="heatingRunTime",
        name="Heating Runtime",
        device_class=SensorDeviceClass.DURATION,
        state_class=SensorStateClass.TOTAL,
        native_unit_of_measurement=UnitOfTime.SECONDS,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDescription(
        key="firmwareVersion",
        name="Firmware Version",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
]

HYDROMETER_SENSOR_DESCRIPTIONS = [
    SensorEntityDescription(
        key="temperature",
        name="Temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        suggested_display_precision=2,
    ),
    SensorEntityDescription(
        key="gravity",
        name="Specific Gravity",
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=5,
    ),
    SensorEntityDescription(
        key="gravityVelocity",
        name="Gravity Velocity",
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=6,
    ),
    SensorEntityDescription(
        key="battery",
        name="Battery Level",
        device_class=SensorDeviceClass.BATTERY,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=PERCENTAGE,
        suggested_display_precision=1,
    ),
    SensorEntityDescription(
        key="rssi",
        name="Signal Strength",
        device_class=SensorDeviceClass.SIGNAL_STRENGTH,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement="dBm",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDescription(
        key="firmwareVersion",
        name="Firmware Version",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDescription(
        key="pairedDeviceType",
        name="Paired Device Type",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDescription(
        key="active",
        name="Active Status",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
]

FERMENTATION_CHAMBER_SENSOR_DESCRIPTIONS = [
    SensorEntityDescription(
        key="temperature",
        name="Temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        suggested_display_precision=1,
    ),
    SensorEntityDescription(
        key="targetTemperature",
        name="Target Temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        suggested_display_precision=1,
    ),
    SensorEntityDescription(
        key="minTargetTemperature",
        name="Min Target Temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        suggested_display_precision=1,
    ),
    SensorEntityDescription(
        key="maxTargetTemperature",
        name="Max Target Temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        suggested_display_precision=1,
    ),
    SensorEntityDescription(
        key="heatingUtilisation",
        name="Heating Utilization",
        device_class=SensorDeviceClass.POWER_FACTOR,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=PERCENTAGE,
        suggested_display_precision=1,
    ),
    SensorEntityDescription(
        key="totalRunTime",
        name="Total Runtime",
        device_class=SensorDeviceClass.DURATION,
        state_class=SensorStateClass.TOTAL_INCREASING,
        native_unit_of_measurement=UnitOfTime.SECONDS,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDescription(
        key="coolingRunTime",
        name="Cooling Runtime",
        device_class=SensorDeviceClass.DURATION,
        state_class=SensorStateClass.TOTAL_INCREASING,
        native_unit_of_measurement=UnitOfTime.SECONDS,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDescription(
        key="heatingRunTime",
        name="Heating Runtime",
        device_class=SensorDeviceClass.DURATION,
        state_class=SensorStateClass.TOTAL_INCREASING,
        native_unit_of_measurement=UnitOfTime.SECONDS,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDescription(
        key="compressorRunTime",
        name="Compressor Runtime",
        device_class=SensorDeviceClass.DURATION,
        state_class=SensorStateClass.TOTAL_INCREASING,
        native_unit_of_measurement=UnitOfTime.SECONDS,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDescription(
        key="auxillaryRunTime",
        name="Auxiliary Runtime",
        device_class=SensorDeviceClass.DURATION,
        state_class=SensorStateClass.TOTAL_INCREASING,
        native_unit_of_measurement=UnitOfTime.SECONDS,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDescription(
        key="coolingStarts",
        name="Cooling Starts",
        state_class=SensorStateClass.TOTAL_INCREASING,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDescription(
        key="heatingStarts",
        name="Heating Starts",
        state_class=SensorStateClass.TOTAL_INCREASING,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDescription(
        key="compressorStarts",
        name="Compressor Starts",
        state_class=SensorStateClass.TOTAL_INCREASING,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDescription(
        key="auxillaryStarts",
        name="Auxiliary Starts",
        state_class=SensorStateClass.TOTAL_INCREASING,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDescription(
        key="highTempAlarm",
        name="High Temperature Alarm",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        suggested_display_precision=1,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDescription(
        key="lowTempAlarm",
        name="Low Temperature Alarm",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        suggested_display_precision=1,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDescription(
        key="connectionState",
        name="Connection Status",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDescription(
        key="status",
        name="Status",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDescription(
        key="rssi",
        name="Signal Strength",
        device_class=SensorDeviceClass.SIGNAL_STRENGTH,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement="dBm",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDescription(
        key="firmwareVersion",
        name="Firmware Version",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDescription(
        key="pidEnabled",
        name="PID Enabled",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDescription(
        key="pidProportional",
        name="PID Proportional",
        entity_category=EntityCategory.DIAGNOSTIC,
        suggested_display_precision=2,
    ),
    SensorEntityDescription(
        key="pidIntegral",
        name="PID Integral",
        entity_category=EntityCategory.DIAGNOSTIC,
        suggested_display_precision=2,
    ),
    SensorEntityDescription(
        key="pidDerivative",
        name="PID Derivative",
        entity_category=EntityCategory.DIAGNOSTIC,
        suggested_display_precision=2,
    ),
    SensorEntityDescription(
        key="coolingEnabled",
        name="Cooling Enabled",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDescription(
        key="heatingEnabled",
        name="Heating Enabled",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDescription(
        key="fanEnabled",
        name="Fan Enabled",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDescription(
        key="lightEnabled",
        name="Light Setting",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDescription(
        key="controlDeviceType",
        name="Control Device Type",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDescription(
        key="controlDeviceTemperature",
        name="Control Device Temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        suggested_display_precision=1,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
]

BREWZILLA_SENSOR_DESCRIPTIONS = [
    SensorEntityDescription(
        key="temperature",
        name="Temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        suggested_display_precision=1,
    ),
    SensorEntityDescription(
        key="targetTemperature",
        name="Target Temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        suggested_display_precision=1,
    ),
    SensorEntityDescription(
        key="minTargetTemperature",
        name="Min Target Temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        suggested_display_precision=1,
    ),
    SensorEntityDescription(
        key="maxTargetTemperature",
        name="Max Target Temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        suggested_display_precision=1,
    ),
    SensorEntityDescription(
        key="heatingUtilisation",
        name="Heating Utilization",
        device_class=SensorDeviceClass.POWER_FACTOR,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=PERCENTAGE,
        suggested_display_precision=1,
    ),
    SensorEntityDescription(
        key="pumpUtilisation",
        name="Pump Utilization",
        device_class=SensorDeviceClass.POWER_FACTOR,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=PERCENTAGE,
        suggested_display_precision=1,
    ),
    SensorEntityDescription(
        key="totalRunTime",
        name="Total Runtime",
        device_class=SensorDeviceClass.DURATION,
        state_class=SensorStateClass.TOTAL_INCREASING,
        native_unit_of_measurement=UnitOfTime.SECONDS,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDescription(
        key="coolingRunTime",
        name="Cooling Runtime",
        device_class=SensorDeviceClass.DURATION,
        state_class=SensorStateClass.TOTAL_INCREASING,
        native_unit_of_measurement=UnitOfTime.SECONDS,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDescription(
        key="heatingRunTime",
        name="Heating Runtime",
        device_class=SensorDeviceClass.DURATION,
        state_class=SensorStateClass.TOTAL_INCREASING,
        native_unit_of_measurement=UnitOfTime.SECONDS,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDescription(
        key="auxillaryRunTime",
        name="Auxiliary Runtime",
        device_class=SensorDeviceClass.DURATION,
        state_class=SensorStateClass.TOTAL_INCREASING,
        native_unit_of_measurement=UnitOfTime.SECONDS,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDescription(
        key="coolingStarts",
        name="Cooling Starts",
        state_class=SensorStateClass.TOTAL_INCREASING,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDescription(
        key="heatingStarts",
        name="Heating Starts",
        state_class=SensorStateClass.TOTAL_INCREASING,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDescription(
        key="auxillaryStarts",
        name="Auxiliary Starts",
        state_class=SensorStateClass.TOTAL_INCREASING,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDescription(
        key="highTempAlarm",
        name="High Temperature Alarm",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        suggested_display_precision=1,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDescription(
        key="lowTempAlarm",
        name="Low Temperature Alarm",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        suggested_display_precision=1,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDescription(
        key="connectionState",
        name="Connection Status",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDescription(
        key="status",
        name="Status",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDescription(
        key="rssi",
        name="Signal Strength",
        device_class=SensorDeviceClass.SIGNAL_STRENGTH,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement="dBm",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDescription(
        key="firmwareVersion",
        name="Firmware Version",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDescription(
        key="pidEnabled",
        name="PID Enabled",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDescription(
        key="pidProportional",
        name="PID Proportional",
        entity_category=EntityCategory.DIAGNOSTIC,
        suggested_display_precision=2,
    ),
    SensorEntityDescription(
        key="pidIntegral",
        name="PID Integral",
        entity_category=EntityCategory.DIAGNOSTIC,
        suggested_display_precision=2,
    ),
    SensorEntityDescription(
        key="pidDerivative",
        name="PID Derivative",
        entity_category=EntityCategory.DIAGNOSTIC,
        suggested_display_precision=2,
    ),
    SensorEntityDescription(
        key="pidCycleTime",
        name="PID Cycle Time",
        native_unit_of_measurement=UnitOfTime.SECONDS,
        entity_category=EntityCategory.DIAGNOSTIC,
        suggested_display_precision=1,
    ),
    SensorEntityDescription(
        key="coolingEnabled",
        name="Cooling Enabled",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDescription(
        key="heatingEnabled",
        name="Heating Enabled",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDescription(
        key="pumpEnabled",
        name="Pump Enabled",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDescription(
        key="distillationMode",
        name="Distillation Mode",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDescription(
        key="bluetoothEnabled",
        name="Bluetooth Enabled",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDescription(
        key="betaUpdates",
        name="Beta Updates Enabled",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDescription(
        key="soundsEnabled",
        name="Sounds Enabled",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDescription(
        key="controlDeviceType",
        name="Control Device Type",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDescription(
        key="controlDeviceTemperature",
        name="Control Device Temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        suggested_display_precision=1,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDescription(
        key="tempUnit",
        name="Temperature Unit",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDescription(
        key="useInternalSensor",
        name="Use Internal Sensor",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDescription(
        key="sensorDifferential",
        name="Sensor Differential",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        suggested_display_precision=2,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDescription(
        key="sensorTimeout",
        name="Sensor Timeout",
        native_unit_of_measurement=UnitOfTime.SECONDS,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDescription(
        key="compressorDelay",
        name="Compressor Delay",
        native_unit_of_measurement=UnitOfTime.MINUTES,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDescription(
        key="modeSwitchDelay",
        name="Mode Switch Delay",
        native_unit_of_measurement=UnitOfTime.SECONDS,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDescription(
        key="coolingHysteresis",
        name="Cooling Hysteresis",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        suggested_display_precision=1,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDescription(
        key="heatingHysteresis",
        name="Heating Hysteresis",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        suggested_display_precision=1,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDescription(
        key="telemetryFrequency",
        name="Telemetry Frequency",
        native_unit_of_measurement=UnitOfTime.SECONDS,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDescription(
        key="ntcBeta",
        name="NTC Beta",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDescription(
        key="ntcRefResistance",
        name="NTC Reference Resistance",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDescription(
        key="ntcRefTemperature",
        name="NTC Reference Temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
]


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up RAPT sensors from config entry."""
    coordinator: RaptDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
    
    if not coordinator.data:
        await coordinator.async_request_refresh()
    
    entities = []
    
    controllers = coordinator.data.get("controllers", []) if coordinator.data else []
    hydrometers = coordinator.data.get("hydrometers", []) if coordinator.data else []
    fermentation_chambers = coordinator.data.get("fermentation_chambers", []) if coordinator.data else []
    brewzillas = coordinator.data.get("brewzillas", []) if coordinator.data else []
    
    if controllers:
        for controller in controllers:
            device_id = controller.get("id", "unknown")
            device_name = controller.get("name", f"RAPT Controller {device_id[:8]}")
            
            for description in CONTROLLER_SENSOR_DESCRIPTIONS:
                if _sensor_data_available(controller, description.key):
                    entities.append(
                        RaptSensor(
                            coordinator,
                            description,
                            device_id,
                            device_name,
                            "TemperatureController",
                        )
                    )
    
    if hydrometers:
        for hydrometer in hydrometers:
            device_id = hydrometer.get("id", "unknown")
            device_name = hydrometer.get("name", f"RAPT Hydrometer {device_id[:8]}")
            
            for description in HYDROMETER_SENSOR_DESCRIPTIONS:
                if _sensor_data_available(hydrometer, description.key):
                    entities.append(
                        RaptSensor(
                            coordinator,
                            description,
                            device_id,
                            device_name,
                            "Hydrometer",
                        )
                    )
    
    if fermentation_chambers:
        for chamber in fermentation_chambers:
            device_id = chamber.get("id", "unknown")
            device_name = chamber.get("name", f"RAPT Chamber {device_id[:8]}")
            
            for description in FERMENTATION_CHAMBER_SENSOR_DESCRIPTIONS:
                if _sensor_data_available(chamber, description.key):
                    entities.append(
                        RaptSensor(
                            coordinator,
                            description,
                            device_id,
                            device_name,
                            "FermentationChamber",
                        )
                    )
    
    if brewzillas:
        for brewzilla in brewzillas:
            device_id = brewzilla.get("id", "unknown")
            device_name = brewzilla.get("name", f"RAPT BrewZilla {device_id[:8]}")
            
            for description in BREWZILLA_SENSOR_DESCRIPTIONS:
                if _sensor_data_available(brewzilla, description.key):
                    entities.append(
                        RaptSensor(
                            coordinator,
                            description,
                            device_id,
                            device_name,
                            "BrewZilla",
                        )
                    )
    
    if entities:
        async_add_entities(entities)
        _LOGGER.info("Added %s RAPT sensors", len(entities))
    else:
        _LOGGER.warning("No RAPT sensors could be created from available data")
    
    async def async_discovery_callback(new_devices: list[dict[str, Any]]) -> None:
        """Handle discovery of new devices."""
        new_entities = []
        
        for device in new_devices:
            device_id = device.get("id", "unknown")
            device_type = device.get("deviceType", "unknown")
            
            if device_type == "TemperatureController":
                device_name = device.get("name", f"RAPT Controller {device_id[:8]}")
                sensor_descriptions = CONTROLLER_SENSOR_DESCRIPTIONS
            elif device_type == "Hydrometer":
                device_name = device.get("name", f"RAPT Hydrometer {device_id[:8]}")
                sensor_descriptions = HYDROMETER_SENSOR_DESCRIPTIONS
            elif device_type == "FermentationChamber":
                device_name = device.get("name", f"RAPT Chamber {device_id[:8]}")
                sensor_descriptions = FERMENTATION_CHAMBER_SENSOR_DESCRIPTIONS
            elif device_type == "BrewZilla":
                device_name = device.get("name", f"RAPT BrewZilla {device_id[:8]}")
                sensor_descriptions = BREWZILLA_SENSOR_DESCRIPTIONS
            else:
                continue
            
            for description in sensor_descriptions:
                if _sensor_data_available(device, description.key):
                    new_entities.append(
                        RaptSensor(
                            coordinator,
                            description,
                            device_id,
                            device_name,
                            device_type,
                        )
                    )
        
        if new_entities:
            async_add_entities(new_entities)
            _LOGGER.info("Added %s new RAPT sensors from discovery", len(new_entities))
    
    coordinator.register_discovery_callback(async_discovery_callback)


def _sensor_data_available(controller: dict[str, Any], sensor_key: str) -> bool:
    """Check if sensor data is available for a controller."""
    if isinstance(controller, dict):
        if sensor_key in controller:
            return True
        
        if "telemetry" in controller and isinstance(controller["telemetry"], list) and controller["telemetry"]:
            latest_telemetry = controller["telemetry"][0]
            if sensor_key in latest_telemetry:
                return True
    
    return False


class RaptSensor(CoordinatorEntity[RaptDataUpdateCoordinator], SensorEntity):
    """Representation of a RAPT sensor."""

    def __init__(
        self,
        coordinator: RaptDataUpdateCoordinator,
        description: SensorEntityDescription,
        device_id: str,
        device_name: str,
        device_type: str,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self.entity_description = description
        self._device_id = device_id
        self._device_name = device_name
        self._device_type = device_type
        
        self._attr_unique_id = f"{device_id}_{description.key}"
        self._attr_name = f"{device_name} {description.name}"
        
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, device_id)},
            name=device_name,
            manufacturer="RAPT",
            model=device_type,
        )

    @property
    def native_value(self) -> float | int | str | None:
        """Return the state of the sensor."""
        if not self.coordinator.data:
            return None
        
        device = None
        if self._device_type == "TemperatureController":
            devices = self.coordinator.data.get("controllers", [])
        else:
            devices = self.coordinator.data.get("hydrometers", [])
        
        for dev in devices:
            if dev.get("id") == self._device_id:
                device = dev
                break
        
        if not device:
            return None
        
        sensor_key = self.entity_description.key
        
        if sensor_key in device:
            return self._parse_value(device[sensor_key])
        
        if "telemetry" in device and isinstance(device["telemetry"], list) and device["telemetry"]:
            latest_telemetry = device["telemetry"][0]
            if sensor_key in latest_telemetry:
                return self._parse_value(latest_telemetry[sensor_key])
        
        return None

    def _parse_value(self, value: Any) -> float | int | str | None:
        """Parse the value from the API response."""
        if value is None:
            return None
        
        if isinstance(value, bool):
            return 100 if value else 0
        
        if isinstance(value, (int, float)):
            return value
        
        if isinstance(value, str):
            try:
                return float(value)
            except ValueError:
                try:
                    return int(value)
                except ValueError:
                    return value
        
        return str(value)

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return self.coordinator.last_update_success and self.native_value is not None