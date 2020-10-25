import photo_dash_sds011


if __name__ == '__main__':
    photo_dash_sds011.config.LOGGER.info('Starting main.py')
    s = photo_dash_sds011.sds011.SDS011()
    s.loop()
