# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [0.2.0] - 2020-11-25
### Changed
- In reference of issue #2: because [config.py] was considerably bloated with air quality data (variables and classes), the air quality data was moved to a separate [module][air_quality.py]. Subsequently, what little tests I wrote will need to be re-written. Although functionality has not been changed, I believe the addition of this module should be treated as minor version change.

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

[air_quality.py]: photo_dash_sds011/air_quality.py
[config.json]: config.json.example
[config.py]: photo_dash_sds011/config.py
