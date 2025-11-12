
from belay import Device, list_devices
import time

class PicoW(Device):
    @Device.setup
    def setup():
        import random
        led = Pin('LED', Pin.OUT)
        temp_sensor = machine.ADC(4)
        conv = 3.3 / 65535  # Conversion factor

    @Device.task
    def led_toggle():
        led.toggle()
        data = {'a': [random.random()], 'b': [random.random()]}
        return(data)

    @Device.task
    def led_off():
        led.value(0)

    @Device.task
    def my_generator(n):
        i = 0
        while i < n:
            led.toggle()
            data = temp_sensor.read_u16() * conv 
            temp = 27-(data-0.706)/0.001721
            yield({
                'temp': temp,
                'time': i
            })
            i += 1

if __name__ == "__main__":
    picoW = PicoW(list_devices()[-1])
    picoW.setup()
    vals = []
    
    try:
        for val in picoW.my_generator():
            t0 = time.time()
            t1 = time.time()
            while t1 - t0 < 1:
                t1 = time.time()
            print(t1 - t0)
            vals.append(val)
            picoW.led_toggle()
        print(vals)
    except:
        print("here", vals)
        picoW.led_off()
        picoW.close()