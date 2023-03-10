from PicoW import PicoW
import belay
import time
import pandas as pd

def single_recording(device):

    # Run experiment
    try:
        data = device.led_toggle()
        time.sleep(2)
        new_data = device.led_toggle()
        data = dict_append(data, new_data)
    except:
        pass
    return(data)

def continuous_recording(device, iti):
    data = pd.DataFrame({
        'temp': [],
        'time': []
    })
    
    # Run experiment
    t_init = time.time()
    iti = 5
    try:
        for val in device.my_generator(iti):
            val_pd = pd.DataFrame([val])
            data = pd.concat([data, val_pd], ignore_index=True)
            data.loc[data.index[-1],'time'] = time.time() - t_init
            print(val_pd)
            t0 = time.time()
            t1 = time.time()
            iti_adjusted = iti - ((t0 - t_init) % iti)
            while t1 - t0 < iti_adjusted:
                t1 = time.time()
    except:
        pass
    print(data)
    return(data)

if __name__ == "__main__":
    devices = belay.list_devices()
    port = devices[-1]
    picoW = PicoW(port)
    picoW.setup()
    try:
        a = single_recording(picoW)
        b = continuous_recording(picoW, iti=5)
    except:
        pass
    picoW.led_off()
    picoW.close()