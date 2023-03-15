from experiments.devices import Pico
import belay
import time
import pandas as pd
import csv

def run_of_sensor(port):
    with Pico.Pico(port) as pico:
        pico.setup_PAA5100(multi=False)
        with open(r'/Users/roaldarbol/Desktop/temps.csv', 'a') as f:
            writer = csv.writer(f)
            start_time = time.time()
            for i in pico.record_flow():
                current_time = (time.time() - start_time)
                j = [current_time, i[0], i[1]]
                print("Distance: {} mm | Rotation: {} deg".format(int(i[0]), int(i[1])))
                writer.writerow(j)

if __name__ == "__main__":
    devices = belay.list_devices()
    selected_port = devices[-1]
    run_of_sensor(selected_port)
    


