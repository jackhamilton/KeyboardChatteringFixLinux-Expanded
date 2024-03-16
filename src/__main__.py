import argparse
import logging
import sys
import configparser
import os
from contextlib import contextmanager

import libevdev

from src.filtering import filter_chattering
from src.keyboard_retrieval import retrieve_virtual_keyboard_with_name, abs_keyboard_path, retrieve_keyboard_name

@contextmanager
def get_device_handle(keyboard_name: str) -> libevdev.Device:
    """ Safely get an evdev device handle. """

    fd = open(abs_keyboard_path(keyboard_name), 'rb')
    evdev = libevdev.Device(fd)
    try:
        yield evdev
    finally:
        fd.close()


if __name__ == "__main__":
    config = configparser.ConfigParser()
    configPath = os.getenv("HOME") + '/.config/KeyboardChatteringFix/config'
    config.read(configPath)
    configuration = config['CONFIG']
    keyboardName = configuration['Keyboard']
    verbosity = configuration['Verbosity']
    keyboardIsVirtual = config.getboolean('CONFIG', 'IsVirtual')
    threshhold = config.getint('CONFIG', 'Threshhold')
    intVerbosity = 0
    if verbosity == "INFO":
        intVerbosity = 1
    elif verbosity == "DEBUG":
        intVerbosity = 2

    logging.basicConfig(
        level={
            0: logging.CRITICAL,
            1: logging.INFO,
            2: logging.DEBUG
        }[intVerbosity],
        handlers=[
            logging.StreamHandler(
                sys.stdout
            )
        ],
        format="%(asctime)s - %(message)s",
        datefmt="%H:%M:%S"
    )
    
    keyboardPath = ""
    if keyboardIsVirtual and keyboardName:
        keyboardPath = retrieve_virtual_keyboard_with_name(keyboardName)
    elif not keyboardIsVirtual:
        if keyboardName:
            keyboardPath = keyboardName
        else:
            keyboardPath = retrieve_keyboard_name()
    else:
        print("Failed to construct keyboard based on provided configuration. Double check your ~/.config/KeyboardChatteringFix/config.")
        sys.exit()
    print("Using keyboard " + keyboardPath + " with threshhold " + str(threshhold))

    deviceHandle = get_device_handle(keyboardPath)
    with get_device_handle(keyboardPath) as device:
        filter_chattering(device, threshhold)
