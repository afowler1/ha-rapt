# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Hydrometer support with specific gravity, gravity velocity, and battery monitoring
- Fermentation chamber support with comprehensive temperature control, heating/cooling metrics, PID settings, and diagnostics
- BrewZilla support with pump control, distillation mode, advanced brewing features, and professional-grade diagnostics
- Device-specific sensor entities based on device type
- Manual device discovery service (`rapt.discover_devices`)
- Automatic detection of new devices during update cycles
- Dynamic entity creation system with discovery callbacks

### Changed
- Optimized API usage to use only list endpoints (no individual device requests)
- Balanced update interval (60 seconds) with improved rate limiting (15 seconds between calls)
- Eliminated unnecessary individual API calls for better performance
- Separated sensor definitions for each device type
- Adjusted rate limiting to accommodate comprehensive device support

## [1.0.0] - 2025-09-18

### Added
- Initial release of RAPT Temperature Controller integration
- Read-only interface for RAPT portal API
- Temperature monitoring with current and target temperature sensors
- Heating and cooling status monitoring
- Automatic authentication and token management
- Rate-limited API calls (30-second intervals)
- Secure API secret storage following HA best practices
- HACS compatibility
- Comprehensive documentation and setup instructions

### Features
- Real-time temperature readings from RAPT temperature controllers
- Target temperature monitoring
- Heating output percentage tracking
- Cooling output percentage tracking
- Automatic token refresh (50-minute validity, refreshed at 45 minutes)
- Device auto-discovery through telemetry data
- Robust error handling and logging
- Configuration flow for easy setup

### Technical Details
- Built for Home Assistant 2024.1.0+
- Cloud polling integration type
- Uses aiohttp for async HTTP communication
- Implements DataUpdateCoordinator for efficient data management
- Follows Home Assistant integration best practices