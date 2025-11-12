from experiments.devices.BeeHive import BeeHive
from belay import Device, list_devices
import belay
import time

if __name__ == "__main__":

    # Device setup
    devices = list_devices()
    port = devices[-1]
    bee = BeeHive('/dev/cu.usbserial-0001')
    bee.setup()

    # Experimental variables
    # Don't randomize, start with shortest duration - 6-8 repeats of each stimulus duration.
    repeats = 10
    stimulus_duration_ms = [10000, 5000, 1000, 500, 100, 50, 10, 1]
    iti = 30
    state = False
    experiment_duration = len(stimulus_duration_ms) * iti * repeats + sum(stimulus_duration_ms) / 1000
    print("Total experimental duration:", round(experiment_duration / 60, 2), "min")

    # Experimental loop
    print("Priming...")
    state = bee.neopixel_toggle(False)
    bee.analog(1)
    time.sleep(iti)
    try:
        for t in stimulus_duration_ms:
            for i in range(repeats):
                state = bee.neopixel_toggle(state)
                bee.analog(0)
                time.sleep(t / 1000)
                state = bee.neopixel_toggle(state)
                bee.analog(1)
                print("Stimulus duration:", t, "ms", i+1)
                time.sleep(iti)
    except:
        pass

    # Tidy up
    bee.neopixel_toggle(False)
    bee.analog(1)
    bee.close()