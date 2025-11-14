# import sys
# import os
# project_dir = os.getcwd()
# if project_dir not in sys.path:
#     sys.path.insert(0, project_dir)

# import atexit
import time
from belay import list_devices
from devices.PicoBonn import PicoBonn

# Initialize device globally
device_port = list_devices()[-1]
t1 = time.time()
with PicoBonn(device_port) as picoB:
    t2 = time.time()
    print()
    print("Connected! Connection took {:.2f}s".format(t2 - t1))
    time.sleep(1)
    print(picoB.latest_temperature)
    time.sleep(1)
    picoB.measure_temperature()
    print("Reading...")
    time.sleep(1)
    print(picoB.latest_temperature)
    time.sleep(1)
    print(picoB.latest_temperature)