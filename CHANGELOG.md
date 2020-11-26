# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [0.1.2] - 2020-11-25
### Added
- Applied update from `photo-dash-base/python` that adds a new class method to sleep until quiet hours are over.

### Changed
- During quiet hours, the serial connection can be closed. This may save the sensor from use during which no data is being read, anyway. Because this is a feature change, a new [configuration][config.json] field is added: `"disconnect_in_quiet_hours"`, set to `false` by default. If this field isn't present, `False` is assumed during the first run. 

## [0.1.1] - 2020-11-04
### Added
- Added a function that checks quiet hours from the endpoint at least every 24 hours.

### Changed
- In reference of issue #1: added time tracking to the [sds011.py](photo_dash_sds011/sds011.py). Now, the project won't read and send data when the endpoint has issued quiet hours.

## [0.1.0] - 2020-10-25
### Added
- Initial version

[config.json]: config.json.example
