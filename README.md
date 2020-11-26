# SDS011 for photo-dash

## Overview

The `photo-dash` project is a series of modules and an endpoint. This repository specifically is a reader for an air quality reader, the [Nova] SDS011 module.

This is the SDS011 module for `photo-dash`. It takes air quality readings (both PM2.5 and PM10, unit in `μg / m^3`) from a SDS011 module and converts it to a request to the `photo-dash` endpoint.

Air quality ranges have been determined from the [AirNow.gov] [AQI Calculator][AQI]. On the main page of airnow.gov, the ranges (and colors) of their "Air Quality Index" have been plugged into the calculator to determine the corresponding levels of PM2.5 and PM10 particulate readings. This information is available in the [config](photo_dash_sds011/config.py) module.

## Usage

1. Setup [config.json](config.json.example) by copying the example file and renaming it. You must fill out all fields: the device path (serial device) and how long to wait between loops.
    - `"device"` must be a string and a path.
    - `"seconds_per_cycle"` must be an integer.
2. Run `sds011.py`.

## Requirements

This code is designed around the following:

- Python 3.7+
    - `pyserial` for serial interface to the SDS011
    - `requests` to send a formatted response to the endpoint
    - other [requirements](requirements.txt)

## Disclaimer

This project is not affiliated with or endorsed by [AirNow.gov] or [Nova]. See [LICENSE](LICENSE) for more detail.

[AirNow.gov]: https://www.airnow.gov
[AQI]: https://www.airnow.gov/aqi/aqi-calculator/
[Nova]: http://www.inovafitness.com/en/a/index.html
