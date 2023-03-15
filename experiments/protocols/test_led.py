from experiments.devices import Pico
import belay
import time
import csv

def testing_it_all(port):
    with Pico.Pico(port) as pico:
        with open(r'/Users/roaldarbol/Desktop/temps.csv', 'a') as f:
            pico.import_libs()
            while True:
                for i in pico.led_toggle():       
                    writer = csv.writer(f)
                    writer.writerow(i)
                    print(i)
                    time.sleep(1)

