# import sys
# import os
# project_dir = os.getcwd()
# if project_dir not in sys.path:
#     sys.path.insert(0, project_dir)

import time
from belay import Device, list_devices
from devices.PicoBonn import PicoBonn

address = list_devices()[-1]
print(address)
picoB = PicoBonn("COM3")
print("Here 1")
picoB.read_light()
print("here 2")
time.sleep(5)
picoB.read_environment()
picoB.close()