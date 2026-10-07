from belay import Device

class PicoBonn(Device):

    # ---- Setup and teardown of device ----- #

    @Device.setup(autoinit=True)
    def setup():
        import machine
        from machine import Pin
        import time
        import random
        from pimoroni_i2c import PimoroniI2C
        from breakout_bh1745 import BreakoutBH1745
        from breakout_bme68x import BreakoutBME68X
        from breakout_ioexpander import BreakoutIOExpander

        # Init on-board stuff
        led = Pin('LED', Pin.OUT)
        temp_sensor = machine.ADC(4)
        conv = 3.3 / 65535  # Conversion factor

        # I2C bus setup
        PINS_BREAKOUT_GARDEN = {"sda": 4, "scl": 5}
        I2C = PimoroniI2C(**PINS_BREAKOUT_GARDEN)
        led.value(True)   

        bh1745 = BreakoutBH1745(I2C)
        bh1745.leds(True)
        bme688 = BreakoutBME68X(I2C)
        ioe = BreakoutIOExpander(I2C)
        IR_PIN = 1
        ioe.set_mode(IR_PIN, ioe.PIN_OUT)
        ioe.output(IR_PIN, 0)

    @Device.teardown
    def teardown():
        if 'bh1745' in dir():
            bh1745.leds(False)
        if 'ioe' in dir():
            ioe.output(IR_PIN, 0)
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
    def ir_led(state):
        ioe.output(IR_PIN, state)

    @Device.task
    def ir_led_toggle():
        current = ioe.input(IR_PIN)
        ioe.output(IR_PIN, not current)

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
        # print("Temp: {}".format(temperature))
        # print("Pressure: {}".format(pressure))
        # print("Humidity: {}".format(humidity))
        return temperature

    # ----- Local wrappers ----- #

    def measure_temperature(self):
        self._temperature = self.read_environment()
        return self._temperature

    @property
    def latest_temperature(self):
        return self._temperature
    
    @Device.task
    def i2c_scan():
        devices = I2C.scan()
        print(f"Found {len(devices)} device(s):")
        for addr in devices:
            print(f"  0x{addr:02x} ({addr})")
        return devices