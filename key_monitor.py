import logging
from pynput import keyboard

logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)
handler = logging.FileHandler('output.log', "a+")
formatter = logging.Formatter('%(asctime)s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


def on_press(key):
    try:
        logger.info("{0} p".format(key.char))
    except AttributeError:
        logger.info('{0} p'.format(key))


def on_release(key):
    logger.info('{0} r'.format(key))
    # if key == keyboard.Key.esc:
    #     # Stop listener
    #     return False


# Collect events until released
with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()
