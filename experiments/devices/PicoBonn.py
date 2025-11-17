from belay import Device

class PicoBonn(Device):
    def __post_autoinit__(self, *args, **kwargs):
        self._temperature = None

    # ---- Setup and teardown of device ----- #

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
        led.value(True)

    @Device.teardown
    def teardown():
        bh1745.leds(False)
        led.value(False)

    # ----- Device methods ----- #

    @Device.task
    def set_led(state):
        print(f"Printing from device; turning LED to {state}.")
        Pin('LED', Pin.OUT).value(state)

    @Device.task
    def led_toggle():
        led.toggle()

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
        return temperature

    # ----- Local wrappers ----- #

    def measure_temperature(self):
        # Runs on your computer - this is a regular method
        self._temperature = self.read_environment()
        return self._temperature

    @property
    def latest_temperature(self):
        # Now you can just return the cached value
        return self._temperature