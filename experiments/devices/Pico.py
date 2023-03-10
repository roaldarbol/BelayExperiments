
from belay import Device, list_devices
import time
import sys
from datetime import datetime as dt
import cursor
import csv

class Pico(Device):
    @Device.setup
    def import_libs():
        import machine
        from machine import Pin
        import time
        from pimoroni_i2c import PimoroniI2C
        from breakout_bme280 import BreakoutBME280
        from breakout_bh1745 import BreakoutBH1745
        from breakout_paa5100 import BreakoutPAA5100 as FlowSensor
        led = Pin(25, Pin.OUT)

    @Device.setup
    def setup_PAA5100(double=False):
        BG_SPI_FRONT = 0
        BG_SPI_BACK = 1
        flo1 = FlowSensor(
            slot=BG_SPI_FRONT
        ) # Front
        if double == True:
            flo2 = FlowSensor(
                slot=BG_SPI_BACK
            ) # Back
        rotation = FlowSensor.DEGREES_0
        SIZE = FlowSensor.FRAME_SIZE
        BYTES = FlowSensor.FRAME_BYTES
        data = bytearray(BYTES)

        flo1.set_rotation(rotation)

        offset = 0
        value = 0

        x = 0
        y = 0
        z = 0


    def value_to_char(value):
        charmap = " .:-=+*#%@"
        val = float(value) / 255.0
        val *= len(charmap) - 1
        chosen_char = charmap[int(val)]
        return chosen_char * 2  # Double chars to - sort of - correct aspect ratio
    # @Device.setup
    # def setup_ADNS3080():



    # @Device.setup
    # def setup_env_sensors():
    #     PINS_BREAKOUT_GARDEN = {"sda": 4, "scl": 5}
    #     PINS_PICO_EXPLORER = {"sda": 20, "scl": 21}

    #     i2c = PimoroniI2C(**PINS_BREAKOUT_GARDEN)
    #     bh1745 = BreakoutBH1745(i2c)
    #     bme = BreakoutBME280(i2c)

        # bh1745.leds(True)

    @Device.task
    def sleep(ms):
        time.sleep_ms(ms)

    @Device.task
    def led_toggle():
        led.toggle()

    @Device.task
    def record_light():
        rgbc_raw = bh1745.rgbc_raw()
        rgb_clamped = bh1745.rgbc_clamped()
        rgb_scaled = bh1745.rgbc_scaled()
        print("Raw: {}, {}, {}, {}".format(*rgbc_raw))
        print("Clamped: {}, {}, {}, {}".format(*rgb_clamped))
        print("Scaled: #{:02x}{:02x}{:02x}".format(*rgb_scaled))
        return list(rgbc_raw)

    @Device.task
    def record_environment():
        return list(bme.read())

    @Device.task
    def record_flow(delay=0):
        tx = 0
        ty = 0
        try:
            while True:
                delta = flo1.get_motion()
                # if abs(delta[0]) > 2: 
                if delta is not None: 
                    x = delta[0]
                    y = delta[1]
                    tx += x
                    ty += y
                print("Relative, rel: x {}, y {}".format(tx, ty))
                if delay != 0:
                    time.sleep(delay)
        except:
            pass

    @Device.task
    def record_flow_double(delay=0):
        tx = 0
        ty = 0
        tz = 0
        try:
            while True:
                delta1 = flo1.get_motion()
                # delta2 = flo2.get_motion()
                # if abs(delta[0]) > 2: 
                if abs(delta1[0]) > 1: 
                    x = -delta1[1] / 34.1 # Distance in cm
                    y = delta1[0] / 14.8 # Get to degrees
                    # z = delta2[1] / 341 # Distance in cm
                    tx += x
                    ty += y
                    # tz += z
                print("Distance: {} mm | Rotation: {} deg".format(int(tx), int(ty)))
                if delay != 0:
                    time.sleep(delay)
        except:
            pass

    @Device.task
    def capture_frame():
        print("Capturing...")
        time.sleep(0.1)

        # Warning! The frame capture function below can take up to 10 seconds to run! Also, it often fails to capture all bytes.
        # A shorter timeout (in seconds) can be set with the 'timeout' keyword e.g. frame_capture(data, timeout=6.0)
        data_size = flo1.frame_capture(data)
        if data_size == BYTES:
            for y in range(0, SIZE):
                if rotation == FlowSensor.DEGREES_180 or rotation == FlowSensor.DEGREES_270:
                    y = SIZE - y - 1

                for x in range(0, SIZE):
                    if rotation == FlowSensor.DEGREES_180 or rotation == FlowSensor.DEGREES_90:
                        x = SIZE - x - 1

                    if rotation == FlowSensor.DEGREES_90 or rotation == FlowSensor.DEGREES_270:
                        offset = (x * 35) + y
                    else:
                        offset = (y * 35) + x

                    value = data[offset]
                    print(value_to_char(value), end="")
                print()
        else:
            print("Capture failed. {} bytes received, of {}. Recapturing in ".format(data_size, BYTES))

        print("5...")
        time.sleep(1.0)
        print("4...")
        time.sleep(1.0)
        print("3...")
        time.sleep(1.0)
        print("2...")
        time.sleep(1.0)
        print("Get Ready!")
        time.sleep(1.0)


