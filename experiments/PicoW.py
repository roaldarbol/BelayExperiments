
from belay import Device, list_devices
import time

class PicoW(Device):
    @Device.setup
    def setup():
        led = Pin('LED', Pin.OUT)

    @Device.task
    def led_toggle():
        led.toggle()

    @Device.task
    def my_generator():
        i = 0
        while i < 10:
            yield i
            i += 1

if __name__ == "__main__":
    picoW = PicoW(list_devices()[-1])
    picoW.setup()
    picoW.led_toggle()
    time.sleep(2)
    picoW.led_toggle()
    vals = []
    for val in picoW.my_generator():
        vals.append(val)
    print(vals)
    picoW.close()