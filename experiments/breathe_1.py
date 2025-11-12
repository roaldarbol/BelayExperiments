from devices.BeeHive import BeeHive
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
    trial_min = 0.5
    state = False
    reps = 10
    current_rep = 0
    experiment_duration = (trial_min * 60) * reps * 2
    print("Total experimental duration:", round(experiment_duration / 60, 2), "min")

    # try:
    #     time.sleep(10)
    #     bee.analog(1)
    #     # state = bee.neopixel_toggle(state)
    #     time.sleep(10)
    #     bee.analog(0)
    #     # state = bee.neopixel_toggle(state)
    # except:
    #     pass
    # Experimental loop
    print("Priming...")
    bee.neopixel_toggle(False)
    bee.analog(1)
    time.sleep(trial_min*60)
    try:
        while current_rep <= reps:
            print("Light, Repetition", current_rep)
            state = bee.neopixel_toggle(state)
            bee.analog(1)
            time.sleep(trial_min * 60)
            print("Dark, Repetition", current_rep)
            state = bee.neopixel_toggle(state)
            bee.analog(0)
            time.sleep(trial_min * 60)
            current_rep += 1
    except:
        pass

    # Tidy up
    bee.neopixel_toggle(False)
    bee.analog(1)
    bee.close()