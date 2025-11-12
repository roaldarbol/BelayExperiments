
from belay import Device, list_devices
import time

class PicoBonn(Device):
    @Device.setup(
        autoinit=True
    )
    def setup():
        import machine
        from machine import Pin
        import time
        import random
        from pimoroni_i2c import PimoroniI2C
        from breakout_bme68x import BreakoutBME68X
        from breakout_bh1745 import BreakoutBH1745

        # Init on-board stuff
        led = Pin('LED', Pin.OUT)
        temp_sensor = machine.ADC(4)
        conv = 3.3 / 65535  # Conversion factor

        # Breakout setup
        PINS_BREAKOUT_GARDEN = {"sda": 4, "scl": 5}
        I2C = PimoroniI2C(**PINS_BREAKOUT_GARDEN)
        bh1745 = BreakoutBH1745(I2C)
        bme688 = BreakoutBME68X(I2C)
        bh1745.leds(True)

    @Device.task
    def set_led(state):
        print(f"Printing from device; turning LED to {state}.")
        Pin('LED', Pin.OUT).value(state)

    @Device.task
    def led_toggle():
        led.toggle()
        # data = {'a': [random.random()], 'b': [random.random()]}
        # return(data)

    @Device.task
    def led_off():
        led.value()

    @Device.task
    def bh_led_toggle(state):
        bh1745.leds(state)

    @Device.task
    def read_light():
        rgbc_raw = bh1745.rgbc_raw()
        rgb_clamped = bh1745.rgbc_clamped()
        rgb_scaled = bh1745.rgbc_scaled()
        print("Raw: {}, {}, {}, {}".format(*rgbc_raw))
        print("Clamped: {}, {}, {}, {}".format(*rgb_clamped))
        print("Scaled: #{:02x}{:02x}{:02x}".format(*rgb_scaled))
        return list(rgbc_raw)

    @Device.task
    def read_environment():
        temperature, pressure, humidity, gas_resistance, status, gas_index, meas_index = bme688.read()
        print("Temp: {}".format(temperature))
        print("Pressure: {}".format(pressure))
        print("Humidity: {}".format(humidity))

if __name__ == "__main__":
    picoB = PicoBonn(list_devices()[-1])
    picoB.setup()
    vals = [1]
    t_interval = 5
    
    try:
        picoB.led_toggle()
        t0 = time.time()
        t1 = time.time()
        while t1 - t0 < t_interval:
            t1 = time.time()
        picoB.led_toggle()
        picoB.record_light()
        
    except:
        print("here", vals)
        picoB.led_off()
        picoB.close()