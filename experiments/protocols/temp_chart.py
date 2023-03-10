from belay import Device, list_devices
import time
import sys
from datetime import datetime as dt
import cursor
import csv
from experiments.devices import Pico, BeeHive

cursor.hide()
pico = Pico.Pico(list_devices()[-1])
pico.setup()
pico.record_environment()
vals = ['temp', 'pressure', 'humidity', 'time']

# Create/overwrite csv file
with open(r'/Users/roaldarbol/Desktop/temps.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(vals)

try:
    # light = pico.record_light()
    while True:
        temp = pico.record_environment()
        now = dt.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        temp.append(dt_string)
        # print(temp)
        with open(r'/Users/roaldarbol/Desktop/temps.csv', 'a') as f:
            writer = csv.writer(f)
            writer.writerow(temp)
        sys.stdout.write("\r{0}: {1}".format(dt_string, temp))
        sys.stdout.flush()
        time.sleep(3)
        
except:
    pass
# print(vals)
# pico.led_off()
pico.close()