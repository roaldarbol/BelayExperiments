from experiments.devices import Pico
import belay
import time
import pandas as pd



if __name__ == "__main__":
    devices = belay.list_devices()
    port = devices[-1]
    pico = Pico.Pico(port)
    pico.import_libs()
    pico.setup_PAA5100(double=True)
    # pico.setup_of_sensor()

    try:
        while True:
            # pico.capture_frame()
            pico.record_flow_double()
            # pico.sleep(10)
    except:
        pass
    pico.close()


