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
    reps = 10
    duration_isi = [15000, 10000, 7500, 5000] # Inter-stimulus intervals
    duration_iti = 60
    stimulus_ms = 100
    state = False

    experiment_duration = len(duration_isi) * stimulus_ms * reps + 6 * sum(duration_isi) / 1000 + len(duration_isi) * duration_iti * 6
    print("Total experimental duration:", round(experiment_duration / 60, 2), "min")

    # Experimental loop
    print("Priming...")
    state = bee.neopixel_toggle(False)
    bee.analog(1)
    time.sleep(duration_iti)
    try:
        for t in duration_isi: # Start with longest ISI first
            for i in range(reps):
                print("Inter-stimulus duration:", t, "ms", i+1)
                state = bee.neopixel_toggle(state)
                bee.analog(0)
                time.sleep(stimulus_ms / 1000)
                state = bee.neopixel_toggle(state)
                bee.analog(1)
                time.sleep(t / 1000)
                state = bee.neopixel_toggle(state)
                bee.analog(0)
                time.sleep(stimulus_ms / 1000)
                state = bee.neopixel_toggle(state)
                bee.analog(1)
                time.sleep(duration_iti)
    except:
        pass

    # Tidy up
    bee.neopixel_toggle(False)
    bee.analog(1)
    bee.close()