if __name__ == "__main__":
    cursor.hide()
    pico = Pico(list_devices()[-1])
    pico.import_libs()
    pico.record_flow()
    # pico.setup_of_sensor()
    # pico.record_environment()
    # vals = ['temp', 'pressure', 'humidity', 'time']
    # with open(r'/Users/roaldarbol/Desktop/temps.csv', 'a') as f:
    #     writer = csv.writer(f)
    #     writer.writerow(vals)
    
    # try:
    #     # light = pico.record_light()
    #     while True:
    #         temp = pico.record_environment()
    #         now = dt.now()
    #         dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    #         temp.append(dt_string)
    #         # print(temp)
    #         # with open(r'/Users/roaldarbol/Desktop/temps.csv', 'a') as f:
    #         #     writer = csv.writer(f)
    #         #     writer.writerow(temp)
    #         sys.stdout.write("\r{0}: {1}".format(dt_string, temp))
    #         sys.stdout.flush()
    #         time.sleep(300)
    #     # vals.append(light)
        
    #     # pico.led_toggle()
    # except:
    #     pass
    # print(vals)
    # pico.led_off()
    pico.close()



#     import asyncio
# import time
# from breakout_paa5100 import BreakoutPAA5100 as FlowSensor

# def setup():
#     BG_SPI_FRONT = 0
#     BG_SPI_BACK = 1

#     flo1 = FlowSensor(
#         slot=BG_SPI_FRONT
#     ) # Front
#     flo2 = FlowSensor(
#         slot=BG_SPI_BACK
#     )
#     # flo2 = FlowSensor(cs=22) # Back
#     flo1.set_rotation(FlowSensor.DEGREES_180)
#     flo2.set_rotation(FlowSensor.DEGREES_180)

#     tx = 0
#     ty = 0
#     tz = 0
#     x = 0
#     y = 0
#     z = 0

# async def main():
#     setup()

#     while True:
#         delta = await asyncio.create_task(flo1.get_motion())
#         delta2 = flo2.get_motion()
#         if delta is not None: 
#             y = delta[1]
#             ty += y
#         if delta2 is not None:
#             x = delta2[0]
#             z = delta2[1]
#             tx += x
#             tz += z
#         print("Relative, rel: x {}, y {}, z {} | Absolute: tx {}, ty {}, tz {}".format(x, y, z, tx, ty, tz))
#         # print(delta[0], delta2[0])
#         # if KeyboardInterrupt():
#         #     break
    
# async def main():
#     setup()
#     asyncio.create_task(myloop())

# async.run(main())