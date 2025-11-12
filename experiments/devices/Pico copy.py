from belay import Device, list_devices

class Pico(Device):
    @Device.setup
    def setup1(argument=False):
        from machine import Pin
        led = Pin(25, Pin.OUT)

    @Device.task
    def led_toggle():
        led.toggle()



if __name__ == "__main__":
    port = list_devices()[-1]
    with Pico(port) as pico:
        pico.setup1(argument=True)
        pico.led_toggle()