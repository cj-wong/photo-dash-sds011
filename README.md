# SDS011 for photo-dash

## Overview

This is the SDS011 module for `photo-dash`. It takes air quality output (both PM2.5 and PM10) from a [Nova] SDS011 module and converts it to a request to the `photo-dash` endpoint.

The `photo-dash` project is a series of modules and an endpoint. The endpoint sends images to a dumb digital photo frame.

## Usage

1. Setup [config.json](config.json.example). You must fill out all fields: the device path (serial device) and how long to wait between loops.
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

This project is not affiliated with or endorsed by [Nova]. See [LICENSE](LICENSE) for more detail.

[Nova]: http://www.inovafitness.com/en/a/index.html
