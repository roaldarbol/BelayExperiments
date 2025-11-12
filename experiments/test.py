import time
from belay import Device, list_devices
from devices.PicoBonn import PicoBonn

picoB = PicoBonn(list_devices()[-1])

picoB.read_light()
picoB.read_environment()
picoB.bh_led_toggle(False)