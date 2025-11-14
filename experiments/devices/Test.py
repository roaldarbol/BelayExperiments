from belay import Device

class PicoBonn3(Device):
    def __init__(self, *args, **kwargs):
        # Initialize host-side variables before calling parent __init__
        self._temperature = None
        super().__init__(*args, **kwargs)

    @Device.setup(
        autoinit=True
    )
    def setup():
        from machine import Pin
        import time

        # Init on-board stuff
        led = Pin('LED', Pin.OUT)
        led.value(True)
        temperature = None
        
    @Device.task
    def _measure_temperature():
        # Runs on the Pico
        # global temperature
        temperature = 72.5  # Or read from a sensor
        return temperature

    def measure_temperature(self):
        # Runs on your computer - this is a regular method
        self._temperature = self._measure_temperature()
        return self._temperature

    @property
    def latest_temperature(self):
        # Now you can just return the cached value
        return self._temperature