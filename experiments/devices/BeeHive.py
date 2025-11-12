from belay import Device, list_devices
import time

class BeeHive(Device):
    @Device.setup
    def setup():
        from neopixel import NeoPixel
        from machine import DAC, Pin
        num_pixels = 12
        np = NeoPixel(Pin(4), num_pixels, bpp=4)
        dac = DAC(Pin(25))
        print("Connected!")

    @Device.task
    def neopixel_toggle(state, colour = (0,0,0,255)):
        # np = NeoPixel(Pin(4), 12, bpp=4)

        dark = (0,0,0,0)

        if state is False:
            np.fill(colour)
        elif state is True:
            np.fill(dark)
        np.write()
        state = not state
        return(state)

    @Device.task
    def neopixel_fade(state, duration, colour = (0,0,0,255), n_leds = 12):
        init_state = state

        dark = (0,0,0,0)
        duration *= 1000
        n_steps = 256
        step_duration_short = round(duration / (n_steps * n_leds))
        step_duration_long = round(duration / n_steps)

        # Maybe find the element with the highest value, do some division to figure out how much to increase by and over how long
        i = 0
        j = 0
        while i < n_steps:
            t_0 = time.ticks_ms()
            while j < n_leds:
                t_1 = time.ticks_ms()
                if state is False:
                    np[j] = (0,0,0,i)
                elif state is True:
                    np[j] = (0,0,0,255-i)
                np.write()
                j += 1
                while time.ticks_ms() - t_1 < step_duration_short:
                    pass
            j = 0
            i += 1
            while time.ticks_ms() - t_0 < step_duration_long:
                pass
        state = not state
        return(state)

    @Device.task
    def analog(voltage):
        val = int(256 * (voltage/3.3))
        dac.write(val)


if __name__ == '__main__':
    devices = list_devices()
    port = devices[-1]
    bee = BeeHive('/dev/cu.usbserial-0001')
    bee.setup()
    try:
        state = False
        state = bee.neopixel_toggle(state)
        time.sleep(1 / 1000)
        state = bee.neopixel_toggle(state)
        print("Made it here...")
        # a = single_recording(picoW)
        # b = continuous_recording(picoW, iti=5)
    except:
        pass
    # bee.led_off()
    bee.close()
    # device = BeeHive('/dev/cu.SLAB_USBtoUART', 115200)
    # device.setup()
    # state = False

    # half_hour = 30 * 60
    # t_0 = time.time()
    # state = neopixel_fade(state, 10)
    # state = neopixel_fade(state, 10)
    # t_2 = time.time()
    # print(t_2 - t_0)
    # device.close()

# state = neopixel_toggle(state)

# while t_1 - t_0 < 5:
#     t_1 = time.time()
#     pass
# light_times = []

# @device.task
# def send_number(event, num):
#     from neopixel import NeoPixel
#     led = Pin(25, Pin.OUT)
#     while True:
#         times = []
#         t_0 = time.ticks_ms()
#         while len(times) <= 10:

#             # Do important stuff
#             led.toggle()
#             t_1 = time.ticks_ms()
#             t_diff_1 = t_1 - t_0

#             # Add to our eventual output list
#             times += [t_diff_1]

#             # "Better sleep"
#             t_diff_2 = 0
#             while t_diff_2 < 1000:
#                 t_diff_2 = time.ticks_ms() - t_1
            
#         yield(times)
#         led.off()
#         break

# if __name__ == '__main__':
#     t_0 = time.time()
#     t_1 = time.time()
#     event = mp.Event()
#     while t_1 - t_0 < 10:
#         for i in led_loop():
#             device.send()
#             light_times.append(x)
#             t_1 = time.time()
