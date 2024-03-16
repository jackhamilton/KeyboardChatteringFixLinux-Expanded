import logging
import os
import configparser
import re
from typing import Final

INPUT_DEVICES_PATH: Final = 'dev/input/by-id'
_KEYBOARD_NAME_SUFFIX: Final = '-kbd'
VIRTUAL_DEVICES_PATH: Final = '/sys/devices/virtual/input/'
KEYBOARD_NAME_PREFIX: Final = 'input'

def retrieve_keyboard_name() -> str:
    config = configparser.ConfigParser()
    keyboard_devices = list(filter(lambda d: d.endswith(_KEYBOARD_NAME_SUFFIX), os.listdir(INPUT_DEVICES_PATH)))
    n_devices = len(keyboard_devices)

    if n_devices == 0:
        raise ValueError(f"Couldn't find a keyboard in '{INPUT_DEVICES_PATH}'")
    if n_devices == 1:
        logging.info(f"Found keyboard: {keyboard_devices[0]}")
        return keyboard_devices[0]
    
    # Use native Python input for user selection
    print("Select a device:")
    for idx, device in enumerate(keyboard_devices, start=1):
        print(f"{idx}. {device}")
    
    selected_idx = -1
    while selected_idx < 1 or selected_idx > n_devices:
        try:
            selected_idx = int(input("Enter your choice (number): "))
            if selected_idx < 1 or selected_idx > n_devices:
                print(f"Please select a number between 1 and {n_devices}")
        except ValueError:
            print("Please enter a valid number")
    
    config['CONFIG']['Keyboard'] = keyboard_devices[selected_idx - 1]
    with open('/root/.config/KeyboardChatteringFix/config', 'w') as configFile:
        config.write(configfile)
    return keyboard_devices[selected_idx - 1]

def get_uevent_path(sysDevicePath) -> str:
    event_directories = list(filter(lambda e: e.startswith("event"), os.listdir(sysDevicePath)))
    if len(event_directories) == 0:
        print("Failed to match keyboard name.")
        return "NO MATCH"
    with open(sysDevicePath + "/" + event_directories[0] + "/uevent") as f:
        s = f.read()
        device = re.search("(?<=DEVNAME=).*$", s)
        if device:
            return "/dev/{}".format(device.group(0))
    print("Failed to match keyboard name.")
    return "NO MATCH"

def retrieve_virtual_keyboard_with_name(name) -> str:
    virtual_devices = list(filter(lambda d: d.startswith(KEYBOARD_NAME_PREFIX), os.listdir(VIRTUAL_DEVICES_PATH)))
    for device in virtual_devices: 
        with open(VIRTUAL_DEVICES_PATH + device + "/name") as f:
            s = f.read()
            if s.strip() == name.strip(): 
                return get_uevent_path(VIRTUAL_DEVICES_PATH + device)
    print("Failed to match keyboard name.")
    return "NO MATCH"

def main():
    print(retrieve_virtual_keyboard_with_name("KMonad kbd"))

if __name__ == "__main__":
    main()

def abs_keyboard_path(device: str) -> str:
    return os.path.join(VIRTUAL_DEVICES_PATH, device)

